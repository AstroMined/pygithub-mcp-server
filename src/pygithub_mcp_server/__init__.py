"""GitHub MCP Server.

This package provides a Model Context Protocol server for interacting with
the GitHub API. It exposes tools for common GitHub operations like managing
issues, repositories, and pull requests.
"""

from .server import mcp
from .version import VERSION

__version__ = VERSION
__all__ = ["mcp", "__version__"]
