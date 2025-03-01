"""Tests for PyGithub object converters.

This module tests the conversion utilities in common/converters.py that transform
PyGithub objects into our schema representations.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, PropertyMock

from github.Issue import Issue
from github.IssueComment import IssueComment
from github.Label import Label
from github.Milestone import Milestone
from github.NamedUser import NamedUser
from github.Repository import Repository

from pygithub_mcp_server.converters import (
    convert_user,
    convert_label,
    convert_milestone,
    convert_issue,
    convert_issue_comment,
    convert_datetime,
)


@pytest.fixture(scope="function")
def mock_user():
    """Create a mock NamedUser."""
    user = Mock(spec=NamedUser)
    user.login = "testuser"
    user.id = 12345
    user.type = "User"
    user.site_admin = False
    return user


@pytest.fixture(scope="function")
def mock_label():
    """Create a mock Label."""
    label = Mock(spec=Label)
    label.id = 98765
    label.name = "bug"
    label.description = "Bug report"
    label.color = "ff0000"
    return label


@pytest.fixture(scope="function")
def mock_milestone():
    """Create a mock Milestone."""
    milestone = Mock(spec=Milestone)
    milestone.id = 54321
    milestone.number = 1
    milestone.title = "v1.0"
    milestone.description = "First release"
    milestone.state = "open"
    milestone.created_at = datetime(2025, 2, 22, 12, 0)
    milestone.updated_at = datetime(2025, 2, 22, 13, 0)
    milestone.due_on = datetime(2025, 3, 1)
    return milestone


@pytest.fixture(scope="function")
def mock_repository():
    """Create a mock Repository."""
    repo = Mock(spec=Repository)
    repo.full_name = "owner/repo"
    repo.name = "repo"
    
    # Mock the owner
    owner = Mock(spec=NamedUser)
    owner.login = "owner"
    type(repo).owner = PropertyMock(return_value=owner)
    
    return repo


@pytest.fixture(scope="function")
def mock_issue(mock_user, mock_label, mock_milestone, mock_repository):
    """Create a mock Issue."""
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
    issue.created_at = datetime(2025, 2, 22, 14, 0)
    issue.updated_at = datetime(2025, 2, 22, 15, 0)
    issue.closed_at = None
    issue.author_association = "OWNER"
    issue.user = mock_user
    issue.assignee = mock_user
    issue.assignees = [mock_user]
    issue.milestone = mock_milestone
    issue.labels = [mock_label]
    issue.url = "https://api.github.com/repos/owner/repo/issues/42"
    issue.html_url = "https://github.com/owner/repo/issues/42"
    issue.repository = mock_repository
    return issue


@pytest.fixture(scope="function")
def mock_comment(mock_user):
    """Create a mock IssueComment."""
    comment = Mock(spec=IssueComment)
    comment.id = 22222
    comment.body = "Test comment"
    comment.user = mock_user
    comment.created_at = datetime(2025, 2, 22, 16, 0)
    comment.updated_at = datetime(2025, 2, 22, 17, 0)
    comment.url = "https://api.github.com/repos/owner/repo/issues/comments/22222"
    comment.html_url = "https://github.com/owner/repo/issues/42#issuecomment-22222"
    return comment


def test_convert_user(mock_user):
    """Test user conversion."""
    result = convert_user(mock_user)
    assert result == {
        "login": "testuser",
        "id": 12345,
        "type": "User",
        "site_admin": False
    }


def test_convert_user_none():
    """Test user conversion with None input."""
    assert convert_user(None) is None


def test_convert_label(mock_label):
    """Test label conversion."""
    result = convert_label(mock_label)
    assert result == {
        "id": 98765,
        "name": "bug",
        "description": "Bug report",
        "color": "ff0000"
    }


def test_convert_milestone(mock_milestone):
    """Test milestone conversion."""
    result = convert_milestone(mock_milestone)
    assert result == {
        "id": 54321,
        "number": 1,
        "title": "v1.0",
        "description": "First release",
        "state": "open",
        "created_at": "2025-02-22T12:00:00",
        "updated_at": "2025-02-22T13:00:00",
        "due_on": "2025-03-01T00:00:00"
    }


def test_convert_milestone_none():
    """Test milestone conversion with None input."""
    assert convert_milestone(None) is None


def test_convert_milestone_without_dates(mock_milestone):
    """Test milestone conversion with missing dates."""
    mock_milestone.created_at = None
    mock_milestone.updated_at = None
    mock_milestone.due_on = None
    
    result = convert_milestone(mock_milestone)
    assert result["created_at"] is None
    assert result["updated_at"] is None
    assert result["due_on"] is None


def test_convert_issue(mock_issue):
    """Test issue conversion."""
    result = convert_issue(mock_issue)
    assert result["id"] == 11111
    assert result["issue_number"] == 42
    assert result["title"] == "Test Issue"
    assert result["body"] == "Issue description"
    assert result["state"] == "open"
    assert result["comments"] == 2
    assert result["created_at"] == "2025-02-22T14:00:00"
    assert result["repository"]["full_name"] == "owner/repo"
    assert len(result["labels"]) == 1
    assert len(result["assignees"]) == 1


def test_convert_issue_comment(mock_comment):
    """Test comment conversion."""
    result = convert_issue_comment(mock_comment)
    assert result == {
        "id": 22222,
        "body": "Test comment",
        "user": {
            "login": "testuser",
            "id": 12345,
            "type": "User",
            "site_admin": False
        },
        "created_at": "2025-02-22T16:00:00",
        "updated_at": "2025-02-22T17:00:00",
        "url": "https://api.github.com/repos/owner/repo/issues/comments/22222",
        "html_url": "https://github.com/owner/repo/issues/42#issuecomment-22222"
    }


def test_convert_datetime():
    """Test datetime conversion."""
    dt = datetime(2025, 2, 22, 18, 0)
    assert convert_datetime(dt) == "2025-02-22T18:00:00"
    assert convert_datetime(None) is None


def test_convert_issue_minimal(mock_issue):
    """Test issue conversion with minimal data."""
    # Remove optional attributes
    mock_issue.body = None
    mock_issue.state_reason = None
    mock_issue.assignee = None
    mock_issue.assignees = []
    mock_issue.milestone = None
    mock_issue.labels = []
    mock_issue.closed_at = None
    
    result = convert_issue(mock_issue)
    assert result["body"] is None
    assert result["state_reason"] is None
    assert result["assignee"] is None
    assert result["assignees"] == []
    assert result["milestone"] is None
    assert result["labels"] == []
    assert result["closed_at"] is None


def test_convert_issue_comment_minimal(mock_comment):
    """Test comment conversion with minimal data."""
    mock_comment.updated_at = None
    
    result = convert_issue_comment(mock_comment)
    assert result["updated_at"] is None
