"""Tool registration system for the PyGithub MCP Server.

This module provides a decorator-based tool registration system that allows
tools to be organized into logical groups and loaded dynamically based on
configuration.
"""

import importlib
import logging
import inspect
from functools import wraps
from typing import Dict, List, Callable, Any, Optional, Set

# Get logger
logger = logging.getLogger(__name__)

# Registry to store tool metadata
_tool_registry: Dict[str, Callable] = {}
_registered_modules: Set[str] = set()

def tool():
    """Decorator to register a function as an MCP tool.
    
    This decorator adds the function to the tool registry for later registration
    with the MCP server. It also handles automatic conversion of dictionary
    parameters to Pydantic models based on the function's type annotations.
    
    Example:
        @tool()
        def create_issue(params: CreateIssueParams) -> dict:
            # Implementation
    
    Returns:
        Function decorator that registers the decorated function
    """
    def decorator(func):
        func_name = func.__name__
        logger.debug(f"Registering tool: {func_name}")
        
        import inspect
        
        # Get function signature and parameter types
        sig = inspect.signature(func)
        param_types = {
            param.name: param.annotation 
            for param in sig.parameters.values()
            if param.annotation != inspect.Parameter.empty
        }
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Convert dictionary parameters to Pydantic models
            converted_args = list(args)
            for i, arg in enumerate(args):
                if i < len(sig.parameters) and isinstance(arg, dict):
                    param_name = list(sig.parameters.keys())[i]
                    if param_name in param_types:
                        model_type = param_types[param_name]
                        # Handle Pydantic v2 models
                        if hasattr(model_type, "model_validate"):
                            try:
                                converted_args[i] = model_type.model_validate(arg)
                                logger.debug(f"Converted dict to {model_type.__name__} for parameter {param_name}")
                            except Exception as e:
                                logger.error(f"Failed to convert dict to {model_type.__name__}: {e}")
                    
            for name, value in list(kwargs.items()):
                if name in param_types and isinstance(value, dict):
                    model_type = param_types[name]
                    # Handle Pydantic v2 models
                    if hasattr(model_type, "model_validate"):
                        try:
                            kwargs[name] = model_type.model_validate(value)
                            logger.debug(f"Converted dict to {model_type.__name__} for parameter {name}")
                        except Exception as e:
                            logger.error(f"Failed to convert dict to {model_type.__name__}: {e}")
            
            return func(*converted_args, **kwargs)
        
        # Store the wrapper in the registry
        _tool_registry[func_name] = wrapper
        
        return wrapper
    
    return decorator

def register_tools(mcp, tools_list: List[Callable]) -> None:
    """Register multiple tools with the MCP server.
    
    Args:
        mcp: The MCP server instance
        tools_list: List of tool functions to register
    """
    for tool_func in tools_list:
        logger.debug(f"Registering tool with MCP: {tool_func.__name__}")
        mcp.tool()(tool_func)

def load_tools(mcp, config: Dict[str, Any]) -> None:
    """Load and register tools based on configuration.
    
    This function dynamically imports tool modules based on the configuration
    and registers the tools with the MCP server.
    
    Args:
        mcp: The MCP server instance
        config: Configuration dictionary with tool groups
    """
    loaded_count = 0
    
    for group_name, group_config in config.get("tool_groups", {}).items():
        if not group_config.get("enabled", False):
            logger.debug(f"Tool group '{group_name}' is disabled")
            continue
            
        logger.debug(f"Loading tool group: {group_name}")
        try:
            # Import the tool module dynamically
            module_path = f"pygithub_mcp_server.tools.{group_name}"
            module = importlib.import_module(module_path)
            
            # Call the register function
            if hasattr(module, "register"):
                module.register(mcp)
                _registered_modules.add(module_path)
                loaded_count += 1
            else:
                logger.warning(f"No register function found in {module_path}")
        except ImportError as e:
            logger.error(f"Failed to import tool group '{group_name}': {e}")
        except Exception as e:
            logger.error(f"Error loading tool group '{group_name}': {e}")
    
    logger.debug(f"Loaded {loaded_count} tool groups")
    
    if loaded_count == 0:
        logger.warning("No tool groups were loaded! Check your configuration.")
