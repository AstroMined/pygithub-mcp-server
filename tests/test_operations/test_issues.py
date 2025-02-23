"""Tests for GitHub issue operations.

This module tests the issue operations in operations/issues.py, focusing on
parameter validation, kwargs building, and pagination handling.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch

from github import GithubException
from github.PaginatedList import PaginatedList

from pygithub_mcp_server.operations.issues import (
    create_issue,
    get_issue,
    update_issue,
    list_issues,
    add_issue_comment,
    list_issue_comments,
    update_issue_comment,
    delete_issue_comment,
    add_issue_labels,
    remove_issue_label,
)
from pygithub_mcp_server.common.errors import GitHubError


@pytest.fixture
def mock_github_instance(mock_repo):
    """Create a mock GitHubClient instance."""
    mock_instance = Mock()
    mock_instance.get_repo.return_value = mock_repo
    return mock_instance

@pytest.fixture
def mock_github_get_instance(monkeypatch, mock_github_instance):
    """Mock GitHubClient.get_instance to return our mock."""
    mock_get_instance = Mock(return_value=mock_github_instance)
    monkeypatch.setattr(
        "pygithub_mcp_server.common.github.GitHubClient.get_instance",
        mock_get_instance
    )
    return mock_get_instance

def test_create_issue_required_params(mock_github_get_instance, mock_repo, mock_issue):
    """Test create_issue with only required parameters."""
    # Setup mock
    mock_repo.create_issue.return_value = mock_issue

    # Test
    result = create_issue("owner", "repo", "Test Issue")

    # Verify
    mock_repo.create_issue.assert_called_once_with(title="Test Issue")
    assert result["title"] == "Test Issue"
    assert result["number"] == mock_issue.number


def test_create_issue_all_params(mock_github_get_instance, mock_repo, mock_issue, mock_milestone):
    """Test create_issue with all parameters."""
    # Setup mock
    mock_repo.create_issue.return_value = mock_issue
    mock_repo.get_milestone.return_value = mock_milestone

    # Test
    result = create_issue(
        owner="owner",
        repo="repo",
        title="Test Issue",
        body="Description",
        assignees=["user1"],
        labels=["bug"],
        milestone=1
    )

    # Verify
    mock_repo.get_milestone.assert_called_once_with(1)
    mock_repo.create_issue.assert_called_once_with(
        title="Test Issue",
        body="Description",
        assignees=["user1"],
        labels=["bug"],
        milestone=mock_milestone
    )
    assert result["title"] == "Test Issue"


def test_create_issue_invalid_milestone(mock_github_get_instance, mock_repo):
    """Test create_issue with invalid milestone."""
    # Setup mock
    mock_repo.get_milestone.side_effect = GithubException(404, {"message": "Not Found"})

    # Test
    with pytest.raises(GitHubError) as exc:
        create_issue(
            owner="owner",
            repo="repo",
            title="Test Issue",
            milestone=999
        )
    assert "Invalid milestone" in str(exc.value)


def test_update_issue_no_changes(mock_github_get_instance, mock_repo, mock_issue):
    """Test update_issue with no changes."""
    # Setup mock
    mock_repo.get_issue.return_value = mock_issue

    # Test
    result = update_issue("owner", "repo", 42)

    # Verify
    mock_issue.edit.assert_not_called()
    assert result["number"] == 42


def test_update_issue_all_fields(mock_github_get_instance, mock_repo, mock_issue, mock_milestone):
    """Test update_issue with all fields."""
    # Setup mock
    mock_repo.get_issue.return_value = mock_issue
    mock_repo.get_milestone.return_value = mock_milestone

    # Test
    result = update_issue(
        owner="owner",
        repo="repo",
        issue_number=42,
        title="Updated Title",
        body="Updated Body",
        state="closed",
        labels=["bug", "urgent"],
        assignees=["user1", "user2"],
        milestone=1
    )

    # Verify
    mock_repo.get_milestone.assert_called_once_with(1)
    mock_issue.edit.assert_called_once_with(
        title="Updated Title",
        body="Updated Body",
        state="closed",
        labels=["bug", "urgent"],
        assignees=["user1", "user2"],
        milestone=mock_milestone
    )
    assert result["number"] == 42


def test_list_issues_pagination(mock_github_get_instance, mock_repo):
    """Test list_issues pagination handling."""
    # Create mock paginated list
    mock_paginated = Mock(spec=PaginatedList)
    mock_paginated.get_page.return_value = []
    mock_repo.get_issues.return_value = mock_paginated

    # Test with pagination
    list_issues("owner", "repo", page=2, per_page=30)

    # Verify
    mock_repo.get_issues.assert_called_once_with(state="open")
    mock_paginated.get_page.assert_called_once_with(1)  # 0-based indexing


def test_list_issues_invalid_state(mock_github_get_instance, mock_repo):
    """Test list_issues with invalid state."""
    with pytest.raises(GitHubError) as exc:
        list_issues("owner", "repo", state="invalid")
    assert "Invalid state" in str(exc.value)


def test_list_issues_invalid_sort(mock_github_get_instance, mock_repo):
    """Test list_issues with invalid sort."""
    with pytest.raises(GitHubError) as exc:
        list_issues("owner", "repo", sort="invalid")
    assert "Invalid sort" in str(exc.value)


def test_add_issue_comment(mock_github_get_instance, mock_repo, mock_issue, mock_comment):
    """Test add_issue_comment."""
    # Setup mock
    mock_repo.get_issue.return_value = mock_issue
    mock_issue.create_comment.return_value = mock_comment

    # Test
    result = add_issue_comment("owner", "repo", 42, "Test comment")

    # Verify
    mock_issue.create_comment.assert_called_once_with("Test comment")
    assert result["id"] == mock_comment.id
    assert result["body"] == mock_comment.body


def test_list_issue_comments_pagination(mock_github_get_instance, mock_repo, mock_issue):
    """Test list_issue_comments pagination."""
    # Setup mock
    mock_repo.get_issue.return_value = mock_issue
    
    # Create mock paginated list
    mock_paginated = Mock(spec=PaginatedList)
    mock_paginated.get_page.return_value = []
    mock_issue.get_comments.return_value = mock_paginated

    # Test with pagination
    list_issue_comments(
        "owner", "repo", 42,
        since=datetime(2025, 2, 22),
        page=2,
        per_page=30
    )

    # Verify
    mock_issue.get_comments.assert_called_once_with(since=datetime(2025, 2, 22))
    mock_paginated.get_page.assert_called_once_with(1)  # 0-based indexing


def test_update_issue_comment(mock_github_get_instance, mock_repo, mock_issue, mock_comment):
    """Test update_issue_comment."""
    # Setup mock
    mock_repo.get_issue.return_value = mock_issue
    mock_issue.get_comment.return_value = mock_comment

    # Test
    result = update_issue_comment("owner", "repo", 42, 123, "Updated comment")

    # Verify
    mock_issue.get_comment.assert_called_once_with(123)
    mock_comment.edit.assert_called_once_with("Updated comment")
    assert result["id"] == mock_comment.id


def test_delete_issue_comment(mock_github_get_instance, mock_repo, mock_issue, mock_comment):
    """Test delete_issue_comment."""
    # Setup mock
    mock_repo.get_issue.return_value = mock_issue
    mock_issue.get_comment.return_value = mock_comment

    # Test
    delete_issue_comment("owner", "repo", 42, 123)

    # Verify
    mock_issue.get_comment.assert_called_once_with(123)
    mock_comment.delete.assert_called_once()


def test_add_issue_labels(mock_github_get_instance, mock_repo, mock_issue, mock_label):
    """Test add_issue_labels."""
    # Setup mock
    mock_repo.get_issue.return_value = mock_issue
    mock_issue.labels = [mock_label]

    # Test
    result = add_issue_labels("owner", "repo", 42, ["bug", "feature"])

    # Verify
    mock_issue.add_to_labels.assert_called_once_with("bug", "feature")
    assert len(result) == 1
    assert result[0]["name"] == mock_label.name


def test_remove_issue_label(mock_github_get_instance, mock_repo, mock_issue):
    """Test remove_issue_label."""
    # Setup mock
    mock_repo.get_issue.return_value = mock_issue

    # Test
    remove_issue_label("owner", "repo", 42, "bug")

    # Verify
    mock_issue.remove_from_labels.assert_called_once_with("bug")
