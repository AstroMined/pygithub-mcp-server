"""Common utilities for GitHub API operations.

This module provides common utilities for GitHub API operations, including
error handling, GitHub client, and conversion utilities.

DEPRECATED: This module is deprecated. Import from the appropriate modules instead:
- For converters: import from pygithub_mcp_server.converters
- For errors: import from pygithub_mcp_server.errors
- For GitHub client: import from pygithub_mcp_server.client
- For utilities: import from pygithub_mcp_server.utils
"""

import warnings

# Show deprecation warning
warnings.warn(
    "The pygithub_mcp_server.common module is deprecated. "
    "Import from the appropriate modules instead:\n"
    "- For converters: import from pygithub_mcp_server.converters\n"
    "- For errors: import from pygithub_mcp_server.errors\n"
    "- For GitHub client: import from pygithub_mcp_server.client\n"
    "- For utilities: import from pygithub_mcp_server.utils",
    DeprecationWarning,
    stacklevel=2
)

# Re-export all from the new locations for backward compatibility
from pygithub_mcp_server.converters import *
from pygithub_mcp_server.errors import *
from pygithub_mcp_server.client import *
from pygithub_mcp_server.utils import *

# Re-export version
from .version import (
    VERSION,
    VERSION_MAJOR,
    VERSION_MINOR,
    VERSION_PATCH,
    VERSION_TUPLE,
    get_version,
    get_version_tuple,
)

__all__ = [
    # Version
    "VERSION",
    "VERSION_MAJOR",
    "VERSION_MINOR",
    "VERSION_PATCH",
    "VERSION_TUPLE",
    "get_version",
    "get_version_tuple",
]
