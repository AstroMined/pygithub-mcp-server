"""GitHub API exception classes.

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
        self, message: str, reset_at: Optional[datetime] = None, response: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize rate limit error.

        Args:
            message: Error message
            reset_at: When the rate limit will reset, or None if unknown
            response: Optional raw API response data
        """
        super().__init__(message, response)
        self.reset_at = reset_at


class GitHubConflictError(GitHubError):
    """Raised when there is a conflict with the current state."""

    pass
