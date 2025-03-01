"""Error formatting utilities.

This module provides functions for formatting GitHub API errors for display
and error handling.
"""

from typing import Any

from .exceptions import (
    GitHubAuthenticationError,
    GitHubConflictError,
    GitHubError,
    GitHubPermissionError,
    GitHubRateLimitError,
    GitHubResourceNotFoundError,
    GitHubValidationError,
)


def format_github_error(error: GitHubError) -> str:
    """Format a GitHub error for display.

    Args:
        error: The GitHub error to format

    Returns:
        Formatted error message with context
    """
    message = f"GitHub API Error: {str(error)}"

    if isinstance(error, GitHubValidationError):
        message = f"Validation Error: {str(error)}"
        if error.response:
            message += f"\nDetails: {error.response}"
    elif isinstance(error, GitHubResourceNotFoundError):
        message = f"Not Found: {str(error)}"
    elif isinstance(error, GitHubAuthenticationError):
        message = f"Authentication Failed: {str(error)}"
    elif isinstance(error, GitHubPermissionError):
        message = f"Permission Denied: {str(error)}"
    elif isinstance(error, GitHubRateLimitError):
        reset_info = f"Resets at: {error.reset_at.isoformat() if error.reset_at else 'unknown'}"
        message = f"Rate Limit Exceeded: {str(error)}\n{reset_info}"
    elif isinstance(error, GitHubConflictError):
        message = f"Conflict: {str(error)}"

    return message


def is_github_error(error: Any) -> bool:
    """Check if an error is a GitHub error.

    Args:
        error: Error to check

    Returns:
        True if error is a GitHub error, False otherwise
    """
    return isinstance(error, GitHubError)
