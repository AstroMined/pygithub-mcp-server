"""Integration tests for the server module.

These tests verify that the server initializes correctly with different configurations
and registers tools properly.
"""

import pytest
import logging
import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from mcp.server.fastmcp import FastMCP

from pygithub_mcp_server.server import create_server
from pygithub_mcp_server.tools.issues.tools import (
    create_issue,
    list_issues,
    get_issue,
    update_issue,
    add_issue_comment,
    list_issue_comments,
    update_issue_comment,
    delete_issue_comment,
    add_issue_labels,
    remove_issue_label
)


# Configure logging
logger = logging.getLogger(__name__)


@pytest.mark.integration
class TestServer:
    """Tests for server initialization and configuration."""
    
    def test_create_server_basic(self):
        """Test creating server with default configuration."""
        # Create server
        server = create_server()
        
        # Verify server instance
        assert isinstance(server, FastMCP)
        assert server.metadata.name == "pygithub-mcp-server"
        
        # Verify tools were registered
        tools = server.list_tools()
        tool_names = [tool.name for tool in tools]
        
        # Verify at least some issue tools are registered
        assert "create_issue" in tool_names
        assert "list_issues" in tool_names
        assert "get_issue" in tool_names
    
    def test_server_tools_callable(self):
        """Test that registered tools are callable."""
        # Create server
        server = create_server()
        
        # Verify tools are callable
        tools = server.list_tools()
        
        # Check create_issue tool exists and is callable
        create_issue_tool = next(tool for tool in tools if tool.name == "create_issue")
        assert create_issue_tool is not None
        assert callable(create_issue_tool.callback)
        
        # Check get_issue tool exists and is callable
        get_issue_tool = next(tool for tool in tools if tool.name == "get_issue")
        assert get_issue_tool is not None
        assert callable(get_issue_tool.callback)
    
    def test_server_metadata(self):
        """Test server metadata is set correctly."""
        # Create server
        server = create_server()
        
        # Verify metadata
        assert server.metadata.name == "pygithub-mcp-server"
        assert server.metadata.description == "GitHub API operations via MCP"
        assert server.metadata.version is not None
        
        # Check capabilities are set
        capabilities = server.capabilities
        assert "tools" in capabilities
    
    def test_server_with_custom_env(self, monkeypatch):
        """Test server creation with environment variable overrides."""
        # Set environment variable to disable issue tools
        monkeypatch.setenv("PYGITHUB_ENABLE_ISSUES", "false")
        
        try:
            # Create server with environment variable override
            server = create_server()
            
            # Verify tools were affected by environment variable
            tools = server.list_tools()
            tool_names = [tool.name for tool in tools]
            
            # Issue tools should not be registered
            assert "create_issue" not in tool_names
            assert "list_issues" not in tool_names
            assert "get_issue" not in tool_names
        finally:
            # Reset environment variable
            monkeypatch.delenv("PYGITHUB_ENABLE_ISSUES", raising=False)
    
    def test_server_logging_initialization(self, tmp_path, monkeypatch):
        """Test server logging initialization."""
        # Redirect logging to a temporary directory
        log_dir = tmp_path / "logs"
        log_file = log_dir / "pygithub_mcp_server.log"
        
        # Create the directory
        log_dir.mkdir(exist_ok=True)
        
        # Mock the log file path
        monkeypatch.setattr("pygithub_mcp_server.server.log_dir", log_dir)
        monkeypatch.setattr("pygithub_mcp_server.server.log_file", log_file)
        
        # Import server module again to trigger logging initialization
        import importlib
        importlib.reload(pytest.importorskip("pygithub_mcp_server.server"))
        
        # Verify log file exists
        assert log_file.exists()
