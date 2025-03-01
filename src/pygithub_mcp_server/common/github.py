"""GitHub client singleton.

DEPRECATED: This module is deprecated. Import from pygithub_mcp_server.client instead.

This module re-exports the GitHub client from the new location for backward compatibility.
"""

import warnings

# Show deprecation warning
warnings.warn(
    "The pygithub_mcp_server.common.github module is deprecated. "
    "Import from pygithub_mcp_server.client instead.",
    DeprecationWarning,
    stacklevel=2
)

# Re-export GitHub client from the new location
from pygithub_mcp_server.client import (
    GitHubClient,
    check_rate_limit,
    wait_for_rate_limit_reset,
    exponential_backoff,
    handle_rate_limit_with_backoff,
)

__all__ = [
    "GitHubClient",
    "check_rate_limit",
    "wait_for_rate_limit_reset",
    "exponential_backoff",
    "handle_rate_limit_with_backoff",
]
