"""GitHub API error handling.

This module defines custom exceptions for GitHub API operations, providing
clear error messages and proper error context.

This package replaces the monolithic errors.py file with a more organized structure.
"""

from .exceptions import (
    GitHubError,
    GitHubValidationError,
    GitHubResourceNotFoundError,
    GitHubAuthenticationError,
    GitHubPermissionError,
    GitHubRateLimitError,
    GitHubConflictError,
)

from .formatters import format_github_error, is_github_error
from .handlers import handle_github_exception, format_validation_error

__all__ = [
    # Exceptions
    "GitHubError",
    "GitHubValidationError",
    "GitHubResourceNotFoundError",
    "GitHubAuthenticationError",
    "GitHubPermissionError",
    "GitHubRateLimitError",
    "GitHubConflictError",
    
    # Formatters
    "format_github_error",
    "is_github_error",
    
    # Handlers
    "handle_github_exception",
    "format_validation_error",
]
