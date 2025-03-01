"""GitHub client singleton.

This module provides a singleton class for managing the PyGithub instance
and handling GitHub API interactions through the PyGithub library.

This package replaces the monolithic github.py file with a more organized structure.
"""

from .client import GitHubClient
from .rate_limit import (
    check_rate_limit,
    wait_for_rate_limit_reset,
    exponential_backoff,
    handle_rate_limit_with_backoff,
)

__all__ = [
    # Client
    "GitHubClient",
    
    # Rate limit
    "check_rate_limit",
    "wait_for_rate_limit_reset",
    "exponential_backoff",
    "handle_rate_limit_with_backoff",
]
