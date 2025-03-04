"""Create issue integration tests.

This module tests the create_issue operation using the real GitHub API.
"""

import pytest
from datetime import datetime

from pygithub_mcp_server.operations.issues import create_issue, get_issue, update_issue


@pytest.mark.integration
def test_create_issue_required_params(test_owner, test_repo_name, unique_id, with_retry):
    """Test create_issue with only required parameters."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (Required Params) {unique_id}"
    
    # Create issue
    @with_retry
    def create_test_issue():
        return create_issue(owner, repo, title)
    
    issue = create_test_issue()
    
    try:
        # Verify
        assert issue["title"] == title
        assert issue["state"] == "open"
        assert issue["body"] is None or issue["body"] == ""
        assert not issue["labels"]
        assert not issue["assignees"]
        assert issue["milestone"] is None
    finally:
        # Cleanup
        try:
            @with_retry
            def close_issue():
                return update_issue(owner, repo, issue["issue_number"], state="closed")
            
            close_issue()
        except Exception as e:
            print(f"Failed to close issue during cleanup: {e}")


@pytest.mark.integration
def test_create_issue_all_params(test_owner, test_repo_name, unique_id, with_retry):
    """Test create_issue with all parameters."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (All Params) {unique_id}"
    body = f"Test body created at {datetime.now().isoformat()}"
    
    # Create issue
    @with_retry
    def create_test_issue():
        return create_issue(
            owner=owner,
            repo=repo,
            title=title,
            body=body,
            labels=["test-label"],
            assignees=[owner]  # Assign to the repo owner
        )
    
    issue = create_test_issue()
    
    try:
        # Verify
        assert issue["title"] == title
        assert issue["body"] == body
        assert issue["state"] == "open"
        assert any(label["name"] == "test-label" for label in issue["labels"])
        assert any(assignee["login"] == owner for assignee in issue["assignees"])
    finally:
        # Cleanup
        try:
            @with_retry
            def close_issue():
                return update_issue(owner, repo, issue["issue_number"], state="closed")
            
            close_issue()
        except Exception as e:
            print(f"Failed to close issue during cleanup: {e}")


@pytest.mark.integration
def test_create_and_verify_issue(test_owner, test_repo_name, unique_id, with_retry):
    """Test create_issue and verify with get_issue."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (Create and Verify) {unique_id}"
    body = f"Test body created at {datetime.now().isoformat()}"
    
    # Create issue
    @with_retry
    def create_test_issue():
        return create_issue(owner, repo, title, body=body)
    
    issue = create_test_issue()
    
    try:
        # Verify by getting the issue
        @with_retry
        def get_test_issue():
            return get_issue(owner, repo, issue["issue_number"])
        
        fetched = get_test_issue()
        
        # Verify
        assert fetched["issue_number"] == issue["issue_number"]
        assert fetched["title"] == title
        assert fetched["body"] == body
        assert fetched["state"] == "open"
    finally:
        # Cleanup
        try:
            @with_retry
            def close_issue():
                return update_issue(owner, repo, issue["issue_number"], state="closed")
            
            close_issue()
        except Exception as e:
            print(f"Failed to close issue during cleanup: {e}")
