"""Integration tests for GitHub issue tools error cases.

These tests verify that the issue tools handle errors correctly, focusing on
parameter validation, edge cases, and error responses from the GitHub API.
"""

import json
import logging
import pytest
from datetime import datetime, timedelta

from pygithub_mcp_server.tools.issues.tools import (
    create_issue,
    get_issue,
    update_issue,
    list_issues,
    add_issue_comment,
    list_issue_comments,
    update_issue_comment,
    delete_issue_comment,
    add_issue_labels,
    remove_issue_label
)


# Configure logging
logger = logging.getLogger(__name__)


@pytest.mark.integration
class TestIssueToolsErrorHandling:
    """Tests for error handling in GitHub issue tools."""
    
    def test_create_issue_missing_required_params(self, test_repo_info):
        """Test create_issue with missing required parameters."""
        # Missing title (required parameter)
        params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            # Intentionally missing title
        }
        
        result = create_issue(params)
        
        # Verify proper error response
        assert result.get("is_error") is True
        assert len(result["content"]) == 1
        assert "title" in result["content"][0]["text"].lower()
    
    def test_create_issue_invalid_repo(self, test_repo_info):
        """Test create_issue with non-existent repository."""
        params = {
            "owner": test_repo_info["owner"],
            "repo": "non-existent-repo-12345",
            "title": "Test Invalid Repo"
        }
        
        result = create_issue(params)
        
        # Verify proper error response
        assert result.get("is_error") is True
        assert ("not found" in result["content"][0]["text"].lower() or 
                "404" in result["content"][0]["text"] or
                "does not exist" in result["content"][0]["text"].lower())
    
    def test_get_issue_invalid_number(self, test_repo_info):
        """Test get_issue with non-existent issue number."""
        params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": 999999999  # Very large number unlikely to exist
        }
        
        result = get_issue(params)
        
        # Verify proper error response
        assert result.get("is_error") is True
        assert ("not found" in result["content"][0]["text"].lower() or 
                "404" in result["content"][0]["text"] or
                "does not exist" in result["content"][0]["text"].lower())
    
    def test_update_issue_nonexistent(self, test_repo_info):
        """Test updating a non-existent issue."""
        params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": 999999999,
            "title": "Updated Title"
        }
        
        result = update_issue(params)
        
        # Verify proper error response
        assert result.get("is_error") is True
        assert "not found" in result["content"][0]["text"].lower() or "404" in result["content"][0]["text"]
    
    def test_update_issue_empty_values(self, test_repo_info, unique_id, issue_cleanup):
        """Test update_issue with empty values for optional fields."""
        # First create an issue to update
        create_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "title": f"Empty Values Test {unique_id}",
            "body": "Initial body"
        }
        
        create_result = create_issue(create_params)
        issue_data = json.loads(create_result["content"][0]["text"])
        issue_number = issue_data["issue_number"]
        issue_cleanup.append(issue_number)
        
        # Update with empty body
        update_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": issue_number,
            "body": ""  # Empty string
        }
        
        update_result = update_issue(update_params)
        
        # Verify successful update even with empty body
        assert not update_result.get("is_error")
        updated_issue = json.loads(update_result["content"][0]["text"])
        assert updated_issue["body"] == ""
    
    def test_add_issue_comment_invalid_issue(self, test_repo_info):
        """Test adding a comment to a non-existent issue."""
        params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": 999999999,
            "body": "Test comment on non-existent issue"
        }
        
        result = add_issue_comment(params)
        
        # Verify proper error response
        assert result.get("is_error") is True
        assert "not found" in result["content"][0]["text"].lower() or "404" in result["content"][0]["text"]
    
    def test_list_issue_comments_invalid_issue(self, test_repo_info):
        """Test listing comments for a non-existent issue."""
        params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": 999999999
        }
        
        result = list_issue_comments(params)
        
        # Verify proper error response
        assert result.get("is_error") is True
        assert "not found" in result["content"][0]["text"].lower() or "404" in result["content"][0]["text"]
    
    def test_list_issue_comments_pagination(self, test_repo_info, unique_id, issue_cleanup):
        """Test list_issue_comments with pagination parameters."""
        # First create an issue
        create_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "title": f"Pagination Test {unique_id}",
            "body": "Test body"
        }
        
        create_result = create_issue(create_params)
        issue_data = json.loads(create_result["content"][0]["text"])
        issue_number = issue_data["issue_number"]
        issue_cleanup.append(issue_number)
        
        # Add multiple comments
        for i in range(3):
            comment_params = {
                "owner": test_repo_info["owner"],
                "repo": test_repo_info["repo"],
                "issue_number": issue_number,
                "body": f"Test comment {i} for pagination"
            }
            add_issue_comment(comment_params)
        
        # Test pagination
        pagination_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": issue_number,
            "per_page": 1,
            "page": 1
        }
        
        pagination_result = list_issue_comments(pagination_params)
        
        # Verify pagination worked
        assert not pagination_result.get("is_error")
        comments = json.loads(pagination_result["content"][0]["text"])
        assert len(comments) <= 1  # Should have at most 1 comment (per_page=1)
    
    def test_update_comment_nonexistent(self, test_repo_info, unique_id, issue_cleanup):
        """Test updating a non-existent comment."""
        # First create an issue
        create_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "title": f"Comment Test {unique_id}",
            "body": "Test body"
        }
        
        create_result = create_issue(create_params)
        issue_data = json.loads(create_result["content"][0]["text"])
        issue_number = issue_data["issue_number"]
        issue_cleanup.append(issue_number)
        
        # Try to update a non-existent comment
        update_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": issue_number,
            "comment_id": 999999999,
            "body": "Updated comment"
        }
        
        result = update_issue_comment(update_params)
        
        # Verify proper error response
        assert result.get("is_error") is True
        assert "not found" in result["content"][0]["text"].lower() or "404" in result["content"][0]["text"]
    
    def test_delete_comment_nonexistent(self, test_repo_info, unique_id, issue_cleanup):
        """Test deleting a non-existent comment."""
        # First create an issue
        create_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "title": f"Comment Delete Test {unique_id}",
            "body": "Test body"
        }
        
        create_result = create_issue(create_params)
        issue_data = json.loads(create_result["content"][0]["text"])
        issue_number = issue_data["issue_number"]
        issue_cleanup.append(issue_number)
        
        # Try to delete a non-existent comment
        delete_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": issue_number,
            "comment_id": 999999999
        }
        
        result = delete_issue_comment(delete_params)
        
        # Verify proper error response
        assert result.get("is_error") is True
        assert "not found" in result["content"][0]["text"].lower() or "404" in result["content"][0]["text"]
    
    def test_add_labels_nonexistent_issue(self, test_repo_info):
        """Test adding labels to a non-existent issue."""
        params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": 999999999,
            "labels": ["test-label"]
        }
        
        result = add_issue_labels(params)
        
        # Verify proper error response
        assert result.get("is_error") is True
        assert "not found" in result["content"][0]["text"].lower() or "404" in result["content"][0]["text"]
    
    def test_remove_label_nonexistent_issue(self, test_repo_info):
        """Test removing a label from a non-existent issue."""
        params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": 999999999,
            "label": "test-label"
        }
        
        result = remove_issue_label(params)
        
        # Verify proper error response
        assert result.get("is_error") is True
        assert "not found" in result["content"][0]["text"].lower() or "404" in result["content"][0]["text"]
    
    def test_remove_nonexistent_label(self, test_repo_info, unique_id, issue_cleanup):
        """Test removing a non-existent label from an issue."""
        # First create an issue
        create_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "title": f"Label Test {unique_id}",
            "body": "Test body"
        }
        
        create_result = create_issue(create_params)
        issue_data = json.loads(create_result["content"][0]["text"])
        issue_number = issue_data["issue_number"]
        issue_cleanup.append(issue_number)
        
        # Try to remove a non-existent label
        remove_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": issue_number,
            "label": f"nonexistent-label-{unique_id}"
        }
        
        result = remove_issue_label(remove_params)
        
        # Verify proper error response
        assert result.get("is_error") is True
        assert ("not found" in result["content"][0]["text"].lower() or 
                "404" in result["content"][0]["text"] or
                "does not exist" in result["content"][0]["text"].lower())
    
    def test_list_issues_pagination(self, test_repo_info):
        """Test listing issues with pagination."""
        # Test pagination with per_page parameter
        pagination_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "per_page": 2,
            "page": 1
        }
        
        result = list_issues(pagination_params)
        
        # Verify pagination worked
        assert not result.get("is_error")
        issues = json.loads(result["content"][0]["text"])
        assert len(issues) <= 2  # Should have at most 2 issues (per_page=2)
    
    def test_list_issues_invalid_params(self, test_repo_info):
        """Test listing issues with invalid parameters."""
        # Test with invalid state
        invalid_state_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "state": "invalid_state"  # Not open, closed, or all
        }
        
        result = list_issues(invalid_state_params)
        
        # May not fail validation since GitHub API might accept the invalid state
        # but we can check the response format is correct
        assert "content" in result
        
        # Test with invalid sort
        invalid_sort_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "sort": "invalid_sort"  # Not created, updated, or comments
        }
        
        result = list_issues(invalid_sort_params)
        
        # May not fail validation since GitHub API might accept the invalid sort
        # but we can check the response format is correct
        assert "content" in result
    
    def test_list_issues_invalid_since(self, test_repo_info):
        """Test listing issues with invalid since parameter."""
        # Invalid date format
        params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "since": "not-a-date"
        }
        
        result = list_issues(params)
        
        # Should get an error response
        assert result.get("is_error") is True
    
    def test_list_issue_comments_invalid_since(self, test_repo_info, unique_id, issue_cleanup):
        """Test listing comments with invalid since parameter."""
        # First create an issue
        create_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "title": f"Comment Since Test {unique_id}",
            "body": "Test body"
        }
        
        create_result = create_issue(create_params)
        issue_data = json.loads(create_result["content"][0]["text"])
        issue_number = issue_data["issue_number"]
        issue_cleanup.append(issue_number)
        
        # Invalid date format
        params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": issue_number,
            "since": "not-a-date"
        }
        
        result = list_issue_comments(params)
        
        # Should get an error response
        assert result.get("is_error") is True
