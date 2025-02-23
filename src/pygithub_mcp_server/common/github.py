"""GitHub client singleton.

This module provides a singleton class for managing the PyGithub instance
and handling GitHub API interactions through the PyGithub library.
"""

import logging
import os
import sys
from typing import Optional, Dict, Any

from github import Auth, Github, GithubException
from github.Repository import Repository

# Get logger
logger = logging.getLogger(__name__)

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
        token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
        logger.debug("Initializing GitHub client")
        
        if not token:
            logger.error("GITHUB_PERSONAL_ACCESS_TOKEN not set")
            raise GitHubError("GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set")

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

    def _handle_github_exception(self, error: GithubException, resource_hint: Optional[str] = None) -> GitHubError:
        """Map PyGithub exceptions to our error types.

        Args:
            error: PyGithub exception
            resource_hint: Optional hint about the resource type being accessed

        Returns:
            Appropriate GitHubError subclass instance
        """
        data = error.data if hasattr(error, "data") else None
        logger.error(f"Handling GitHub exception: status={error.status}, data={data}")

        # Extract useful information from the error message
        error_msg = str(error)
        
        # Determine resource type, prioritizing the hint
        resource_type = resource_hint
        if not resource_type:
            if data and "resource" in data:
                resource_type = data["resource"]
            elif "issue" in error_msg.lower():
                resource_type = "issue"
            elif "repository" in error_msg.lower():
                resource_type = "repository"
            elif "comment" in error_msg.lower():
                resource_type = "comment"
            elif "label" in error_msg.lower():
                resource_type = "label"

        if error.status == 401:
            logger.error("Authentication error")
            return GitHubAuthenticationError(
                "Authentication failed. Please verify your GitHub token.",
                data
            )
        elif error.status == 403:
            if "rate limit" in error_msg.lower():
                logger.error("Rate limit exceeded")
                headers = getattr(error, "headers", {}) or {}
                reset_time = headers.get("X-RateLimit-Reset")
                return GitHubRateLimitError(
                    "API rate limit exceeded. Please wait before making more requests.",
                    reset_time,
                    data
                )
            logger.error("Permission denied")
            return GitHubPermissionError(
                "You don't have permission to perform this operation.",
                data
            )
        elif error.status == 404:
            logger.error("Resource not found")
            msg = "Resource not found"
            if resource_type:
                msg = f"{resource_type.title()} not found"
            return GitHubResourceNotFoundError(msg, data)
        elif error.status == 422:
            logger.error("Validation error")
            return GitHubValidationError(
                self._format_validation_error(error_msg, data),
                data
            )
        else:
            logger.error(f"Unknown GitHub error: {error.status}")
            return GitHubError(
                f"GitHub API error (HTTP {error.status}): {error_msg}",
                data
            )

    def _format_validation_error(self, error_msg: str, data: Optional[Dict[str, Any]]) -> str:
        """Format validation error message to be more user-friendly.

        Args:
            error_msg: Original error message
            data: Error response data

        Returns:
            Formatted error message
        """
        if not data:
            return error_msg

        # Extract validation errors from response data
        errors = data.get("errors", [])
        if not errors:
            return error_msg

        # Format each validation error
        formatted_errors = []
        for error in errors:
            if "field" in error:
                field = error["field"]
                code = error.get("code", "invalid")
                message = error.get("message", "is invalid")
                formatted_errors.append(f"- {field}: {message} ({code})")

        if formatted_errors:
            return "Validation failed:\n" + "\n".join(formatted_errors)
        return error_msg
