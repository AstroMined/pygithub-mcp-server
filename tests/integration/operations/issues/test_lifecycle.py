"""Issue lifecycle integration tests.

This module tests the complete lifecycle of GitHub issues using the real GitHub API,
including creation, retrieval, updating, commenting, labeling, and closing.
"""

import pytest
from datetime import datetime

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


@pytest.mark.integration
def test_issue_lifecycle(test_owner, test_repo_name, unique_id, with_retry):
    """Test complete issue lifecycle with real API."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue {unique_id}"
    body = f"Test body created at {datetime.now().isoformat()}"
    
    # Create issue
    @with_retry
    def create_test_issue():
        return create_issue(owner, repo, title, body=body)
    
    issue = create_test_issue()
    assert issue["title"] == title
    assert issue["body"] == body
    assert issue["state"] == "open"
    
    try:
        # Get issue
        @with_retry
        def get_test_issue():
            return get_issue(owner, repo, issue["issue_number"])
        
        fetched = get_test_issue()
        assert fetched["issue_number"] == issue["issue_number"]
        assert fetched["title"] == title
        
        # Update issue
        @with_retry
        def update_test_issue():
            updated_title = f"Updated {title}"
            return update_issue(owner, repo, issue["issue_number"], title=updated_title)
        
        updated = update_test_issue()
        assert updated["title"] == f"Updated {title}"
        
        # Add comment
        @with_retry
        def add_test_comment():
            return add_issue_comment(owner, repo, issue["issue_number"], "Test comment")
        
        comment = add_test_comment()
        assert comment["body"] == "Test comment"
        
        # List comments
        @with_retry
        def list_test_comments():
            return list_issue_comments(owner, repo, issue["issue_number"])
        
        comments = list_test_comments()
        assert len(comments) >= 1
        assert any(c["body"] == "Test comment" for c in comments)
        
        # Update comment
        @with_retry
        def update_test_comment():
            return update_issue_comment(
                owner, repo, issue["issue_number"], comment["id"], "Updated comment"
            )
        
        updated_comment = update_test_comment()
        assert updated_comment["body"] == "Updated comment"
        
        # Add labels
        @with_retry
        def add_test_labels():
            return add_issue_labels(owner, repo, issue["issue_number"], ["test-label"])
        
        labels = add_test_labels()
        assert any(label["name"] == "test-label" for label in labels)
        
        # Remove label
        @with_retry
        def remove_test_label():
            return remove_issue_label(owner, repo, issue["issue_number"], "test-label")
        
        remove_test_label()
        
        # Close issue
        @with_retry
        def close_test_issue():
            return update_issue(owner, repo, issue["issue_number"], state="closed")
        
        closed = close_test_issue()
        assert closed["state"] == "closed"
        
    finally:
        # Cleanup - ensure issue is closed even if test fails
        try:
            @with_retry
            def ensure_closed():
                return update_issue(owner, repo, issue["issue_number"], state="closed")
            
            ensure_closed()
        except Exception as e:
            print(f"Failed to close issue during cleanup: {e}")
