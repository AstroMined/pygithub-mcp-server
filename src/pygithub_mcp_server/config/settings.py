"""Configuration settings for the PyGithub MCP Server.

This module handles loading configuration from files and environment variables,
with a focus on tool group enablement.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Default configuration with all tool groups
DEFAULT_CONFIG = {
    "tool_groups": {
        "issues": {"enabled": True},
        "repositories": {"enabled": False},
        "pull_requests": {"enabled": False},
        "discussions": {"enabled": False},
        "search": {"enabled": False},
        "users": {"enabled": False},
        "organizations": {"enabled": False},
        "teams": {"enabled": False},
        "webhooks": {"enabled": False},
        "gists": {"enabled": False},
    }
}

def load_config() -> Dict[str, Any]:
    """Load configuration from file and environment variables.
    
    Configuration is loaded in the following order of precedence:
    1. Default configuration
    2. Configuration file (if specified via PYGITHUB_MCP_CONFIG env var)
    3. Environment variables (PYGITHUB_ENABLE_*)
    
    Returns:
        Dict[str, Any]: The merged configuration
    """
    # Make a deep copy to avoid modifying the original DEFAULT_CONFIG
    config = json.loads(json.dumps(DEFAULT_CONFIG))
    
    # Load from config file if it exists
    config_path = os.environ.get("PYGITHUB_MCP_CONFIG")
    if config_path and Path(config_path).exists():
        try:
            with open(config_path, "r") as f:
                file_config = json.load(f)
                logger.debug(f"Loaded configuration from {config_path}")
                
                # Merge with default config
                if "tool_groups" in file_config:
                    for group, settings in file_config["tool_groups"].items():
                        if group in config["tool_groups"]:
                            config["tool_groups"][group].update(settings)
                        else:
                            config["tool_groups"][group] = settings
                            
                # Merge other top-level settings
                for key, value in file_config.items():
                    if key != "tool_groups":
                        config[key] = value
        except Exception as e:
            logger.error(f"Failed to load configuration from {config_path}: {e}")
            # Make sure we reset to the default config when an error occurs
            config = json.loads(json.dumps(DEFAULT_CONFIG))
    
    # Override from environment variables
    for group in config["tool_groups"]:
        env_var = f"PYGITHUB_ENABLE_{group.upper()}"
        if env_var in os.environ:
            enabled = os.environ[env_var].lower() in ("1", "true", "yes", "on")
            config["tool_groups"][group]["enabled"] = enabled
            logger.debug(f"Setting {group} tool group enabled={enabled} from environment variable")
    
    return config
