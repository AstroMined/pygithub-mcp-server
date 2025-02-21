"""Entry point for the GitHub MCP Server.

This module provides the main entry point for running the server.
"""

from github_mcp_server.server import mcp

def main():
    """Run the GitHub MCP server."""
    mcp.run()

if __name__ == "__main__":
    main()
