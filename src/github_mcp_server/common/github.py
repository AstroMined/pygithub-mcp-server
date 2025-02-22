"""GitHub client singleton.

This module provides a singleton class for managing the PyGithub instance
and handling GitHub API interactions through the PyGithub library.
"""

import os
from typing import Optional

from github import Auth, Github, GithubException
from github.Repository import Repository

from .errors import (
    GitHubAuthenticationError,
    GitHubError,
    GitHubPermissionError,
    GitHubRateLimitError,
    GitHubResourceNotFoundError,
    GitHubValidationError,
)


class GitHubClient:
    """Singleton class for managing PyGithub instance."""

    _instance: Optional["GitHubClient"] = None
    _github: Optional[Github] = None

    def __init__(self) -> None:
        """Initialize GitHub client.

        Note: Use get_instance() instead of constructor.
        """
        if GitHubClient._instance is not None:
            raise RuntimeError("Use GitHubClient.get_instance() instead")
        self._init_client()

    @classmethod
    def get_instance(cls) -> "GitHubClient":
        """Get singleton instance.

        Returns:
            GitHubClient instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _init_client(self) -> None:
        """Initialize PyGithub client with token authentication."""
        token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
        if not token:
            raise GitHubError("GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set")

        auth = Auth.Token(token)
        self._github = Github(auth=auth)

    @property
    def github(self) -> Github:
        """Get PyGithub instance.

        Returns:
            PyGithub instance

        Raises:
            GitHubError: If client is not initialized
        """
        if self._github is None:
            raise GitHubError("GitHub client not initialized")
        return self._github

    def get_repo(self, full_name: str) -> Repository:
        """Get a repository by full name.

        Args:
            full_name: Repository full name (owner/repo)

        Returns:
            PyGithub Repository object

        Raises:
            GitHubError: If repository access fails
        """
        try:
            return self.github.get_repo(full_name)
        except GithubException as e:
            self._handle_github_exception(e)

    def _handle_github_exception(self, error: GithubException) -> None:
        """Map PyGithub exceptions to our error types.

        Args:
            error: PyGithub exception

        Raises:
            GitHubError: Appropriate error type based on exception
        """
        data = error.data if hasattr(error, "data") else None

        if error.status == 401:
            raise GitHubAuthenticationError(str(error), data)
        elif error.status == 403:
            if "rate limit" in str(error).lower():
                # Note: PyGithub provides rate limit info in error.headers
                # but we're keeping the simple message for now
                raise GitHubRateLimitError(str(error), error.headers.get("X-RateLimit-Reset"), data)
            raise GitHubPermissionError(str(error), data)
        elif error.status == 404:
            raise GitHubResourceNotFoundError(str(error), data)
        elif error.status == 422:
            raise GitHubValidationError(str(error), data)
        else:
            raise GitHubError(f"GitHub API error ({error.status}): {str(error)}", data)
