"""Integration tests for GitHub issue tools.

These tests verify that the issue tools work correctly with the real GitHub API.
They follow the principles in ADR-002 which emphasizes testing with real API calls
instead of mocks.
"""

import os
import json
import uuid
import time
import logging
from datetime import datetime, timedelta

import pytest
from mcp.server.fastmcp import FastMCP

from pygithub_mcp_server.server import create_server
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


@pytest.fixture(scope="module")
def test_repo_info():
    """Get test repository information from environment variables."""
    owner = os.environ.get("GITHUB_TEST_OWNER")
    repo = os.environ.get("GITHUB_TEST_REPO")
    
    if not owner or not repo:
        pytest.skip("GITHUB_TEST_OWNER and GITHUB_TEST_REPO environment variables required")
    
    return {
        "owner": owner,
        "repo": repo
    }


@pytest.fixture
def unique_id():
    """Generate a unique ID for test resources to prevent test interference."""
    return f"test-{uuid.uuid4().hex[:8]}"


@pytest.fixture
def issue_cleanup(test_repo_info):
    """Clean up test issues after the test."""
    created_issues = []
    
    yield created_issues
    
    # Clean up all issues created during the test
    for issue_number in created_issues:
        try:
            params = {
                "owner": test_repo_info["owner"],
                "repo": test_repo_info["repo"],
                "issue_number": issue_number,
                "state": "closed"
            }
            logger.info(f"Cleaning up test issue #{issue_number}")
            update_issue(params)
        except Exception as e:
            logger.warning(f"Failed to clean up issue #{issue_number}: {e}")


@pytest.mark.integration
class TestIssueTools:
    """Integration tests for GitHub issue tools."""
    
    def test_issue_lifecycle(self, test_repo_info, unique_id, issue_cleanup):
        """Test the complete lifecycle of an issue."""
        # Step 1: Create an issue
        create_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "title": f"Test Issue {unique_id}",
            "body": f"This is a test issue created by integration tests at {datetime.now().isoformat()}",
            "labels": ["test", "integration"],
        }
        
        create_result = create_issue(create_params)
        
        # Verify successful creation
        assert not create_result.get("is_error")
        assert len(create_result["content"]) == 1
        assert create_result["content"][0]["type"] == "text"
        
        issue_data = json.loads(create_result["content"][0]["text"])
        assert issue_data["title"] == create_params["title"]
        assert issue_data["body"] == create_params["body"]
        assert "test" in [label["name"] for label in issue_data["labels"]]
        
        issue_number = issue_data["number"]
        issue_cleanup.append(issue_number)
        logger.info(f"Created test issue #{issue_number}")
        
        # Step 2: Get the issue
        get_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": issue_number
        }
        
        get_result = get_issue(get_params)
        
        # Verify successful retrieval
        assert not get_result.get("is_error")
        fetched_issue = json.loads(get_result["content"][0]["text"])
        assert fetched_issue["number"] == issue_number
        assert fetched_issue["title"] == create_params["title"]
        
        # Step 3: Update the issue
        update_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": issue_number,
            "title": f"Updated: {create_params['title']}",
            "body": f"Updated body: {create_params['body']}"
        }
        
        update_result = update_issue(update_params)
        
        # Verify successful update
        assert not update_result.get("is_error")
        updated_issue = json.loads(update_result["content"][0]["text"])
        assert updated_issue["title"] == update_params["title"]
        assert updated_issue["body"] == update_params["body"]
        
        # Step 4: Add a comment
        comment_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": issue_number,
            "body": f"Test comment {unique_id}"
        }
        
        comment_result = add_issue_comment(comment_params)
        
        # Verify successful comment creation
        assert not comment_result.get("is_error")
        comment_data = json.loads(comment_result["content"][0]["text"])
        assert comment_data["body"] == comment_params["body"]
        comment_id = comment_data["id"]
        
        # Step 5: List comments
        list_comments_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": issue_number
        }
        
        list_comments_result = list_issue_comments(list_comments_params)
        
        # Verify comments are listed
        assert not list_comments_result.get("is_error")
        comments = json.loads(list_comments_result["content"][0]["text"])
        assert len(comments) >= 1
        assert any(comment["id"] == comment_id for comment in comments)
        
        # Step 6: Update comment
        update_comment_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": issue_number,
            "comment_id": comment_id,
            "body": f"Updated comment {unique_id}"
        }
        
        update_comment_result = update_issue_comment(update_comment_params)
        
        # Verify successful comment update
        assert not update_comment_result.get("is_error")
        updated_comment = json.loads(update_comment_result["content"][0]["text"])
        assert updated_comment["body"] == update_comment_params["body"]
        
        # Step 7: Add labels
        add_labels_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": issue_number,
            "labels": ["documentation", "enhancement"]
        }
        
        add_labels_result = add_issue_labels(add_labels_params)
        
        # Verify labels were added
        assert not add_labels_result.get("is_error")
        labels = json.loads(add_labels_result["content"][0]["text"])
        label_names = [label["name"] for label in labels]
        assert "documentation" in label_names
        assert "enhancement" in label_names
        
        # Step 8: Remove a label
        remove_label_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": issue_number,
            "label": "documentation"
        }
        
        remove_label_result = remove_issue_label(remove_label_params)
        
        # Verify label was removed
        assert not remove_label_result.get("is_error")
        
        # Verify with get_issue
        updated_get_result = get_issue(get_params)
        updated_issue_data = json.loads(updated_get_result["content"][0]["text"])
        updated_label_names = [label["name"] for label in updated_issue_data["labels"]]
        assert "documentation" not in updated_label_names
        assert "enhancement" in updated_label_names
        
        # Step 9: Delete comment
        delete_comment_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": issue_number,
            "comment_id": comment_id
        }
        
        delete_comment_result = delete_issue_comment(delete_comment_params)
        
        # Verify successful deletion
        assert not delete_comment_result.get("is_error")
        assert "Comment deleted successfully" in delete_comment_result["content"][0]["text"]
        
        # Step 10: Close the issue
        close_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "issue_number": issue_number,
            "state": "closed"
        }
        
        close_result = update_issue(close_params)
        
        # Verify successful closure
        assert not close_result.get("is_error")
        closed_issue = json.loads(close_result["content"][0]["text"])
        assert closed_issue["state"] == "closed"
    
    def test_list_issues(self, test_repo_info, unique_id, issue_cleanup):
        """Test listing issues with various filters."""
        # Create a test issue first
        create_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "title": f"List Test Issue {unique_id}",
            "body": "This is a test issue for list_issues",
            "labels": ["test", "list-test"]
        }
        
        create_result = create_issue(create_params)
        issue_data = json.loads(create_result["content"][0]["text"])
        issue_number = issue_data["number"]
        issue_cleanup.append(issue_number)
        
        # Wait a moment to ensure the issue is indexed
        time.sleep(1)
        
        # Test basic listing
        list_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "state": "open"
        }
        
        list_result = list_issues(list_params)
        
        # Verify issues are listed
        assert not list_result.get("is_error")
        issues = json.loads(list_result["content"][0]["text"])
        assert len(issues) > 0
        assert any(issue["number"] == issue_number for issue in issues)
        
        # Test filtering by label
        label_filter_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "labels": ["list-test"]
        }
        
        label_result = list_issues(label_filter_params)
        
        # Verify filtered issues
        assert not label_result.get("is_error")
        filtered_issues = json.loads(label_result["content"][0]["text"])
        assert len(filtered_issues) > 0
        assert all("list-test" in [label["name"] for label in issue["labels"]] for issue in filtered_issues)
        
        # Test since parameter
        since_date = datetime.now() - timedelta(days=1)
        since_params = {
            "owner": test_repo_info["owner"],
            "repo": test_repo_info["repo"],
            "since": since_date.isoformat()
        }
        
        since_result = list_issues(since_params)
        
        # Verify issues since date
        assert not since_result.get("is_error")
