"""Shared test configuration and fixtures.

This module provides shared pytest fixtures and configuration for testing
the PyGithub MCP Server.
"""

import os
import pytest
from datetime import datetime
from unittest.mock import Mock, PropertyMock

from github import Github, GithubException
from github.Issue import Issue
from github.IssueComment import IssueComment
from github.Label import Label
from github.Milestone import Milestone
from github.NamedUser import NamedUser
from github.Repository import Repository

from pygithub_mcp_server.common.github import GitHubClient


@pytest.fixture(autouse=True)
def reset_github_client():
    """Reset GitHubClient singleton between tests."""
    # Store original state
    original_instance = GitHubClient._instance
    original_github = GitHubClient._github
    
    yield
    
    # Restore original state
    GitHubClient._instance = original_instance
    GitHubClient._github = original_github


@pytest.fixture
def mock_github_exception():
    """Create a mock GithubException factory."""
    def _create_exception(status, data=None, headers=None):
        exc = GithubException(status, data or {})
        if headers:
            exc.headers = headers
        return exc
    return _create_exception


@pytest.fixture
def mock_datetime():
    """Create a fixed datetime for testing."""
    return datetime(2025, 2, 22, 12, 0)


@pytest.fixture
def mock_user():
    """Create a mock GitHub user."""
    user = Mock(spec=NamedUser)
    user.login = "testuser"
    user.id = 12345
    user.type = "User"
    user.site_admin = False
    return user


@pytest.fixture
def mock_repo(mock_user):
    """Create a mock GitHub repository."""
    repo = Mock(spec=Repository)
    repo.full_name = "owner/repo"
    repo.name = "repo"
    
    # Mock the owner
    owner = Mock(spec=NamedUser)
    owner.login = "owner"
    type(repo).owner = PropertyMock(return_value=owner)
    
    return repo


@pytest.fixture
def mock_label():
    """Create a mock GitHub label."""
    label = Mock(spec=Label)
    label.id = 98765
    label.name = "bug"
    label.description = "Bug report"
    label.color = "ff0000"
    return label


@pytest.fixture
def mock_milestone(mock_datetime):
    """Create a mock GitHub milestone."""
    milestone = Mock(spec=Milestone)
    milestone.id = 54321
    milestone.number = 1
    milestone.title = "v1.0"
    milestone.description = "First release"
    milestone.state = "open"
    milestone.created_at = mock_datetime
    milestone.updated_at = mock_datetime
    milestone.due_on = mock_datetime
    return milestone


@pytest.fixture
def mock_issue(mock_user, mock_label, mock_milestone, mock_repo, mock_datetime):
    """Create a mock GitHub issue."""
    issue = Mock(spec=Issue)
    issue.id = 11111
    issue.number = 42
    issue.title = "Test Issue"
    issue.body = "Issue description"
    issue.state = "open"
    issue.state_reason = None
    issue.locked = False
    issue.active_lock_reason = None
    issue.comments = 2
    issue.created_at = mock_datetime
    issue.updated_at = mock_datetime
    issue.closed_at = None
    issue.author_association = "OWNER"
    issue.user = mock_user
    issue.assignee = mock_user
    issue.assignees = [mock_user]
    issue.milestone = mock_milestone
    issue.labels = [mock_label]
    issue.url = "https://api.github.com/repos/owner/repo/issues/42"
    issue.html_url = "https://github.com/owner/repo/issues/42"
    issue.repository = mock_repo
    return issue


@pytest.fixture
def mock_comment(mock_user, mock_datetime):
    """Create a mock GitHub issue comment."""
    comment = Mock(spec=IssueComment)
    comment.id = 22222
    comment.body = "Test comment"
    comment.user = mock_user
    comment.created_at = mock_datetime
    comment.updated_at = mock_datetime
    comment.url = "https://api.github.com/repos/owner/repo/issues/comments/22222"
    comment.html_url = "https://github.com/owner/repo/issues/42#issuecomment-22222"
    return comment


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
