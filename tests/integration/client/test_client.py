"""Integration tests for GitHub client.

This module tests the GitHubClient class with the real GitHub API.
"""

import os
import pytest
from datetime import datetime

from github import GithubException

from pygithub_mcp_server.client.client import GitHubClient
from pygithub_mcp_server.errors.exceptions import (
    GitHubError,
    GitHubAuthenticationError,
    GitHubPermissionError,
    GitHubRateLimitError,
    GitHubResourceNotFoundError,
    GitHubValidationError,
)


@pytest.mark.integration
def test_singleton_pattern(github_client):
    """Test that GitHubClient follows singleton pattern."""
    # First instance
    client1 = GitHubClient.get_instance()
    assert isinstance(client1, GitHubClient)
    
    # Second instance should be same object
    client2 = GitHubClient.get_instance()
    assert client1 is client2
    
    # Should be the same as the fixture instance
    assert client1 is github_client


@pytest.mark.integration
def test_direct_instantiation():
    """Test that direct instantiation is prevented."""
    with pytest.raises(RuntimeError) as exc:
        GitHubClient()
    assert "Use GitHubClient.get_instance()" in str(exc.value)


@pytest.mark.integration
def test_github_property(github_client):
    """Test github property returns a valid PyGithub instance."""
    # Access github property
    github = github_client.github
    
    # Verify it's a valid instance by calling a method
    rate_limit = github.get_rate_limit()
    assert hasattr(rate_limit, 'core')
    assert hasattr(rate_limit.core, 'limit')
    assert hasattr(rate_limit.core, 'remaining')
    assert hasattr(rate_limit.core, 'reset')


@pytest.mark.integration
def test_get_repo_success(github_client, test_owner, test_repo_name, with_retry):
    """Test successful repository retrieval."""
    @with_retry
    def get_test_repo():
        return github_client.get_repo(f"{test_owner}/{test_repo_name}")
    
    # Get repository
    repo = get_test_repo()
    
    # Verify
    assert repo.full_name == f"{test_owner}/{test_repo_name}"


@pytest.mark.integration
def test_get_repo_not_found(github_client, test_owner, with_retry):
    """Test repository not found error."""
    nonexistent_repo = f"{test_owner}/nonexistent-repo-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    @with_retry
    def get_nonexistent_repo():
        with pytest.raises(GitHubResourceNotFoundError) as exc:
            github_client.get_repo(nonexistent_repo)
        return exc
    
    # Try to get nonexistent repository
    exc = get_nonexistent_repo()
    
    # Verify
    assert "not found" in str(exc.value).lower()


@pytest.mark.integration
def test_get_repo_invalid_name(github_client, with_retry):
    """Test repository with invalid name."""
    invalid_repo = "invalid/repo/name"
    
    @with_retry
    def get_invalid_repo():
        with pytest.raises(GitHubError) as exc:
            github_client.get_repo(invalid_repo)
        return exc
    
    # Try to get repository with invalid name
    exc = get_invalid_repo()
    
    # Verify
    assert "invalid" in str(exc.value).lower() or "not found" in str(exc.value).lower()
