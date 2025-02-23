"""Tests for GitHub issue operations.

This module tests the issue operations in operations/issues.py, focusing on
parameter validation, kwargs building, and pagination handling.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch, PropertyMock

from github import GithubException, RateLimitExceededException
from github.PaginatedList import PaginatedList
from github.Rate import Rate
from github.RateLimit import RateLimit

from pygithub_mcp_server.common.github import GitHubClient
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
    mock_instance._handle_github_exception = GitHubClient._handle_github_exception.__get__(mock_instance)
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

@pytest.fixture
def mock_repo():
    """Create a mock Repository."""
    mock = Mock()
    mock.full_name = "owner/repo"
    return mock

@pytest.fixture
def mock_comment():
    """Create a mock IssueComment."""
    mock = Mock()
    mock.id = 123
    mock.body = "Test comment"
    mock.user = Mock()
    mock.user.login = "test-user"
    mock.user.id = 456
    mock.created_at = datetime(2025, 2, 23, 2, 0, 0)
    mock.updated_at = datetime(2025, 2, 23, 2, 0, 0)
    
    # Ensure edit updates the state and returns self
    def edit(body):
        mock.body = body
        mock.updated_at = datetime.now()
        return mock
    mock.edit.side_effect = edit
    
    # Add to_dict method for consistent conversion
    def to_dict():
        return {
            "id": mock.id,
            "body": mock.body,
            "user": {
                "login": mock.user.login,
                "id": mock.user.id
            },
            "created_at": mock.created_at.isoformat(),
            "updated_at": mock.updated_at.isoformat()
        }
    mock.to_dict = to_dict
    
    return mock

@pytest.fixture
def mock_label():
    """Create a mock Label."""
    mock = Mock()
    mock.name = "bug"
    mock.color = "fc2929"  # GitHub's default red color
    mock.description = "Something isn't working"
    mock.url = "https://api.github.com/repos/owner/repo/labels/bug"
    
    # Add to_dict method for consistent conversion
    def to_dict():
        return {
            "name": mock.name,
            "color": mock.color,
            "description": mock.description,
            "url": mock.url
        }
    mock.to_dict = to_dict
    
    return mock

@pytest.fixture
def mock_milestone():
    """Create a mock Milestone."""
    mock = Mock()
    mock.number = 1
    mock.title = "v1.0"
    mock.state = "open"
    mock.description = "First major release"
    mock.creator = Mock()
    mock.creator.login = "test-user"
    mock.creator.id = 456
    mock.due_on = datetime(2025, 12, 31)
    mock.created_at = datetime(2025, 2, 23, 2, 0, 0)
    mock.updated_at = datetime(2025, 2, 23, 2, 0, 0)
    
    # Add to_dict method for consistent conversion
    def to_dict():
        return {
            "number": mock.number,
            "title": mock.title,
            "state": mock.state,
            "description": mock.description,
            "creator": {
                "login": mock.creator.login,
                "id": mock.creator.id
            },
            "due_on": mock.due_on.isoformat() if mock.due_on else None,
            "created_at": mock.created_at.isoformat(),
            "updated_at": mock.updated_at.isoformat()
        }
    mock.to_dict = to_dict
    
    return mock

@pytest.fixture
def mock_rate_limit():
    """Create a mock Rate instance for rate limit testing."""
    mock_rate = Mock(spec=Rate)
    mock_rate.remaining = 0
    mock_rate.limit = 5000
    mock_rate.reset = datetime(2025, 2, 23, 3, 0, 0)  # Reset in 1 hour
    
    # Create RateLimitExceededException with the Rate mock
    data = {
        "message": "API rate limit exceeded",
        "documentation_url": "https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting"
    }
    exc = RateLimitExceededException(mock_rate, data)
    exc.rate = mock_rate  # PyGithub sets this attribute
    return exc

@pytest.fixture
def mock_paginated_empty():
    """Create a mock PaginatedList that returns empty results."""
    mock = Mock(spec=PaginatedList)
    mock.totalCount = 0
    mock.get_page.return_value = []
    # Make the mock iterable
    mock.__iter__ = lambda self: iter([])
    mock.__getitem__ = lambda self, key: []
    return mock

@pytest.fixture
def mock_paginated_full():
    """Create a mock PaginatedList with 100+ items."""
    mock = Mock(spec=PaginatedList)
    mock.totalCount = 150
    
    # Create mock issues
    mock_issues = [Mock(number=i) for i in range(1, 151)]
    
    # Return different items for different pages
    def get_page(page):
        start = page * 30
        end = start + 30
        return mock_issues[start:end] if start < len(mock_issues) else []
    
    # Make the mock iterable and subscriptable
    mock.get_page.side_effect = get_page
    mock.__iter__ = lambda self: iter(mock_issues)
    mock.__getitem__ = lambda self, key: mock_issues[key] if isinstance(key, int) else mock_issues[key.start:key.stop]
    return mock

@pytest.fixture
def mock_user():
    """Create a mock User."""
    def create(login):
        user = Mock()
        user.login = login
        user.id = hash(login)  # Unique ID based on login
        return user
    return create

@pytest.fixture
def mock_issue(mock_user):
    """Create a mock Issue with proper attribute initialization."""
    mock = Mock()
    mock.number = 42
    mock.title = "Test Issue"
    mock.state = "open"
    mock.body = "Test body"
    mock.labels = []
    mock.assignees = []
    mock.milestone = None
    mock.id = 12345
    
    # Ensure edit updates the state and returns self
    def edit(**kwargs):
        for key, value in kwargs.items():
            if key == "assignees":
                mock.assignees = [mock_user(login) for login in value]
            elif key == "labels":
                # Convert label strings to mock Label objects
                mock.labels = [Mock(name=label) for label in value]
            else:
                setattr(mock, key, value)
        return mock
    mock.edit.side_effect = edit
    
    # Add to_dict method for consistent conversion
    def to_dict():
        return {
            "id": mock.id,
            "number": mock.number,
            "title": mock.title,
            "state": mock.state,
            "body": mock.body,
            "labels": [{"name": label.name} for label in mock.labels],
            "assignees": [{"login": assignee.login, "id": assignee.id} for assignee in mock.assignees],
            "milestone": {"number": mock.milestone.number} if mock.milestone else None
        }
    mock.to_dict = to_dict
    
    return mock

@pytest.fixture
def mock_paginated_full():
    """Create a mock PaginatedList with 100+ items."""
    mock = Mock(spec=PaginatedList)
    mock.totalCount = 150
    
    # Create mock issues
    mock_issues = []
    for i in range(1, 151):
        issue = Mock()
        issue.number = i
        issue.title = f"Issue {i}"
        issue.state = "open"
        issue.body = f"Body {i}"
        issue.labels = []
        issue.assignees = []
        issue.milestone = None
        mock_issues.append(issue)
    
    # Return different items for different pages
    def get_page(page):
        start = page * 30
        end = start + 30
        return mock_issues[start:end] if start < len(mock_issues) else []
    
    # Make the mock iterable and subscriptable
    mock.get_page.side_effect = get_page
    mock.__iter__ = lambda self: iter(mock_issues)
    mock.__getitem__ = lambda self, key: mock_issues[key] if isinstance(key, int) else mock_issues[key.start:key.stop]
    
    return mock

@pytest.fixture
def network_error():
    """Create a GithubException that simulates a network error."""
    return GithubException(503, {"message": "Service temporarily unavailable"})

@pytest.fixture
def permission_error():
    """Create a GithubException that simulates a permission error."""
    return GithubException(403, {"message": "Resource not accessible by integration"})

@pytest.fixture
def not_found_error():
    """Create a GithubException that simulates a not found error."""
    return GithubException(404, {"message": "Not Found"})

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

# Parameter Validation Tests

@pytest.mark.parametrize("invalid_labels", [
    "not_a_list",
    [1, 2, 3],  # non-string elements
    [{"name": "label"}],  # complex objects
])
def test_list_issues_invalid_labels(mock_github_get_instance, mock_repo, invalid_labels):
    """Test list_issues with invalid label types."""
    with pytest.raises(GitHubError) as exc:
        list_issues("owner", "repo", labels=invalid_labels)
    assert "Labels must be" in str(exc.value)

@pytest.mark.parametrize("invalid_direction", ["up", "down", "forward"])
def test_list_issues_invalid_direction(mock_github_get_instance, mock_repo, invalid_direction):
    """Test list_issues with invalid direction."""
    with pytest.raises(GitHubError) as exc:
        list_issues("owner", "repo", direction=invalid_direction)
    assert "Invalid direction" in str(exc.value)

@pytest.mark.parametrize("invalid_page", [-1, 0, "1", 1.5])
def test_list_issues_invalid_page(mock_github_get_instance, mock_repo, invalid_page):
    """Test list_issues with invalid page numbers."""
    with pytest.raises(GitHubError) as exc:
        list_issues("owner", "repo", page=invalid_page)
    assert "Invalid page" in str(exc.value)

# Error Handling Tests

def test_list_issues_rate_limit(mock_github_get_instance, mock_repo, mock_rate_limit):
    """Test list_issues with rate limit exceeded."""
    mock_repo.get_issues.side_effect = mock_rate_limit
    
    with pytest.raises(GitHubError) as exc:
        list_issues("owner", "repo")
    assert "API rate limit exceeded" in str(exc.value)
    assert "Reset at" in str(exc.value)

def test_list_issues_network_error(mock_github_get_instance, mock_repo, network_error):
    """Test list_issues with network error."""
    mock_repo.get_issues.side_effect = network_error
    
    with pytest.raises(GitHubError) as exc:
        list_issues("owner", "repo")
    assert "Service temporarily unavailable" in str(exc.value)

def test_list_issues_permission_error(mock_github_get_instance, mock_repo, permission_error):
    """Test list_issues with permission error."""
    mock_repo.get_issues.side_effect = permission_error
    
    with pytest.raises(GitHubError) as exc:
        list_issues("owner", "repo")
    assert "Resource not accessible" in str(exc.value)

def test_get_issue_not_found(mock_github_get_instance, mock_repo, not_found_error):
    """Test get_issue with non-existent issue."""
    mock_repo.get_issue.side_effect = not_found_error
    
    with pytest.raises(GitHubError) as exc:
        get_issue("owner", "repo", 999)
    assert "Not Found" in str(exc.value)

# Pagination Tests

def test_list_issues_empty_results(mock_github_get_instance, mock_repo, mock_paginated_empty):
    """Test list_issues with no results."""
    mock_repo.get_issues.return_value = mock_paginated_empty
    
    result = list_issues("owner", "repo")
    assert len(result) == 0

def test_list_issues_full_pagination(mock_github_get_instance, mock_repo, mock_paginated_full):
    """Test list_issues with full pagination."""
    mock_repo.get_issues.return_value = mock_paginated_full
    
    # Test first page
    result = list_issues("owner", "repo", page=1, per_page=30)
    assert len(result) == 30
    assert result[0]["number"] == 1
    
    # Test second page
    result = list_issues("owner", "repo", page=2, per_page=30)
    assert len(result) == 30
    assert result[0]["number"] == 31

def test_list_issues_beyond_last_page(mock_github_get_instance, mock_repo, mock_paginated_full):
    """Test list_issues with page number beyond results."""
    mock_repo.get_issues.return_value = mock_paginated_full
    
    result = list_issues("owner", "repo", page=10)
    assert len(result) == 0

@pytest.mark.parametrize("per_page", [101, 200, 500])
def test_list_issues_per_page_limit(mock_github_get_instance, mock_repo, per_page):
    """Test list_issues with per_page exceeding limit."""
    with pytest.raises(GitHubError) as exc:
        list_issues("owner", "repo", per_page=per_page)
    assert "per_page cannot exceed 100" in str(exc.value)

# Resource Lifecycle Tests

def test_issue_lifecycle(mock_github_get_instance, mock_repo, mock_issue):
    """Test complete issue lifecycle (create → update → close)."""
    # Setup mock
    mock_repo.create_issue.return_value = mock_issue
    mock_repo.get_issue.return_value = mock_issue
    
    # Create issue
    issue = create_issue("owner", "repo", "Test Issue")
    assert issue["state"] == "open"
    
    # Update issue
    updated = update_issue("owner", "repo", issue["number"], title="Updated Title")
    assert updated["title"] == "Updated Title"
    
    # Close issue
    closed = update_issue("owner", "repo", issue["number"], state="closed")
    assert closed["state"] == "closed"

def test_comment_lifecycle(mock_github_get_instance, mock_repo, mock_issue, mock_comment):
    """Test comment lifecycle (add → update → delete)."""
    # Setup mocks
    mock_repo.get_issue.return_value = mock_issue
    mock_issue.create_comment.return_value = mock_comment
    mock_issue.get_comment.return_value = mock_comment
    
    # Add comment
    comment = add_issue_comment("owner", "repo", 42, "Initial comment")
    assert comment["body"] == mock_comment.body
    
    # Update comment
    updated = update_issue_comment("owner", "repo", 42, comment["id"], "Updated comment")
    assert updated["id"] == comment["id"]
    
    # Delete comment
    delete_issue_comment("owner", "repo", 42, comment["id"])
    mock_comment.delete.assert_called_once()

def test_label_lifecycle(mock_github_get_instance, mock_repo, mock_issue, mock_label):
    """Test label lifecycle (add → remove)."""
    # Setup mocks
    mock_repo.get_issue.return_value = mock_issue
    mock_issue.labels = [mock_label]
    
    # Add labels
    labels = add_issue_labels("owner", "repo", 42, ["bug", "feature"])
    assert len(labels) == 1
    assert labels[0]["name"] == mock_label.name
    
    # Remove label
    remove_issue_label("owner", "repo", 42, "bug")
    mock_issue.remove_from_labels.assert_called_once_with("bug")

# Additional Error Scenarios

def test_update_issue_invalid_state(mock_github_get_instance, mock_repo, mock_issue):
    """Test update_issue with invalid state."""
    mock_repo.get_issue.return_value = mock_issue
    mock_issue.edit.side_effect = GithubException(
        422, {"message": "Invalid state value"}
    )
    
    with pytest.raises(GitHubError) as exc:
        update_issue("owner", "repo", 42, state="invalid")
    assert "Invalid state value" in str(exc.value)

def test_add_issue_comment_rate_limit(mock_github_get_instance, mock_repo, mock_issue, mock_rate_limit):
    """Test add_issue_comment with rate limit exceeded."""
    mock_repo.get_issue.return_value = mock_issue
    mock_issue.create_comment.side_effect = mock_rate_limit
    
    with pytest.raises(GitHubError) as exc:
        add_issue_comment("owner", "repo", 42, "Test comment")
    assert "API rate limit exceeded" in str(exc.value)
    assert "Reset at" in str(exc.value)

def test_update_issue_comment_not_found(mock_github_get_instance, mock_repo, mock_issue, not_found_error):
    """Test update_issue_comment with non-existent comment."""
    mock_repo.get_issue.return_value = mock_issue
    mock_issue.get_comment.side_effect = not_found_error
    
    with pytest.raises(GitHubError) as exc:
        update_issue_comment("owner", "repo", 42, 999, "Updated text")
    assert "Not Found" in str(exc.value)

def test_add_issue_labels_network_error(mock_github_get_instance, mock_repo, mock_issue, network_error):
    """Test add_issue_labels with network error."""
    mock_repo.get_issue.return_value = mock_issue
    mock_issue.add_to_labels.side_effect = network_error
    
    with pytest.raises(GitHubError) as exc:
        add_issue_labels("owner", "repo", 42, ["bug"])
    assert "Service temporarily unavailable" in str(exc.value)

def test_remove_issue_label_permission_error(mock_github_get_instance, mock_repo, mock_issue, permission_error):
    """Test remove_issue_label with permission error."""
    mock_repo.get_issue.return_value = mock_issue
    mock_issue.remove_from_labels.side_effect = permission_error
    
    with pytest.raises(GitHubError) as exc:
        remove_issue_label("owner", "repo", 42, "bug")
    assert "Resource not accessible" in str(exc.value)
