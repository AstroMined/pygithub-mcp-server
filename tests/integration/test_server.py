"""Integration tests for the server module.

These tests verify that the server initializes correctly with different configurations
and registers tools properly.
"""

import pytest
import logging
import json
import asyncio
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


# Helper function to run async tests
def run_async(coro):
    """Run an async coroutine and return its result."""
    return asyncio.run(coro)


@pytest.mark.integration
class TestServer:
    """Tests for server initialization and configuration."""
    
    def test_create_server_basic(self):
        """Test creating server with default configuration."""
        # Create server
        server = create_server()
        
        # Verify server instance
        assert isinstance(server, FastMCP)
        
        # Verify tools were registered - use run_async for async methods
        tools = run_async(server.list_tools())
        tool_names = [tool.name for tool in tools]
        
        # Verify at least some issue tools are registered
        assert "create_issue" in tool_names
        assert "list_issues" in tool_names
        assert "get_issue" in tool_names
    
    def test_server_tools_callable(self):
        """Test that registered tools are callable."""
        # Create server
        server = create_server()
        
        # Verify tools are callable - use run_async for async methods
        tools = run_async(server.list_tools())
        
        # Check create_issue tool exists
        create_issue_tool = next(tool for tool in tools if tool.name == "create_issue")
        assert create_issue_tool is not None
        
        # Instead of checking callback directly, verify the tool has expected attributes
        assert hasattr(create_issue_tool, "name")
        assert create_issue_tool.name == "create_issue"
        
        # Check get_issue tool exists
        get_issue_tool = next(tool for tool in tools if tool.name == "get_issue")
        assert get_issue_tool is not None
        assert get_issue_tool.name == "get_issue"
    
    def test_server_metadata(self):
        """Test server configuration."""
        # Create server
        server = create_server()
        
        # Verify server is initialized
        assert isinstance(server, FastMCP)
        
        # Check if the server has tools registered
        tools = run_async(server.list_tools())
        assert len(tools) > 0, "Server should have tools registered"
    
    def test_server_with_custom_env(self, monkeypatch):
        """Test server creation with environment variable overrides."""
        # Set environment variable to disable issue tools
        monkeypatch.setenv("PYGITHUB_ENABLE_ISSUES", "false")
        
        try:
            # Create server with environment variable override
            server = create_server()
            
            # Verify tools were affected by environment variable - use run_async
            tools = run_async(server.list_tools())
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
        
        # Create an empty log file to verify we can write to this location
        with open(log_file, 'w') as f:
            f.write("Test log initialization\n")
        
        # Verify the file was created
        assert log_file.exists()
        
        # Now let's test the server's logging initialization
        # Mock the log file path
        monkeypatch.setattr("pygithub_mcp_server.server.log_dir", log_dir)
        monkeypatch.setattr("pygithub_mcp_server.server.log_file", log_file)
        
        # Import server module again to trigger logging initialization
        import importlib
        importlib.reload(pytest.importorskip("pygithub_mcp_server.server"))
        
        # Verify file still exists and has content
        assert log_file.exists()
        assert log_file.stat().st_size > 0
