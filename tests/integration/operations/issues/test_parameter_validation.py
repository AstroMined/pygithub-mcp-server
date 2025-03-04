"""Integration tests for parameter validation in issue operations.

These tests specifically target the parameter validation logic in the issues.py
operations module to improve code coverage.
"""

import logging
import pytest
from datetime import datetime, timedelta

from pygithub_mcp_server.errors import GitHubError
from pygithub_mcp_server.operations.issues import (
    list_issues,
    list_issue_comments,
    update_issue,
    create_issue,
    add_issue_labels,
    remove_issue_label
)


# Configure logging
logger = logging.getLogger(__name__)


@pytest.mark.integration
class TestIssueOperationsValidation:
    """Tests for parameter validation in issue operations."""
    
    def test_list_issues_invalid_state(self, test_owner, test_repo_name):
        """Test list_issues with invalid state parameter."""
        with pytest.raises(GitHubError) as exc_info:
            list_issues(test_owner, test_repo_name, state="invalid_state")
        
        # Verify proper error message
        assert "Invalid state" in str(exc_info.value)
    
    def test_list_issues_invalid_sort(self, test_owner, test_repo_name):
        """Test list_issues with invalid sort parameter."""
        with pytest.raises(GitHubError) as exc_info:
            list_issues(test_owner, test_repo_name, sort="invalid_sort")
        
        # Verify proper error message
        assert "Invalid sort" in str(exc_info.value)
    
    def test_list_issues_invalid_direction(self, test_owner, test_repo_name):
        """Test list_issues with invalid direction parameter."""
        with pytest.raises(GitHubError) as exc_info:
            list_issues(test_owner, test_repo_name, direction="invalid_direction")
        
        # Verify proper error message
        assert "Invalid direction" in str(exc_info.value)
    
    def test_list_issues_invalid_page(self, test_owner, test_repo_name):
        """Test list_issues with invalid page parameter."""
        # Test negative page
        with pytest.raises(GitHubError) as exc_info:
            list_issues(test_owner, test_repo_name, page=-1)
        
        assert "Invalid page number" in str(exc_info.value)
        
        # Test non-integer page
        with pytest.raises(GitHubError) as exc_info:
            list_issues(test_owner, test_repo_name, page="not_a_number")
        
        assert "Invalid page number" in str(exc_info.value)
    
    def test_list_issues_invalid_per_page(self, test_owner, test_repo_name):
        """Test list_issues with invalid per_page parameter."""
        # Test negative per_page
        with pytest.raises(GitHubError) as exc_info:
            list_issues(test_owner, test_repo_name, per_page=-1)
        
        assert "Invalid per_page value" in str(exc_info.value)
        
        # Test non-integer per_page
        with pytest.raises(GitHubError) as exc_info:
            list_issues(test_owner, test_repo_name, per_page="not_a_number")
        
        assert "Invalid per_page value" in str(exc_info.value)
        
        # Test too large per_page
        with pytest.raises(GitHubError) as exc_info:
            list_issues(test_owner, test_repo_name, per_page=101)
        
        assert "per_page cannot exceed 100" in str(exc_info.value)
    
    def test_list_issues_invalid_labels(self, test_owner, test_repo_name):
        """Test list_issues with invalid labels parameter."""
        # Test non-list labels
        with pytest.raises(GitHubError) as exc_info:
            list_issues(test_owner, test_repo_name, labels="not_a_list")
        
        assert "Labels must be a list" in str(exc_info.value)
        
        # Test labels with non-string items
        with pytest.raises(GitHubError) as exc_info:
            list_issues(test_owner, test_repo_name, labels=["valid", 123])
        
        assert "Labels must be a list of strings" in str(exc_info.value)
    
    def test_list_issues_invalid_since(self, test_owner, test_repo_name):
        """Test list_issues with invalid since parameter."""
        # Test non-datetime since
        with pytest.raises(GitHubError) as exc_info:
            list_issues(test_owner, test_repo_name, since="not_a_date")
        
        assert "since parameter" in str(exc_info.value).lower()
    
    def test_update_issue_with_no_changes(self, test_owner, test_repo_name, unique_id, with_retry):
        """Test update_issue with no changes provided."""
        # First create an issue to update
        @with_retry
        def create_test_issue():
            return create_issue(
                owner=test_owner,
                repo=test_repo_name,
                title=f"Test No Changes {unique_id}"
            )
        
        issue = create_test_issue()
        issue_number = issue["issue_number"]
        
        try:
            # Call update_issue with no changes
            @with_retry
            def update_with_no_changes():
                return update_issue(
                    owner=test_owner,
                    repo=test_repo_name,
                    issue_number=issue_number
                    # No parameters changed
                )
            
            result = update_with_no_changes()
            
            # Should return the original issue
            assert result["issue_number"] == issue_number
            assert result["title"] == issue["title"]
        finally:
            # Close the issue
            update_issue(test_owner, test_repo_name, issue_number, state="closed")
    
    def test_update_issue_invalid_milestone(self, test_owner, test_repo_name, unique_id, with_retry):
        """Test update_issue with invalid milestone."""
        # First create an issue to update
        @with_retry
        def create_test_issue():
            return create_issue(
                owner=test_owner,
                repo=test_repo_name,
                title=f"Test Invalid Milestone {unique_id}"
            )
        
        issue = create_test_issue()
        issue_number = issue["issue_number"]
        
        try:
            # Call update_issue with non-existent milestone
            with pytest.raises(GitHubError) as exc_info:
                update_issue(
                    owner=test_owner,
                    repo=test_repo_name,
                    issue_number=issue_number,
                    milestone=999999999  # Non-existent milestone
                )
            
            # Should raise an error
            assert "Invalid milestone" in str(exc_info.value)
        finally:
            # Close the issue
            update_issue(test_owner, test_repo_name, issue_number, state="closed")
    
    def test_create_issue_invalid_milestone(self, test_owner, test_repo_name, unique_id):
        """Test create_issue with invalid milestone."""
        # Call create_issue with non-existent milestone
        with pytest.raises(GitHubError) as exc_info:
            create_issue(
                owner=test_owner,
                repo=test_repo_name,
                title=f"Test Invalid Milestone {unique_id}",
                milestone=999999999  # Non-existent milestone
            )
        
        # Should raise an error
        assert "Invalid milestone" in str(exc_info.value)
    
    def test_list_issue_comments_invalid_since(self, test_owner, test_repo_name, unique_id, with_retry):
        """Test list_issue_comments with invalid since parameter."""
        # First create an issue to list comments for
        @with_retry
        def create_test_issue():
            return create_issue(
                owner=test_owner,
                repo=test_repo_name,
                title=f"Test Comments Since {unique_id}"
            )
        
        issue = create_test_issue()
        issue_number = issue["issue_number"]
        
        try:
            # Test non-datetime since
            with pytest.raises(GitHubError) as exc_info:
                list_issue_comments(
                    owner=test_owner,
                    repo=test_repo_name,
                    issue_number=issue_number,
                    since="not_a_date"
                )
            
            assert "since parameter" in str(exc_info.value).lower()
        finally:
            # Close the issue
            update_issue(test_owner, test_repo_name, issue_number, state="closed")
    
    def test_list_issues_timezone_handling(self, test_owner, test_repo_name):
        """Test list_issues with different timezone formats."""
        # Get current time minus one day
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        
        # Test ISO format with Z
        result_z = list_issues(
            owner=test_owner,
            repo=test_repo_name,
            since=yesterday.replace(microsecond=0).isoformat() + "Z"
        )
        
        # Test ISO format with +00:00
        result_offset = list_issues(
            owner=test_owner,
            repo=test_repo_name,
            since=yesterday.replace(microsecond=0).isoformat() + "+00:00"
        )
        
        # Both should work and return issues
        assert isinstance(result_z, list)
        assert isinstance(result_offset, list)
