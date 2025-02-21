#!/usr/bin/env python3
"""CLI entry point for GitHub MCP Server."""

from github.server import mcp

def main():
    """Run the GitHub MCP server."""
    mcp.run("stdio")
    return 0

if __name__ == "__main__":
    main()
