"""Server-specific test fixtures.

This module provides pytest fixtures specifically for testing the FastMCP server
implementation. These fixtures complement the global fixtures from ../conftest.py.
"""

import json
from unittest.mock import Mock, call

import pytest
from mcp.server.fastmcp import FastMCP


@pytest.fixture(scope="function", autouse=True)
def mock_fastmcp(monkeypatch):
    """Mock FastMCP while preserving type checking and tracking decorator calls."""
    # Create mock class with proper spec
    mock_class = Mock(spec=FastMCP)
    mock_instance = Mock(spec=FastMCP)
    mock_class.return_value = mock_instance
    
    # Create tool decorator that tracks calls and preserves function
    def mock_tool():
        def decorator(func):
            wrapped = Mock(wraps=func)
            # Track the decorator call
            mock_instance.tool.mock_calls.append(call())
            return wrapped
        return decorator
    
    # Configure tool method to track calls
    mock_instance.tool = Mock(side_effect=mock_tool)
    mock_instance.tool.mock_calls = []
    
    # Patch both import and usage locations
    monkeypatch.setattr("mcp.server.fastmcp.FastMCP", mock_class)
    monkeypatch.setattr("pygithub_mcp_server.server.FastMCP", mock_class)
    
    # Return the class for constructor call assertions
    return mock_class


@pytest.fixture(scope="function")
def mock_tool_response():
    """Create standard tool response format matching server implementation."""
    def _create_response(content, is_error=False):
        return {
            "content": [{
                # Use 'error' type for error responses
                "type": "error" if is_error else "text",
                "text": json.dumps(content, indent=2)
            }],
            "is_error": is_error
        }
    return _create_response
