"""GitHub client singleton.

This module provides a singleton class for managing the PyGithub instance
and handling GitHub API interactions through the PyGithub library.
"""

import logging
import os
from typing import Optional

from github import Auth, Github, GithubException, RateLimitExceededException
from github.Repository import Repository

from pygithub_mcp_server.errors import (
    GitHubError,
    handle_github_exception,
)
from pygithub_mcp_server.utils import get_github_token

# Get logger
logger = logging.getLogger(__name__)


class GitHubClient:
    """Singleton class for managing PyGithub instance."""

    _instance: Optional["GitHubClient"] = None
    _github: Optional[Github] = None
    _created_via_get_instance: bool = False
    _initialized: bool = False

    def __init__(self) -> None:
        """Initialize GitHub client.

        Note: Use get_instance() instead of constructor.
        
        Raises:
            RuntimeError: If instantiated directly instead of through get_instance()
        """
        if not GitHubClient._created_via_get_instance:
            raise RuntimeError("Use GitHubClient.get_instance() instead")
        GitHubClient._created_via_get_instance = False  # Reset for next instantiation

    @classmethod
    def get_instance(cls) -> "GitHubClient":
        """Get singleton instance.

        Returns:
            GitHubClient instance
        """
        if cls._instance is None:
            cls._created_via_get_instance = True
            cls._instance = cls()
            cls._instance._init_client()
        return cls._instance

    def _init_client(self) -> None:
        """Initialize PyGithub client with token authentication."""
        if self._initialized:
            return

        # Initialize real client
        token = get_github_token()
        logger.debug("Initializing GitHub client")
        
        logger.debug("Token found, creating GitHub client")
        self._create_client(token)
        logger.debug("GitHub client initialized successfully")
        self._initialized = True

    def _create_client(self, token: str) -> None:
        """Create PyGithub client instance.
        
        Args:
            token: GitHub personal access token
        """
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
        if not self._initialized:
            self._init_client()

        if self._github is None:
            raise GitHubError("GitHub client not initialized")

        return self._github

    def _handle_github_exception(self, exception: GithubException, resource_hint: Optional[str] = None) -> GitHubError:
        """Forward to the module-level handler for consistent error handling.
        
        Args:
            exception: PyGithub exception
            resource_hint: Optional hint about the resource type being accessed
            
        Returns:
            Appropriate GitHubError subclass instance
        """
        return handle_github_exception(exception, resource_hint)

    def get_rate_limit(self):
        """Get rate limit information.
        
        Returns:
            RateLimit: Rate limit information from PyGithub
            
        Raises:
            GitHubError: If rate limit retrieval fails
        """
        logger.debug("Getting rate limit information")
        try:
            return self.github.get_rate_limit()
        except GithubException as e:
            logger.error(f"GitHub exception when getting rate limit: {str(e)}")
            raise self._handle_github_exception(e, resource_hint="rate_limit")
            
    def get_repo(self, full_name: str) -> Repository:
        """Get a repository by full name.

        Args:
            full_name: Repository full name (owner/repo)

        Returns:
            PyGithub Repository object

        Raises:
            GitHubError: If repository access fails
        """
        logger.debug(f"Getting repository: {full_name}")
        try:
            repo = self.github.get_repo(full_name)
            logger.debug(f"Successfully got repository: {full_name}")
            return repo
        except GithubException as e:
            logger.error(f"GitHub exception when getting repo {full_name}: {str(e)}")
            raise self._handle_github_exception(e, resource_hint="repository")
