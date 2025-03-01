"""GitHub API error handling.

DEPRECATED: This module is deprecated. Import from pygithub_mcp_server.errors instead.

This module re-exports all error classes and functions from the new location
for backward compatibility.
"""

import warnings

# Show deprecation warning
warnings.warn(
    "The pygithub_mcp_server.common.errors module is deprecated. "
    "Import from pygithub_mcp_server.errors instead.",
    DeprecationWarning,
    stacklevel=2
)

# Re-export all error classes and functions from the new location
from pygithub_mcp_server.errors import (
    GitHubError,
    GitHubValidationError,
    GitHubResourceNotFoundError,
    GitHubAuthenticationError,
    GitHubPermissionError,
    GitHubRateLimitError,
    GitHubConflictError,
    format_github_error,
    is_github_error,
    handle_github_exception,
    format_validation_error,
)

__all__ = [
    "GitHubError",
    "GitHubValidationError",
    "GitHubResourceNotFoundError",
    "GitHubAuthenticationError",
    "GitHubPermissionError",
    "GitHubRateLimitError",
    "GitHubConflictError",
    "format_github_error",
    "is_github_error",
    "handle_github_exception",
    "format_validation_error",
]
