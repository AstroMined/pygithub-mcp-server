"""Environment and configuration utilities.

This module provides functions for accessing environment variables and
configuration settings.
"""

import os

from pygithub_mcp_server.errors import GitHubError


def get_github_token() -> str:
    """Get GitHub personal access token from environment.

    Returns:
        GitHub personal access token

    Raises:
        GitHubError: If token is not set in environment
    """
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        raise GitHubError("GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set")
    return token
