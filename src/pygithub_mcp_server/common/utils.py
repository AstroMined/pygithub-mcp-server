"""Utility functions for GitHub API operations.

DEPRECATED: This module is deprecated. Import from the appropriate modules instead:
- For environment utilities: import from pygithub_mcp_server.utils
- For parameter formatting: import from pygithub_mcp_server.converters
- For response formatting: import from pygithub_mcp_server.converters

This module re-exports utility functions from the new locations for backward compatibility.
"""

import warnings

# Show deprecation warning
warnings.warn(
    "The pygithub_mcp_server.common.utils module is deprecated. "
    "Import from the appropriate modules instead:\n"
    "- For environment utilities: import from pygithub_mcp_server.utils\n"
    "- For parameter formatting: import from pygithub_mcp_server.converters\n"
    "- For response formatting: import from pygithub_mcp_server.converters",
    DeprecationWarning,
    stacklevel=2
)

# Re-export utility functions from the new locations
from pygithub_mcp_server.utils import get_github_token
from pygithub_mcp_server.converters import format_query_params, create_tool_response

# Constants
API_BASE_URL = "https://api.github.com"
API_VERSION = "2022-11-28"
DEFAULT_HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": API_VERSION,
}

__all__ = [
    # Environment utilities
    "get_github_token",
    
    # Parameter formatting
    "format_query_params",
    
    # Response formatting
    "create_tool_response",
    
    # Constants
    "API_BASE_URL",
    "API_VERSION",
    "DEFAULT_HEADERS",
]
