"""Tests for GitHub client singleton.

This module tests the GitHubClient singleton class that manages PyGithub
instance and handles GitHub API interactions.
"""

import os
import pytest
from unittest.mock import Mock, patch
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


@pytest.fixture
def mock_github():
    """Create a mock Github instance."""
    return Mock(spec=Github)


@pytest.fixture
def mock_repo():
    """Create a mock Repository."""
    repo = Mock(spec=Repository)
    repo.full_name = "owner/repo"
    return repo


@pytest.fixture
def github_token():
    """Set up and tear down GitHub token environment variable."""
    original_token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"] = "test-token"
    yield "test-token"
    if original_token:
        os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"] = original_token
    else:
        del os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]


def test_singleton_pattern():
    """Test that GitHubClient follows singleton pattern."""
    # Clear any existing instance
    GitHubClient._instance = None
    GitHubClient._github = None

    # First instance
    client1 = GitHubClient.get_instance()
    assert isinstance(client1, GitHubClient)

    # Second instance should be same object
    client2 = GitHubClient.get_instance()
    assert client1 is client2


def test_direct_instantiation():
    """Test that direct instantiation is prevented."""
    with pytest.raises(RuntimeError) as exc:
        GitHubClient()
    assert "Use GitHubClient.get_instance()" in str(exc.value)


@patch("github.Github")
def test_client_initialization(mock_github_class, github_token):
    """Test client initialization with token."""
    # Clear any existing instance
    GitHubClient._instance = None
    GitHubClient._github = None

    client = GitHubClient.get_instance()
    assert client._github is not None
    mock_github_class.assert_called_once()


def test_missing_token():
    """Test initialization without token."""
    # Clear any existing instance
    GitHubClient._instance = None
    GitHubClient._github = None
    
    # Remove token from environment
    if "GITHUB_PERSONAL_ACCESS_TOKEN" in os.environ:
        del os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]

    with pytest.raises(GitHubError) as exc:
        GitHubClient.get_instance()
    assert "GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set" in str(exc.value)


@patch("github.Github")
def test_get_repo_success(mock_github_class, mock_repo, github_token):
    """Test successful repository retrieval."""
    # Setup mock
    mock_github_instance = Mock()
    mock_github_instance.get_repo.return_value = mock_repo
    mock_github_class.return_value = mock_github_instance

    # Clear any existing instance
    GitHubClient._instance = None
    GitHubClient._github = None

    # Test
    client = GitHubClient.get_instance()
    repo = client.get_repo("owner/repo")
    assert repo.full_name == "owner/repo"
    mock_github_instance.get_repo.assert_called_once_with("owner/repo")


@patch("github.Github")
def test_get_repo_not_found(mock_github_class, github_token):
    """Test repository not found error."""
    # Setup mock to raise not found error
    mock_github_instance = Mock()
    mock_github_instance.get_repo.side_effect = GithubException(
        404,
        {"message": "Not Found"},
    )
    mock_github_class.return_value = mock_github_instance

    # Clear any existing instance
    GitHubClient._instance = None
    GitHubClient._github = None

    # Test
    client = GitHubClient.get_instance()
    with pytest.raises(GitHubResourceNotFoundError) as exc:
        client.get_repo("owner/nonexistent")
    assert "Repository not found" in str(exc.value)


@patch("github.Github")
def test_authentication_error(mock_github_class, github_token):
    """Test authentication error handling."""
    # Setup mock to raise authentication error
    mock_github_instance = Mock()
    mock_github_instance.get_repo.side_effect = GithubException(
        401,
        {"message": "Bad credentials"},
    )
    mock_github_class.return_value = mock_github_instance

    # Clear any existing instance
    GitHubClient._instance = None
    GitHubClient._github = None

    # Test
    client = GitHubClient.get_instance()
    with pytest.raises(GitHubAuthenticationError) as exc:
        client.get_repo("owner/repo")
    assert "Authentication failed" in str(exc.value)


@patch("github.Github")
def test_rate_limit_error(mock_github_class, github_token):
    """Test rate limit error handling."""
    # Setup mock to raise rate limit error
    mock_github_instance = Mock()
    mock_github_instance.get_repo.side_effect = GithubException(
        403,
        {
            "message": "API rate limit exceeded",
            "documentation_url": "https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting"
        }
    )
    mock_github_class.return_value = mock_github_instance

    # Clear any existing instance
    GitHubClient._instance = None
    GitHubClient._github = None

    # Test
    client = GitHubClient.get_instance()
    with pytest.raises(GitHubRateLimitError) as exc:
        client.get_repo("owner/repo")
    assert "rate limit exceeded" in str(exc.value).lower()


@patch("github.Github")
def test_permission_error(mock_github_class, github_token):
    """Test permission error handling."""
    # Setup mock to raise permission error
    mock_github_instance = Mock()
    mock_github_instance.get_repo.side_effect = GithubException(
        403,
        {"message": "Resource not accessible by integration"}
    )
    mock_github_class.return_value = mock_github_instance

    # Clear any existing instance
    GitHubClient._instance = None
    GitHubClient._github = None

    # Test
    client = GitHubClient.get_instance()
    with pytest.raises(GitHubPermissionError) as exc:
        client.get_repo("owner/repo")
    assert "permission" in str(exc.value).lower()


@patch("github.Github")
def test_validation_error(mock_github_class, github_token):
    """Test validation error handling."""
    # Setup mock to raise validation error
    mock_github_instance = Mock()
    mock_github_instance.get_repo.side_effect = GithubException(
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
    mock_github_class.return_value = mock_github_instance

    # Clear any existing instance
    GitHubClient._instance = None
    GitHubClient._github = None

    # Test
    client = GitHubClient.get_instance()
    with pytest.raises(GitHubValidationError) as exc:
        client.get_repo("invalid/repo/name")
    assert "Validation" in str(exc.value)


@patch("github.Github")
def test_unknown_error(mock_github_class, github_token):
    """Test unknown error handling."""
    # Setup mock to raise unknown error
    mock_github_instance = Mock()
    mock_github_instance.get_repo.side_effect = GithubException(
        500,
        {"message": "Internal server error"}
    )
    mock_github_class.return_value = mock_github_instance

    # Clear any existing instance
    GitHubClient._instance = None
    GitHubClient._github = None

    # Test
    client = GitHubClient.get_instance()
    with pytest.raises(GitHubError) as exc:
        client.get_repo("owner/repo")
    assert "500" in str(exc.value)
    assert "Internal server error" in str(exc.value)


@patch("github.Github")
def test_error_with_no_response_data(mock_github_class, github_token):
    """Test error handling when no response data is available."""
    # Setup mock to raise error without response data
    mock_github_instance = Mock()
    mock_github_instance.get_repo.side_effect = GithubException(
        404,
        None  # No response data
    )
    mock_github_class.return_value = mock_github_instance

    # Clear any existing instance
    GitHubClient._instance = None
    GitHubClient._github = None

    # Test
    client = GitHubClient.get_instance()
    with pytest.raises(GitHubResourceNotFoundError) as exc:
        client.get_repo("owner/repo")
    assert "not found" in str(exc.value).lower()
