"""Tests for GitHub client singleton.

This module tests the GitHubClient singleton class that manages PyGithub
instance and handles GitHub API interactions.
"""

import os
import pytest
from unittest.mock import Mock, ANY
from datetime import datetime

from github import Auth, Github, GithubException
from github.Repository import Repository

from pygithub_mcp_server.common.github import GitHubClient
from pygithub_mcp_server.common.errors import (
    GitHubError,
    GitHubAuthenticationError,
    GitHubPermissionError,
    GitHubRateLimitError,
    GitHubResourceNotFoundError,
    GitHubValidationError,
)


def test_singleton_pattern(mock_github_class, mock_auth):
    """Test that GitHubClient follows singleton pattern."""
    # First instance
    client1 = GitHubClient.get_instance()
    assert isinstance(client1, GitHubClient)
    
    # Second instance should be same object
    client2 = GitHubClient.get_instance()
    assert client1 is client2
    
    # Verify Github initialization
    mock_auth.Token.assert_called_once_with("test-token")
    mock_github_class.assert_called_once_with(auth=mock_auth.Token.return_value)


def test_direct_instantiation(reset_github_client):
    """Test that direct instantiation is prevented."""
    with pytest.raises(RuntimeError) as exc:
        GitHubClient()
    assert "Use GitHubClient.get_instance()" in str(exc.value)


def test_client_initialization(mock_github_class, mock_auth):
    """Test client initialization with token."""
    client = GitHubClient.get_instance()
    assert client._github is not None
    mock_auth.Token.assert_called_once_with("test-token")
    mock_github_class.assert_called_once_with(auth=mock_auth.Token.return_value)


def test_missing_token(monkeypatch):
    """Test initialization without token."""
    monkeypatch.delenv("GITHUB_PERSONAL_ACCESS_TOKEN", raising=False)
    
    with pytest.raises(GitHubError) as exc:
        GitHubClient.get_instance()
    assert "GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set" in str(exc.value)


def test_get_repo_success(mock_github_class, mock_repo, mock_auth):
    """Test successful repository retrieval."""
    # Setup mock
    mock_github_class.return_value.get_repo.return_value = mock_repo
    
    # Test
    client = GitHubClient.get_instance()
    repo = client.get_repo("owner/repo")
    
    # Verify
    assert repo.full_name == "owner/repo"
    mock_github_class.return_value.get_repo.assert_called_once_with("owner/repo")
    mock_auth.Token.assert_called_once_with("test-token")


def test_get_repo_not_found(mock_github_class, mock_auth):
    """Test repository not found error."""
    # Setup mock
    mock_github_class.return_value.get_repo.side_effect = GithubException(
        404,
        {"message": "Not Found"},
    )
    
    # Test
    client = GitHubClient.get_instance()
    with pytest.raises(GitHubResourceNotFoundError) as exc:
        client.get_repo("owner/nonexistent")
    
    # Verify
    assert "Repository not found" in str(exc.value)
    mock_auth.Token.assert_called_once_with("test-token")


def test_authentication_error(mock_github_class, mock_auth):
    """Test authentication error handling."""
    # Setup mock
    mock_github_class.return_value.get_repo.side_effect = GithubException(
        401,
        {"message": "Bad credentials"},
    )
    
    # Test
    client = GitHubClient.get_instance()
    with pytest.raises(GitHubAuthenticationError) as exc:
        client.get_repo("owner/repo")
    
    # Verify
    assert "Authentication failed" in str(exc.value)
    mock_auth.Token.assert_called_once_with("test-token")


def test_rate_limit_error(mock_github_class, mock_auth):
    """Test rate limit error handling."""
    # Setup mock
    mock_github_class.return_value.get_repo.side_effect = GithubException(
        403,
        {
            "message": "API rate limit exceeded",
            "documentation_url": "https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting"
        }
    )
    
    # Test
    client = GitHubClient.get_instance()
    with pytest.raises(GitHubRateLimitError) as exc:
        client.get_repo("owner/repo")
    
    # Verify
    assert "rate limit exceeded" in str(exc.value).lower()
    mock_auth.Token.assert_called_once_with("test-token")


def test_permission_error(mock_github_class, mock_auth):
    """Test permission error handling."""
    # Setup mock
    mock_github_class.return_value.get_repo.side_effect = GithubException(
        403,
        {"message": "Resource not accessible by integration"}
    )
    
    # Test
    client = GitHubClient.get_instance()
    with pytest.raises(GitHubPermissionError) as exc:
        client.get_repo("owner/repo")
    
    # Verify
    assert "permission" in str(exc.value).lower()
    mock_auth.Token.assert_called_once_with("test-token")


def test_validation_error(mock_github_class, mock_auth):
    """Test validation error handling."""
    # Setup mock
    mock_github_class.return_value.get_repo.side_effect = GithubException(
        422,
        {
            "message": "Validation Failed",
            "errors": [
                {
                    "resource": "Repository",
                    "code": "custom",
                    "message": "Invalid repository name"
                }
            ]
        }
    )
    
    # Test
    client = GitHubClient.get_instance()
    with pytest.raises(GitHubValidationError) as exc:
        client.get_repo("invalid/repo/name")
    
    # Verify
    assert "Validation" in str(exc.value)
    mock_auth.Token.assert_called_once_with("test-token")


def test_unknown_error(mock_github_class, mock_auth):
    """Test unknown error handling."""
    # Setup mock
    mock_github_class.return_value.get_repo.side_effect = GithubException(
        500,
        {"message": "Internal server error"}
    )
    
    # Test
    client = GitHubClient.get_instance()
    with pytest.raises(GitHubError) as exc:
        client.get_repo("owner/repo")
    
    # Verify
    assert "500" in str(exc.value)
    assert "Internal server error" in str(exc.value)
    mock_auth.Token.assert_called_once_with("test-token")


def test_error_with_no_response_data(mock_github_class, mock_auth):
    """Test error handling when no response data is available."""
    # Setup mock
    mock_github_class.return_value.get_repo.side_effect = GithubException(
        404,
        None  # No response data
    )
    
    # Test
    client = GitHubClient.get_instance()
    with pytest.raises(GitHubResourceNotFoundError) as exc:
        client.get_repo("owner/repo")
    
    # Verify
    assert "not found" in str(exc.value).lower()
    mock_auth.Token.assert_called_once_with("test-token")
