"""Tests for issue-related schema models.

This module tests the schema models used for GitHub issue operations.
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from pygithub_mcp_server.schemas.issues import (
    CreateIssueParams,
    ListIssuesParams,
    GetIssueParams,
    UpdateIssueParams,
    IssueCommentParams,
    ListIssueCommentsParams,
    UpdateIssueCommentParams,
    DeleteIssueCommentParams,
    AddIssueLabelsParams,
    RemoveIssueLabelParams,
)


class TestCreateIssueParams:
    """Tests for the CreateIssueParams schema."""

    def test_valid_data(self, valid_create_issue_data):
        """Test that valid data passes validation."""
        params = CreateIssueParams(**valid_create_issue_data)
        assert params.owner == valid_create_issue_data["owner"]
        assert params.repo == valid_create_issue_data["repo"]
        assert params.title == valid_create_issue_data["title"]
        assert params.body == valid_create_issue_data["body"]
        assert params.assignees == valid_create_issue_data["assignees"]
        assert params.labels == valid_create_issue_data["labels"]
        assert params.milestone == valid_create_issue_data["milestone"]

    def test_minimal_valid_data(self, valid_repository_ref_data):
        """Test with minimal valid data (only required fields)."""
        # Only owner, repo, and title are required
        params = CreateIssueParams(
            **valid_repository_ref_data,
            title="Found a bug"
        )
        assert params.owner == valid_repository_ref_data["owner"]
        assert params.repo == valid_repository_ref_data["repo"]
        assert params.title == "Found a bug"
        assert params.body is None
        assert params.assignees == []
        assert params.labels == []
        assert params.milestone is None

    def test_missing_required_fields(self, valid_repository_ref_data):
        """Test that missing required fields raise validation errors."""
        # Missing title
        with pytest.raises(ValidationError) as exc_info:
            CreateIssueParams(**valid_repository_ref_data)
        assert "title" in str(exc_info.value).lower()

    def test_invalid_field_types(self, valid_repository_ref_data):
        """Test that invalid field types raise validation errors."""
        # Invalid title type
        with pytest.raises(ValidationError) as exc_info:
            CreateIssueParams(
                **valid_repository_ref_data,
                title=123
            )
        assert "title" in str(exc_info.value).lower()
        
        # Invalid body type
        with pytest.raises(ValidationError) as exc_info:
            CreateIssueParams(
                **valid_repository_ref_data,
                title="Found a bug",
                body=123
            )
        assert "body" in str(exc_info.value).lower()
        
        # Invalid assignees type
        with pytest.raises(ValidationError) as exc_info:
            CreateIssueParams(
                **valid_repository_ref_data,
                title="Found a bug",
                assignees="octocat"  # Should be a list
            )
        assert "assignees" in str(exc_info.value).lower()
        
        # Invalid labels type
        with pytest.raises(ValidationError) as exc_info:
            CreateIssueParams(
                **valid_repository_ref_data,
                title="Found a bug",
                labels="bug"  # Should be a list
            )
        assert "labels" in str(exc_info.value).lower()
        
        # Invalid milestone type
        with pytest.raises(ValidationError) as exc_info:
            CreateIssueParams(
                **valid_repository_ref_data,
                title="Found a bug",
                milestone="1"  # Should be an integer
            )
        assert "milestone" in str(exc_info.value).lower()

    def test_empty_strings(self, valid_repository_ref_data):
        """Test behavior with empty strings."""
        # Empty title - should raise error
        with pytest.raises(ValidationError) as exc_info:
            CreateIssueParams(
                **valid_repository_ref_data,
                title=""
            )
        assert "title cannot be empty" in str(exc_info.value).lower()
        
        # Whitespace-only title - should raise error
        with pytest.raises(ValidationError) as exc_info:
            CreateIssueParams(
                **valid_repository_ref_data,
                title="   "
            )
        assert "title cannot be empty" in str(exc_info.value).lower()
        
        # Empty body - should be valid
        params = CreateIssueParams(
            **valid_repository_ref_data,
            title="Found a bug",
            body=""
        )
        assert params.body == ""

    def test_none_values(self, valid_repository_ref_data):
        """Test behavior with None values."""
        # None title - should raise error
        with pytest.raises(ValidationError) as exc_info:
            CreateIssueParams(
                **valid_repository_ref_data,
                title=None
            )
        assert "title" in str(exc_info.value).lower()
        
        # None body - should be valid
        params = CreateIssueParams(
            **valid_repository_ref_data,
            title="Found a bug",
            body=None
        )
        assert params.body is None
        
        # None milestone - should be valid
        params = CreateIssueParams(
            **valid_repository_ref_data,
            title="Found a bug",
            milestone=None
        )
        assert params.milestone is None

    def test_empty_lists(self, valid_repository_ref_data):
        """Test behavior with empty lists."""
        # Empty assignees - should be valid
        params = CreateIssueParams(
            **valid_repository_ref_data,
            title="Found a bug",
            assignees=[]
        )
        assert params.assignees == []
        
        # Empty labels - should be valid
        params = CreateIssueParams(
            **valid_repository_ref_data,
            title="Found a bug",
            labels=[]
        )
        assert params.labels == []

    def test_default_values(self, valid_repository_ref_data):
        """Test that default values are correctly applied."""
        params = CreateIssueParams(
            **valid_repository_ref_data,
            title="Found a bug"
        )
        assert params.assignees == []  # Default is empty list
        assert params.labels == []  # Default is empty list


class TestListIssuesParams:
    """Tests for the ListIssuesParams schema."""

    def test_valid_data(self, valid_list_issues_data):
        """Test that valid data passes validation."""
        params = ListIssuesParams(**valid_list_issues_data)
        assert params.owner == valid_list_issues_data["owner"]
        assert params.repo == valid_list_issues_data["repo"]
        assert params.state == valid_list_issues_data["state"]
        assert params.labels == valid_list_issues_data["labels"]
        assert params.sort == valid_list_issues_data["sort"]
        assert params.direction == valid_list_issues_data["direction"]
        # Check that since is a datetime object with the correct values
        assert isinstance(params.since, datetime)
        assert params.since.year == 2020
        assert params.since.month == 1
        assert params.since.day == 1
        assert params.since.hour == 0
        assert params.since.minute == 0
        assert params.since.second == 0
        assert params.page == valid_list_issues_data["page"]
        assert params.per_page == valid_list_issues_data["per_page"]

    def test_minimal_valid_data(self, valid_repository_ref_data):
        """Test with minimal valid data (only required fields)."""
        # Only owner and repo are required
        params = ListIssuesParams(**valid_repository_ref_data)
        assert params.owner == valid_repository_ref_data["owner"]
        assert params.repo == valid_repository_ref_data["repo"]
        assert params.state is None
        assert params.labels is None
        assert params.sort is None
        assert params.direction is None
        assert params.since is None
        assert params.page is None
        assert params.per_page is None

    def test_valid_state_values(self, valid_repository_ref_data):
        """Test that valid state values pass validation."""
        # Valid state values: open, closed, all
        params = ListIssuesParams(**valid_repository_ref_data, state="open")
        assert params.state == "open"
        
        params = ListIssuesParams(**valid_repository_ref_data, state="closed")
        assert params.state == "closed"
        
        params = ListIssuesParams(**valid_repository_ref_data, state="all")
        assert params.state == "all"
        
    def test_invalid_state_values(self, valid_repository_ref_data):
        """Test that invalid state values raise validation errors."""
        with pytest.raises(ValidationError) as exc_info:
            ListIssuesParams(**valid_repository_ref_data, state="invalid")
        assert "Invalid state" in str(exc_info.value)

    def test_valid_sort_values(self, valid_repository_ref_data):
        """Test that valid sort values pass validation."""
        # Valid sort values: created, updated, comments
        params = ListIssuesParams(**valid_repository_ref_data, sort="created")
        assert params.sort == "created"
        
        params = ListIssuesParams(**valid_repository_ref_data, sort="updated")
        assert params.sort == "updated"
        
        params = ListIssuesParams(**valid_repository_ref_data, sort="comments")
        assert params.sort == "comments"
        
    def test_invalid_sort_values(self, valid_repository_ref_data):
        """Test that invalid sort values raise validation errors."""
        with pytest.raises(ValidationError) as exc_info:
            ListIssuesParams(**valid_repository_ref_data, sort="invalid")
        assert "Invalid sort value" in str(exc_info.value)

    def test_valid_direction_values(self, valid_repository_ref_data):
        """Test that valid direction values pass validation."""
        # Valid direction values: asc, desc
        params = ListIssuesParams(**valid_repository_ref_data, direction="asc")
        assert params.direction == "asc"
        
        params = ListIssuesParams(**valid_repository_ref_data, direction="desc")
        assert params.direction == "desc"
        
    def test_invalid_direction_values(self, valid_repository_ref_data):
        """Test that invalid direction values raise validation errors."""
        with pytest.raises(ValidationError) as exc_info:
            ListIssuesParams(**valid_repository_ref_data, direction="invalid")
        assert "Invalid direction" in str(exc_info.value)
        
    def test_invalid_page_values(self, valid_repository_ref_data):
        """Test that invalid page values raise validation errors."""
        with pytest.raises(ValidationError) as exc_info:
            ListIssuesParams(**valid_repository_ref_data, page=0)
        assert "Page number must be a positive integer" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            ListIssuesParams(**valid_repository_ref_data, page=-1)
        assert "Page number must be a positive integer" in str(exc_info.value)
        
    def test_invalid_per_page_values(self, valid_repository_ref_data):
        """Test that invalid per_page values raise validation errors."""
        with pytest.raises(ValidationError) as exc_info:
            ListIssuesParams(**valid_repository_ref_data, per_page=0)
        assert "Results per page must be a positive integer" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            ListIssuesParams(**valid_repository_ref_data, per_page=-1)
        assert "Results per page must be a positive integer" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            ListIssuesParams(**valid_repository_ref_data, per_page=101)
        assert "Results per page cannot exceed 100" in str(exc_info.value)
        
    def test_none_per_page_value(self, valid_repository_ref_data):
        """Test that None per_page value is valid."""
        params = ListIssuesParams(**valid_repository_ref_data, per_page=None)
        assert params.per_page is None

    def test_datetime_parsing(self, valid_repository_ref_data):
        """Test that datetime strings are correctly parsed."""
        # ISO format datetime string
        params = ListIssuesParams(
            **valid_repository_ref_data,
            since="2020-01-01T00:00:00Z"
        )
        assert isinstance(params.since, datetime)
        assert params.since.year == 2020
        assert params.since.month == 1
        assert params.since.day == 1
        assert params.since.hour == 0
        assert params.since.minute == 0
        assert params.since.second == 0
        
        # Test with different ISO format
        params = ListIssuesParams(
            **valid_repository_ref_data,
            since="2020-01-01T12:30:45+00:00"
        )
        assert isinstance(params.since, datetime)
        assert params.since.year == 2020
        assert params.since.month == 1
        assert params.since.day == 1
        assert params.since.hour == 12
        assert params.since.minute == 30
        assert params.since.second == 45
        
        # Test with datetime object directly
        dt = datetime(2020, 1, 1, 0, 0, 0, tzinfo=datetime.now().astimezone().tzinfo)
        params = ListIssuesParams(
            **valid_repository_ref_data,
            since=dt
        )
        assert params.since == dt
    
    def test_invalid_datetime_format(self, valid_repository_ref_data):
        """Test behavior with invalid datetime format."""
        # Missing time component
        with pytest.raises(ValidationError) as exc_info:
            ListIssuesParams(
                **valid_repository_ref_data,
                since="2020-01-01"  # Missing time component
            )
        assert "Invalid ISO format datetime" in str(exc_info.value)
        
        # Missing timezone
        with pytest.raises(ValidationError) as exc_info:
            ListIssuesParams(
                **valid_repository_ref_data,
                since="2020-01-01T00:00:00"  # No timezone
            )
        assert "Invalid ISO format datetime" in str(exc_info.value)
        
        # Space instead of 'T'
        with pytest.raises(ValidationError) as exc_info:
            ListIssuesParams(
                **valid_repository_ref_data,
                since="2020-01-01 00:00:00Z"  # Space instead of 'T'
            )
        assert "Invalid ISO format datetime" in str(exc_info.value)
        
        # Completely invalid format
        with pytest.raises(ValidationError) as exc_info:
            ListIssuesParams(
                **valid_repository_ref_data,
                since="not-a-date"
            )
        assert "Invalid ISO format datetime" in str(exc_info.value)
        
        # Malformed but plausible ISO format (passes regex check but fails parsing)
        with pytest.raises(ValidationError) as exc_info:
            ListIssuesParams(
                **valid_repository_ref_data,
                since="2020-13-32T25:61:61Z"  # Invalid month, day, hour, minute, second
            )
        assert "Invalid ISO format datetime" in str(exc_info.value)
        assert "Contains invalid date/time components" in str(exc_info.value)


class TestGetIssueParams:
    """Tests for the GetIssueParams schema."""

    def test_valid_data(self, valid_get_issue_data):
        """Test that valid data passes validation."""
        params = GetIssueParams(**valid_get_issue_data)
        assert params.owner == valid_get_issue_data["owner"]
        assert params.repo == valid_get_issue_data["repo"]
        assert params.issue_number == valid_get_issue_data["issue_number"]

    def test_missing_required_fields(self, valid_repository_ref_data):
        """Test that missing required fields raise validation errors."""
        # Missing issue_number
        with pytest.raises(ValidationError) as exc_info:
            GetIssueParams(**valid_repository_ref_data)
        assert "issue_number" in str(exc_info.value).lower()

    def test_invalid_issue_number_type(self, valid_repository_ref_data):
        """Test that invalid issue_number type raises validation error."""
        # String instead of integer
        with pytest.raises(ValidationError) as exc_info:
            GetIssueParams(
                **valid_repository_ref_data,
                issue_number="1"  # Should be an integer
            )
        assert "issue_number" in str(exc_info.value).lower()

    def test_negative_issue_number(self, valid_repository_ref_data):
        """Test behavior with negative issue number."""
        # Negative issue number - should be valid (though not practical)
        params = GetIssueParams(
            **valid_repository_ref_data,
            issue_number=-1
        )
        assert params.issue_number == -1


class TestUpdateIssueParams:
    """Tests for the UpdateIssueParams schema."""

    def test_valid_data(self, valid_update_issue_data):
        """Test that valid data passes validation."""
        params = UpdateIssueParams(**valid_update_issue_data)
        assert params.owner == valid_update_issue_data["owner"]
        assert params.repo == valid_update_issue_data["repo"]
        assert params.issue_number == valid_update_issue_data["issue_number"]
        assert params.title == valid_update_issue_data["title"]
        assert params.body == valid_update_issue_data["body"]
        assert params.state == valid_update_issue_data["state"]
        assert params.labels == valid_update_issue_data["labels"]
        assert params.assignees == valid_update_issue_data["assignees"]
        assert params.milestone == valid_update_issue_data["milestone"]

    def test_minimal_valid_data(self, valid_repository_ref_data):
        """Test with minimal valid data (only required fields)."""
        # Only owner, repo, and issue_number are required
        params = UpdateIssueParams(
            **valid_repository_ref_data,
            issue_number=1
        )
        assert params.owner == valid_repository_ref_data["owner"]
        assert params.repo == valid_repository_ref_data["repo"]
        assert params.issue_number == 1
        assert params.title is None
        assert params.body is None
        assert params.state is None
        assert params.labels is None
        assert params.assignees is None
        assert params.milestone is None

    def test_partial_update(self, valid_repository_ref_data):
        """Test updating only some fields."""
        # Update only title and state
        params = UpdateIssueParams(
            **valid_repository_ref_data,
            issue_number=1,
            title="Updated bug report",
            state="closed"
        )
        assert params.title == "Updated bug report"
        assert params.state == "closed"
        assert params.body is None
        assert params.labels is None
        assert params.assignees is None
        assert params.milestone is None

    def test_valid_state_values(self, valid_repository_ref_data):
        """Test that valid state values pass validation."""
        # Valid state values: open, closed
        params = UpdateIssueParams(
            **valid_repository_ref_data,
            issue_number=1,
            state="open"
        )
        assert params.state == "open"
        
        params = UpdateIssueParams(
            **valid_repository_ref_data,
            issue_number=1,
            state="closed"
        )
        assert params.state == "closed"
        
    def test_invalid_state_values(self, valid_repository_ref_data):
        """Test that invalid state values raise validation errors."""
        # 'all' is not valid for UpdateIssueParams
        with pytest.raises(ValidationError) as exc_info:
            UpdateIssueParams(
                **valid_repository_ref_data,
                issue_number=1,
                state="all"
            )
        assert "Invalid state" in str(exc_info.value)
        
        # Other invalid values
        with pytest.raises(ValidationError) as exc_info:
            UpdateIssueParams(
                **valid_repository_ref_data,
                issue_number=1,
                state="invalid"
            )
        assert "Invalid state" in str(exc_info.value)
        
    def test_empty_title(self, valid_repository_ref_data):
        """Test that empty title raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            UpdateIssueParams(
                **valid_repository_ref_data,
                issue_number=1,
                title=""
            )
        assert "title cannot be empty" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            UpdateIssueParams(
                **valid_repository_ref_data,
                issue_number=1,
                title="   "  # Whitespace only
            )
        assert "title cannot be empty" in str(exc_info.value)

    def test_none_values(self, valid_repository_ref_data):
        """Test behavior with None values."""
        # All optional fields can be None
        params = UpdateIssueParams(
            **valid_repository_ref_data,
            issue_number=1,
            title=None,
            body=None,
            state=None,
            labels=None,
            assignees=None,
            milestone=None
        )
        assert params.title is None
        assert params.body is None
        assert params.state is None
        assert params.labels is None
        assert params.assignees is None
        assert params.milestone is None


class TestDeleteIssueCommentParams:
    """Tests for the DeleteIssueCommentParams schema."""

    def test_valid_data(self, valid_delete_issue_comment_data):
        """Test that valid data passes validation."""
        params = DeleteIssueCommentParams(**valid_delete_issue_comment_data)
        assert params.owner == valid_delete_issue_comment_data["owner"]
        assert params.repo == valid_delete_issue_comment_data["repo"]
        assert params.issue_number == valid_delete_issue_comment_data["issue_number"]
        assert params.comment_id == valid_delete_issue_comment_data["comment_id"]

    def test_missing_required_fields(self, valid_repository_ref_data):
        """Test that missing required fields raise validation errors."""
        # Missing issue_number
        with pytest.raises(ValidationError) as exc_info:
            DeleteIssueCommentParams(
                **valid_repository_ref_data,
                comment_id=123456
            )
        assert "issue_number" in str(exc_info.value).lower()
        
        # Missing comment_id
        with pytest.raises(ValidationError) as exc_info:
            DeleteIssueCommentParams(
                **valid_repository_ref_data,
                issue_number=1
            )
        assert "comment_id" in str(exc_info.value).lower()

    def test_negative_issue_number(self, valid_repository_ref_data):
        """Test behavior with negative issue number."""
        # Negative issue number - should be valid (though not practical)
        params = DeleteIssueCommentParams(
            **valid_repository_ref_data,
            issue_number=-1,
            comment_id=123456
        )
        assert params.issue_number == -1


class TestAddIssueLabelsParams:
    """Tests for the AddIssueLabelsParams schema."""

    def test_valid_data(self, valid_add_issue_labels_data):
        """Test that valid data passes validation."""
        params = AddIssueLabelsParams(**valid_add_issue_labels_data)
        assert params.owner == valid_add_issue_labels_data["owner"]
        assert params.repo == valid_add_issue_labels_data["repo"]
        assert params.issue_number == valid_add_issue_labels_data["issue_number"]
        assert params.labels == valid_add_issue_labels_data["labels"]

    def test_missing_required_fields(self, valid_repository_ref_data):
        """Test that missing required fields raise validation errors."""
        # Missing issue_number
        with pytest.raises(ValidationError) as exc_info:
            AddIssueLabelsParams(
                **valid_repository_ref_data,
                labels=["bug", "help wanted"]
            )
        assert "issue_number" in str(exc_info.value).lower()
        
        # Missing labels
        with pytest.raises(ValidationError) as exc_info:
            AddIssueLabelsParams(
                **valid_repository_ref_data,
                issue_number=1
            )
        assert "labels" in str(exc_info.value).lower()

    def test_empty_labels_list(self, valid_repository_ref_data):
        """Test behavior with empty labels list."""
        # Empty labels list - should be valid but not practical
        with pytest.raises(ValidationError) as exc_info:
            AddIssueLabelsParams(
                **valid_repository_ref_data,
                issue_number=1,
                labels=[]
            )
        assert "labels" in str(exc_info.value).lower()

    def test_negative_issue_number(self, valid_repository_ref_data):
        """Test behavior with negative issue number."""
        # Negative issue number - should be valid (though not practical)
        params = AddIssueLabelsParams(
            **valid_repository_ref_data,
            issue_number=-1,
            labels=["bug", "help wanted"]
        )
        assert params.issue_number == -1


class TestIssueCommentParams:
    """Tests for the IssueCommentParams schema."""

    def test_valid_data(self, valid_issue_comment_data):
        """Test that valid data passes validation."""
        params = IssueCommentParams(**valid_issue_comment_data)
        assert params.owner == valid_issue_comment_data["owner"]
        assert params.repo == valid_issue_comment_data["repo"]
        assert params.issue_number == valid_issue_comment_data["issue_number"]
        assert params.body == valid_issue_comment_data["body"]

    def test_missing_required_fields(self, valid_repository_ref_data):
        """Test that missing required fields raise validation errors."""
        # Missing issue_number
        with pytest.raises(ValidationError) as exc_info:
            IssueCommentParams(
                **valid_repository_ref_data,
                body="This is a comment."
            )
        assert "issue_number" in str(exc_info.value).lower()
        
        # Missing body
        with pytest.raises(ValidationError) as exc_info:
            IssueCommentParams(
                **valid_repository_ref_data,
                issue_number=1
            )
        assert "body" in str(exc_info.value).lower()

    def test_empty_body(self, valid_repository_ref_data):
        """Test behavior with empty body."""
        # Empty body - should raise error
        with pytest.raises(ValidationError) as exc_info:
            IssueCommentParams(
                **valid_repository_ref_data,
                issue_number=1,
                body=""
            )
        assert "body cannot be empty" in str(exc_info.value).lower()
        
        # Whitespace-only body - should raise error
        with pytest.raises(ValidationError) as exc_info:
            IssueCommentParams(
                **valid_repository_ref_data,
                issue_number=1,
                body="   "
            )
        assert "body cannot be empty" in str(exc_info.value).lower()


class TestListIssueCommentsParams:
    """Tests for the ListIssueCommentsParams schema."""

    def test_valid_data(self, valid_list_issue_comments_data):
        """Test that valid data passes validation."""
        params = ListIssueCommentsParams(**valid_list_issue_comments_data)
        assert params.owner == valid_list_issue_comments_data["owner"]
        assert params.repo == valid_list_issue_comments_data["repo"]
        assert params.issue_number == valid_list_issue_comments_data["issue_number"]
        # Check that since is a datetime object with the correct values
        assert isinstance(params.since, datetime)
        assert params.since.year == 2020
        assert params.since.month == 1
        assert params.since.day == 1
        assert params.since.hour == 0
        assert params.since.minute == 0
        assert params.since.second == 0
        assert params.page == valid_list_issue_comments_data["page"]
        assert params.per_page == valid_list_issue_comments_data["per_page"]

    def test_minimal_valid_data(self, valid_repository_ref_data):
        """Test with minimal valid data (only required fields)."""
        # Only owner, repo, and issue_number are required
        params = ListIssueCommentsParams(
            **valid_repository_ref_data,
            issue_number=1
        )
        assert params.owner == valid_repository_ref_data["owner"]
        assert params.repo == valid_repository_ref_data["repo"]
        assert params.issue_number == 1
        assert params.since is None
        assert params.page is None
        assert params.per_page is None

    def test_datetime_parsing(self, valid_repository_ref_data):
        """Test that datetime strings are correctly parsed."""
        # ISO format datetime string
        params = ListIssueCommentsParams(
            **valid_repository_ref_data,
            issue_number=1,
            since="2020-01-01T00:00:00Z"
        )
        assert isinstance(params.since, datetime)
        assert params.since.year == 2020
        assert params.since.month == 1
        assert params.since.day == 1
        assert params.since.hour == 0
        assert params.since.minute == 0
        assert params.since.second == 0
        
        # Test with different ISO format
        params = ListIssueCommentsParams(
            **valid_repository_ref_data,
            issue_number=1,
            since="2020-01-01T12:30:45+00:00"
        )
        assert isinstance(params.since, datetime)
        assert params.since.year == 2020
        assert params.since.month == 1
        assert params.since.day == 1
        assert params.since.hour == 12
        assert params.since.minute == 30
        assert params.since.second == 45
        
        # Test with datetime object directly
        dt = datetime(2020, 1, 1, 0, 0, 0, tzinfo=datetime.now().astimezone().tzinfo)
        params = ListIssueCommentsParams(
            **valid_repository_ref_data,
            issue_number=1,
            since=dt
        )
        assert params.since == dt
