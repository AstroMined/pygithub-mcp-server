"""Entry point for the PyGithub MCP Server.

This module provides the main entry point for running the server.
"""

from pygithub_mcp_server.server import create_server

def main():
    """Run the GitHub MCP server."""
    server = create_server()
    server.run()

if __name__ == "__main__":
    main()
