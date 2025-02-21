"""GitHub API error handling.

This module defines custom exceptions for GitHub API operations, providing
clear error messages and proper error context.
"""

from datetime import datetime
from typing import Any, Dict, Optional


class GitHubError(Exception):
    """Base exception for GitHub API errors."""

    def __init__(self, message: str, response: Optional[Dict[str, Any]] = None) -> None:
        """Initialize GitHub error.

        Args:
            message: Error message
            response: Optional raw API response data
        """
        super().__init__(message)
        self.response = response


class GitHubValidationError(GitHubError):
    """Raised when request validation fails."""

    pass


class GitHubResourceNotFoundError(GitHubError):
    """Raised when a requested resource is not found."""

    pass


class GitHubAuthenticationError(GitHubError):
    """Raised when authentication fails."""

    pass


class GitHubPermissionError(GitHubError):
    """Raised when the authenticated user lacks required permissions."""

    pass


class GitHubRateLimitError(GitHubError):
    """Raised when GitHub API rate limit is exceeded."""

    def __init__(
        self, message: str, reset_at: datetime, response: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize rate limit error.

        Args:
            message: Error message
            reset_at: When the rate limit will reset
            response: Optional raw API response data
        """
        super().__init__(message, response)
        self.reset_at = reset_at


class GitHubConflictError(GitHubError):
    """Raised when there is a conflict with the current state."""

    pass


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
        message = f"Rate Limit Exceeded: {str(error)}\nResets at: {error.reset_at.isoformat()}"
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
