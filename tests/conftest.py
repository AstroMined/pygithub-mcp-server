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
from github.PaginatedList import PaginatedList
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
        
        # Initialize all required attributes
        self._name = self._attributes.get('name')
        self._full_name = self._attributes.get('full_name')
        self._description = self._attributes.get('description')
        self._private = self._attributes.get('private', False)
        self._fork = self._attributes.get('fork', False)
        self._url = self._attributes.get('url')
        self._html_url = self._attributes.get('html_url')
        self._owner = None  # Set via property mock

    def _completeIfNotSet(self, value):
        """Mock the _completeIfNotSet method to just return the value."""
        return value

    @property
    def name(self):
        """Get repository name."""
        return self._completeIfNotSet(self._name)

    @property
    def full_name(self):
        """Get repository full name."""
        return self._completeIfNotSet(self._full_name)

    @property
    def description(self):
        """Get repository description."""
        return self._completeIfNotSet(self._description)

    @property
    def private(self):
        """Get repository private status."""
        return self._completeIfNotSet(self._private)

    @property
    def fork(self):
        """Get repository fork status."""
        return self._completeIfNotSet(self._fork)

    @property
    def url(self):
        """Get repository API URL."""
        return self._completeIfNotSet(self._url)

    @property
    def html_url(self):
        """Get repository HTML URL."""
        return self._completeIfNotSet(self._html_url)

class MockNamedUser(NamedUser):
    """Mock class that inherits from NamedUser."""
    def __init__(self, *args, **kwargs):
        self._requester = None
        self._headers = {}
        self._attributes = kwargs.get('attributes', {})
        self._completed = True
        self._login = self._attributes.get('login')
        self._id = self._attributes.get('id')
        self._type = self._attributes.get('type')
        self._site_admin = self._attributes.get('site_admin')

    def _completeIfNotSet(self, value):
        """Mock the _completeIfNotSet method to just return the value."""
        return value

    @property
    def login(self):
        """Get user login."""
        return self._completeIfNotSet(self._login)

    @property
    def id(self):
        """Get user ID."""
        return self._completeIfNotSet(self._id)

    @property
    def type(self):
        """Get user type."""
        return self._completeIfNotSet(self._type)

    @property
    def site_admin(self):
        """Get user site admin status."""
        return self._completeIfNotSet(self._site_admin)

class MockIssue(Issue):
    """Mock class that inherits from Issue."""
    def __init__(self, *args, **kwargs):
        self._requester = None
        self._headers = {}
        self._attributes = kwargs.get('attributes', {})
        self._completed = True
        self._repository = kwargs.get('repository')
        
        # Initialize all required attributes
        self._id = self._attributes.get('id')
        self._number = self._attributes.get('number')
        self._title = self._attributes.get('title')
        self._body = self._attributes.get('body')
        self._state = self._attributes.get('state')
        self._state_reason = self._attributes.get('state_reason')
        self._labels = self._attributes.get('labels', [])
        self._assignee = self._attributes.get('assignee')
        self._assignees = self._attributes.get('assignees', [])
        self._milestone = self._attributes.get('milestone')
        self._comments = self._attributes.get('comments', 0)
        self._created_at = self._attributes.get('created_at')
        self._updated_at = self._attributes.get('updated_at')
        self._closed_at = self._attributes.get('closed_at')
        self._url = self._attributes.get('url')
        self._html_url = self._attributes.get('html_url')
        self._user = self._attributes.get('user')
        self._locked = self._attributes.get('locked', False)
        self._active_lock_reason = self._attributes.get('active_lock_reason')
        self._author_association = self._attributes.get('author_association')

    def _completeIfNotSet(self, value):
        """Mock the _completeIfNotSet method to just return the value."""
        return value

    @property
    def id(self):
        """Get issue ID."""
        return self._completeIfNotSet(self._id)

    @property
    def number(self):
        """Get issue number."""
        return self._completeIfNotSet(self._number)

    @property
    def title(self):
        """Get issue title."""
        return self._completeIfNotSet(self._title)

    @property
    def body(self):
        """Get issue body."""
        return self._completeIfNotSet(self._body)

    @property
    def state(self):
        """Get issue state."""
        return self._completeIfNotSet(self._state)

    @property
    def state_reason(self):
        """Get issue state reason."""
        return self._completeIfNotSet(self._state_reason)

    @property
    def labels(self):
        """Get issue labels."""
        return self._completeIfNotSet(self._labels)

    @labels.setter
    def labels(self, value):
        """Set issue labels."""
        self._labels = value

    @property
    def assignee(self):
        """Get issue assignee."""
        return self._completeIfNotSet(self._assignee)

    @property
    def assignees(self):
        """Get issue assignees."""
        return self._completeIfNotSet(self._assignees)

    @property
    def milestone(self):
        """Get issue milestone."""
        return self._completeIfNotSet(self._milestone)

    @property
    def comments(self):
        """Get issue comments count."""
        return self._completeIfNotSet(self._comments)

    @property
    def created_at(self):
        """Get issue creation date."""
        return self._completeIfNotSet(self._created_at)

    @property
    def updated_at(self):
        """Get issue update date."""
        return self._completeIfNotSet(self._updated_at)

    @property
    def closed_at(self):
        """Get issue closure date."""
        return self._completeIfNotSet(self._closed_at)

    @property
    def url(self):
        """Get issue API URL."""
        return self._completeIfNotSet(self._url)

    @property
    def html_url(self):
        """Get issue HTML URL."""
        return self._completeIfNotSet(self._html_url)

    @property
    def user(self):
        """Get issue creator."""
        return self._completeIfNotSet(self._user)

    @property
    def locked(self):
        """Get issue locked state."""
        return self._completeIfNotSet(self._locked)

    @property
    def active_lock_reason(self):
        """Get issue lock reason."""
        return self._completeIfNotSet(self._active_lock_reason)

    @property
    def author_association(self):
        """Get author association."""
        return self._completeIfNotSet(self._author_association)

    @property
    def repository(self):
        """Get issue repository."""
        return self._completeIfNotSet(self._repository)

class MockLabel(Label):
    """Mock class that inherits from Label."""
    def __init__(self, *args, **kwargs):
        self._requester = None
        self._headers = {}
        self._attributes = kwargs.get('attributes', {})
        self._completed = True
        self._id = self._attributes.get('id')
        self._name = self._attributes.get('name')
        self._description = self._attributes.get('description')
        self._color = self._attributes.get('color')

    def _completeIfNotSet(self, value):
        """Mock the _completeIfNotSet method to just return the value."""
        return value

    @property
    def id(self):
        """Get label ID."""
        return self._completeIfNotSet(self._id)

    @property
    def name(self):
        """Get label name."""
        return self._completeIfNotSet(self._name)

    @property
    def description(self):
        """Get label description."""
        return self._completeIfNotSet(self._description)

    @property
    def color(self):
        """Get label color."""
        return self._completeIfNotSet(self._color)

class MockMilestone(Milestone):
    """Mock class that inherits from Milestone."""
    def __init__(self, *args, **kwargs):
        self._requester = None
        self._headers = {}
        self._attributes = kwargs.get('attributes', {})
        self._completed = True
        
        # Initialize all required attributes
        self._id = self._attributes.get('id')
        self._number = self._attributes.get('number')
        self._title = self._attributes.get('title')
        self._description = self._attributes.get('description')
        self._state = self._attributes.get('state')
        self._created_at = self._attributes.get('created_at')
        self._updated_at = self._attributes.get('updated_at')
        self._due_on = self._attributes.get('due_on')

    def _completeIfNotSet(self, value):
        """Mock the _completeIfNotSet method to just return the value."""
        return value

    @property
    def id(self):
        """Get milestone ID."""
        return self._completeIfNotSet(self._id)

    @property
    def number(self):
        """Get milestone number."""
        return self._completeIfNotSet(self._number)

    @property
    def title(self):
        """Get milestone title."""
        return self._completeIfNotSet(self._title)

    @property
    def description(self):
        """Get milestone description."""
        return self._completeIfNotSet(self._description)

    @property
    def state(self):
        """Get milestone state."""
        return self._completeIfNotSet(self._state)

    @property
    def created_at(self):
        """Get milestone creation date."""
        return self._completeIfNotSet(self._created_at)

    @property
    def updated_at(self):
        """Get milestone update date."""
        return self._completeIfNotSet(self._updated_at)

    @property
    def due_on(self):
        """Get milestone due date."""
        return self._completeIfNotSet(self._due_on)

class MockIssueComment(IssueComment):
    """Mock class that inherits from IssueComment."""
    def __init__(self, *args, **kwargs):
        self._requester = None
        self._headers = {}
        self._attributes = kwargs.get('attributes', {})
        self._completed = True
        self._id = self._attributes.get('id')
        self._body = self._attributes.get('body')
        self._user = self._attributes.get('user')
        self._created_at = self._attributes.get('created_at')
        self._updated_at = self._attributes.get('updated_at')
        self._url = self._attributes.get('url')
        self._html_url = self._attributes.get('html_url')

    def _completeIfNotSet(self, value):
        """Mock the _completeIfNotSet method to just return the value."""
        return value

    @property
    def id(self):
        """Get comment ID."""
        return self._completeIfNotSet(self._id)

    @property
    def body(self):
        """Get comment body."""
        return self._completeIfNotSet(self._body)

    @property
    def user(self):
        """Get comment author."""
        return self._completeIfNotSet(self._user)

    @property
    def created_at(self):
        """Get comment creation date."""
        return self._completeIfNotSet(self._created_at)

    @property
    def updated_at(self):
        """Get comment update date."""
        return self._completeIfNotSet(self._updated_at)

    @property
    def url(self):
        """Get comment API URL."""
        return self._completeIfNotSet(self._url)

    @property
    def html_url(self):
        """Get comment HTML URL."""
        return self._completeIfNotSet(self._html_url)


@pytest.fixture(scope="function", autouse=True)
def mock_environment(monkeypatch, github_token):
    """Set up test environment."""
    monkeypatch.setenv("TEST_ENVIRONMENT", "true")
    monkeypatch.setenv("GITHUB_PERSONAL_ACCESS_TOKEN", github_token)
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
    GitHubClient._initialized = False
    yield
    GitHubClient._instance = None
    GitHubClient._github = None
    GitHubClient._created_via_get_instance = False
    GitHubClient._initialized = False


@pytest.fixture(scope="function")
def mock_github_class(monkeypatch, mock_repo):
    """Mock Github class in the module under test."""
    # Create base mock with proper spec
    mock = Mock(wraps=MockGithub)
    mock_instance = MockGithub()
    mock.return_value = mock_instance
    
    # Configure instance with necessary methods
    mock_instance.get_repo = Mock(return_value=mock_repo)
    mock_instance.get_rate_limit = Mock()  # Prevents auth errors
    
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


@pytest.fixture(scope="function", autouse=True)
def configure_mock_repo(mock_repo, mock_issue, mock_milestone):
    """Configure mock repository methods after issue is created."""
    # Configure methods with proper mocking
    mock_repo.create_issue = Mock(spec=mock_repo.create_issue, return_value=mock_issue)
    mock_repo.get_issue = Mock(spec=mock_repo.get_issue, return_value=mock_issue)
    mock_repo.get_milestone = Mock(spec=mock_repo.get_milestone, return_value=mock_milestone)
    
    # Configure get_issues for pagination tests
    mock_paginated = Mock(spec=PaginatedList)
    mock_paginated.get_page = Mock(return_value=[])
    mock_repo.get_issues = Mock(return_value=mock_paginated)


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
def mock_issue(mock_user, mock_label, mock_milestone, mock_datetime, mock_repo):
    """Create a mock GitHub issue."""
    issue = MockIssue(
        repository=mock_repo,
        attributes={
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
        "html_url": "https://github.com/owner/repo/issues/42"
    })
    
    # Configure methods with proper mocking while preserving inheritance
    issue.create_comment = Mock(spec=issue.create_comment)
    issue.get_comments = Mock(spec=issue.get_comments)
    issue.get_comment = Mock(spec=issue.get_comment)
    issue.edit = Mock(spec=issue.edit)
    issue.add_to_labels = Mock(spec=issue.add_to_labels)
    issue.remove_from_labels = Mock(spec=issue.remove_from_labels)
    
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
    
    # Configure methods with proper mocking while preserving inheritance
    comment.edit = Mock(spec=comment.edit)
    comment.delete = Mock(spec=comment.delete)
    
    return comment


@pytest.fixture(scope="function")
def github_token():
    """Get the mock token value."""
    return "test-token"
