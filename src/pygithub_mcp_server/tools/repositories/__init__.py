"""Repository tools module.

This module provides MCP tools for GitHub repository operations.
"""

from mcp.server.fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    """Register all repository tools with the MCP server.

    Args:
        mcp: The MCP server instance
    """
    from pygithub_mcp_server.tools import register_tools
    from .tools import (
        get_repository,
        create_repository,
        fork_repository,
        search_repositories,
        get_file_contents,
        create_or_update_file,
        push_files,
        create_branch,
        list_commits
    )

    # Register all repository tools
    register_tools(mcp, [
        get_repository,
        create_repository,
        fork_repository,
        search_repositories,
        get_file_contents,
        create_or_update_file,
        push_files,
        create_branch,
        list_commits
    ])
