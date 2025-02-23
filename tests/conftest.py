"""Shared test configuration and fixtures.

This module provides shared pytest fixtures and configuration for testing
the PyGithub MCP Server.
"""

import os
import pytest
from datetime import datetime
from unittest.mock import Mock, PropertyMock, patch

from github import Github, GithubException, Auth
from github.Issue import Issue
from github.IssueComment import IssueComment
from github.Label import Label
from github.Milestone import Milestone
from github.NamedUser import NamedUser
from github.Repository import Repository

from pygithub_mcp_server.common.github import GitHubClient


# Mock classes that inherit from GitHub classes
class MockGithub(Github):
    """Mock class that inherits from Github."""
    def __init__(self, *args, **kwargs):
        pass

class MockRepository(Repository):
    """Mock class that inherits from Repository."""
    def __init__(self, *args, **kwargs):
        self._requester = None
        self._headers = {}
        self._attributes = kwargs.get('attributes', {})
        self._completed = True
        self._full_name = self._attributes.get('full_name')

    @property
    def full_name(self):
        """Get repository full name."""
        return self._full_name

class MockNamedUser(NamedUser):
    """Mock class that inherits from NamedUser."""
    def __init__(self, *args, **kwargs):
        self._requester = None
        self._headers = {}
        self._attributes = kwargs.get('attributes', {})
        self._completed = True

class MockIssue(Issue):
    """Mock class that inherits from Issue."""
    def __init__(self, *args, **kwargs):
        self._requester = None
        self._headers = {}
        self._attributes = kwargs.get('attributes', {})
        self._completed = True

class MockLabel(Label):
    """Mock class that inherits from Label."""
    def __init__(self, *args, **kwargs):
        self._requester = None
        self._headers = {}
        self._attributes = kwargs.get('attributes', {})
        self._completed = True

class MockMilestone(Milestone):
    """Mock class that inherits from Milestone."""
    def __init__(self, *args, **kwargs):
        self._requester = None
        self._headers = {}
        self._attributes = kwargs.get('attributes', {})
        self._completed = True

class MockIssueComment(IssueComment):
    """Mock class that inherits from IssueComment."""
    def __init__(self, *args, **kwargs):
        self._requester = None
        self._headers = {}
        self._attributes = kwargs.get('attributes', {})
        self._completed = True


@pytest.fixture(scope="function", autouse=True)
def mock_environment(monkeypatch):
    """Set up test environment with mock token."""
    monkeypatch.setenv("GITHUB_PERSONAL_ACCESS_TOKEN", "test-token")
    yield


@pytest.fixture(scope="function")
def mock_auth(monkeypatch):
    """Mock Github Auth.Token while preserving module structure."""
    # Create a dummy token instance that passes isinstance(auth, Auth.Auth)
    mock_token_instance = Mock(spec=Auth.Auth, name="mock_auth_token")
    
    # Create a Token factory that returns this dummy token instance
    token_factory_mock = Mock(return_value=mock_token_instance)
    
    # Create a dummy module to replace Auth in our module under test
    mock_auth_module = type("MockAuthModule", (), {})()
    mock_auth_module.Token = token_factory_mock
    
    # Patch the Auth in the module under test
    monkeypatch.setattr("pygithub_mcp_server.common.github.Auth", mock_auth_module)
    
    return mock_auth_module


@pytest.fixture(scope="function", autouse=True)
def reset_github_client():
    """Reset GitHubClient singleton between tests."""
    GitHubClient._instance = None
    GitHubClient._github = None
    GitHubClient._created_via_get_instance = False
    yield
    GitHubClient._instance = None
    GitHubClient._github = None
    GitHubClient._created_via_get_instance = False


@pytest.fixture(scope="function")
def mock_github_class(monkeypatch):
    """Mock Github class in the module under test."""
    mock = Mock(wraps=MockGithub)
    mock_instance = MockGithub()
    mock.return_value = mock_instance
    mock_instance.get_repo = Mock(return_value=None)  # Can be overridden in tests

    # Patch Github in the module under test
    monkeypatch.setattr("pygithub_mcp_server.common.github.Github", mock)
    return mock


@pytest.fixture(scope="function")
def mock_github_exception():
    """Create a mock GithubException factory."""
    def _create_exception(status, data=None, headers=None):
        exc = GithubException(status, data or {})
        if headers:
            exc.headers = headers
        return exc
    return _create_exception


@pytest.fixture(scope="function")
def mock_datetime():
    """Create a fixed datetime for testing."""
    return datetime(2025, 2, 22, 12, 0)


@pytest.fixture(scope="function")
def mock_user():
    """Create a mock GitHub user."""
    user = MockNamedUser(attributes={
        "login": "testuser",
        "id": 12345,
        "type": "User",
        "site_admin": False
    })
    return user


@pytest.fixture(scope="function")
def mock_repo(mock_user):
    """Create a mock GitHub repository."""
    repo = MockRepository(attributes={
        "full_name": "owner/repo",
        "name": "repo"
    })
    
    # Mock the owner
    owner = MockNamedUser(attributes={"login": "owner"})
    type(repo).owner = PropertyMock(return_value=owner)
    
    return repo


@pytest.fixture(scope="function")
def mock_label():
    """Create a mock GitHub label."""
    label = MockLabel(attributes={
        "id": 98765,
        "name": "bug",
        "description": "Bug report",
        "color": "ff0000"
    })
    return label


@pytest.fixture(scope="function")
def mock_milestone(mock_datetime):
    """Create a mock GitHub milestone."""
    milestone = MockMilestone(attributes={
        "id": 54321,
        "number": 1,
        "title": "v1.0",
        "description": "First release",
        "state": "open",
        "created_at": mock_datetime,
        "updated_at": mock_datetime,
        "due_on": mock_datetime
    })
    return milestone


@pytest.fixture(scope="function")
def mock_issue(mock_user, mock_label, mock_milestone, mock_repo, mock_datetime):
    """Create a mock GitHub issue."""
    issue = MockIssue(attributes={
        "id": 11111,
        "number": 42,
        "title": "Test Issue",
        "body": "Issue description",
        "state": "open",
        "state_reason": None,
        "locked": False,
        "active_lock_reason": None,
        "comments": 2,
        "created_at": mock_datetime,
        "updated_at": mock_datetime,
        "closed_at": None,
        "author_association": "OWNER",
        "user": mock_user,
        "assignee": mock_user,
        "assignees": [mock_user],
        "milestone": mock_milestone,
        "labels": [mock_label],
        "url": "https://api.github.com/repos/owner/repo/issues/42",
        "html_url": "https://github.com/owner/repo/issues/42",
        "repository": mock_repo
    })
    return issue


@pytest.fixture(scope="function")
def mock_comment(mock_user, mock_datetime):
    """Create a mock GitHub issue comment."""
    comment = MockIssueComment(attributes={
        "id": 22222,
        "body": "Test comment",
        "user": mock_user,
        "created_at": mock_datetime,
        "updated_at": mock_datetime,
        "url": "https://api.github.com/repos/owner/repo/issues/comments/22222",
        "html_url": "https://github.com/owner/repo/issues/42#issuecomment-22222"
    })
    return comment


@pytest.fixture(scope="function")
def github_token():
    """Get the mock token value."""
    return "test-token"
