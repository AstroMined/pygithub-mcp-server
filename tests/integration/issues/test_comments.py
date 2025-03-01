"""Issue comments integration tests.

This module tests the issue comment operations using the real GitHub API.
"""

import pytest
from datetime import datetime, timedelta

from pygithub_mcp_server.operations.issues import (
    create_issue,
    update_issue,
    add_issue_comment,
    list_issue_comments,
    update_issue_comment,
    delete_issue_comment,
)


@pytest.mark.integration
def test_add_issue_comment(test_owner, test_repo_name, unique_id, with_retry):
    """Test adding a comment to an issue."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (Add Comment) {unique_id}"
    
    # Create an issue
    @with_retry
    def create_test_issue():
        return create_issue(owner, repo, title)
    
    issue = create_test_issue()
    
    try:
        # Add a comment
        comment_body = f"Test comment at {datetime.now().isoformat()}"
        
        @with_retry
        def add_test_comment():
            return add_issue_comment(owner, repo, issue["issue_number"], comment_body)
        
        comment = add_test_comment()
        
        # Verify
        assert comment["body"] == comment_body
        assert "id" in comment
        assert "user" in comment
        assert "created_at" in comment
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
def test_list_issue_comments(test_owner, test_repo_name, unique_id, with_retry):
    """Test listing comments on an issue."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (List Comments) {unique_id}"
    
    # Create an issue
    @with_retry
    def create_test_issue():
        return create_issue(owner, repo, title)
    
    issue = create_test_issue()
    
    try:
        # Add a comment
        comment_body = f"Test comment for listing at {datetime.now().isoformat()}"
        
        @with_retry
        def add_test_comment():
            return add_issue_comment(owner, repo, issue["issue_number"], comment_body)
        
        comment = add_test_comment()
        
        # List comments
        @with_retry
        def list_test_comments():
            return list_issue_comments(owner, repo, issue["issue_number"])
        
        comments = list_test_comments()
        
        # Verify
        assert isinstance(comments, list)
        assert len(comments) >= 1
        
        # Verify our comment is in the list
        found = False
        for c in comments:
            if c["id"] == comment["id"]:
                found = True
                assert c["body"] == comment_body
                break
        
        assert found, "Test comment not found in list_issue_comments results"
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
def test_update_issue_comment(test_owner, test_repo_name, unique_id, with_retry):
    """Test updating a comment on an issue."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (Update Comment) {unique_id}"
    
    # Create an issue
    @with_retry
    def create_test_issue():
        return create_issue(owner, repo, title)
    
    issue = create_test_issue()
    
    try:
        # Add a comment
        comment_body = f"Initial comment at {datetime.now().isoformat()}"
        
        @with_retry
        def add_test_comment():
            return add_issue_comment(owner, repo, issue["issue_number"], comment_body)
        
        comment = add_test_comment()
        
        # Update the comment
        updated_body = f"Updated comment at {datetime.now().isoformat()}"
        
        @with_retry
        def update_test_comment():
            return update_issue_comment(
                owner, repo, issue["issue_number"], comment["id"], updated_body
            )
        
        updated = update_test_comment()
        
        # Verify
        assert updated["id"] == comment["id"]
        assert updated["body"] == updated_body
        assert updated["body"] != comment_body
        
        # List comments to verify update
        @with_retry
        def list_test_comments():
            return list_issue_comments(owner, repo, issue["issue_number"])
        
        comments = list_test_comments()
        
        # Verify our updated comment is in the list
        found = False
        for c in comments:
            if c["id"] == comment["id"]:
                found = True
                assert c["body"] == updated_body
                break
        
        assert found, "Updated comment not found in list_issue_comments results"
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
def test_delete_issue_comment(test_owner, test_repo_name, unique_id, with_retry):
    """Test deleting a comment from an issue."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (Delete Comment) {unique_id}"
    
    # Create an issue
    @with_retry
    def create_test_issue():
        return create_issue(owner, repo, title)
    
    issue = create_test_issue()
    
    try:
        # Add a comment
        comment_body = f"Comment to delete at {datetime.now().isoformat()}"
        
        @with_retry
        def add_test_comment():
            return add_issue_comment(owner, repo, issue["issue_number"], comment_body)
        
        comment = add_test_comment()
        
        # Verify comment exists
        @with_retry
        def list_test_comments_before():
            return list_issue_comments(owner, repo, issue["issue_number"])
        
        comments_before = list_test_comments_before()
        
        found_before = False
        for c in comments_before:
            if c["id"] == comment["id"]:
                found_before = True
                break
        
        assert found_before, "Comment not found before deletion"
        
        # Delete the comment
        @with_retry
        def delete_test_comment():
            return delete_issue_comment(owner, repo, issue["issue_number"], comment["id"])
        
        delete_test_comment()
        
        # Verify comment is deleted
        @with_retry
        def list_test_comments_after():
            return list_issue_comments(owner, repo, issue["issue_number"])
        
        comments_after = list_test_comments_after()
        
        for c in comments_after:
            assert c["id"] != comment["id"], "Comment still exists after deletion"
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
def test_list_issue_comments_since(test_owner, test_repo_name, unique_id, with_retry):
    """Test listing comments on an issue with since parameter."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (List Comments Since) {unique_id}"
    
    # Create an issue
    @with_retry
    def create_test_issue():
        return create_issue(owner, repo, title)
    
    issue = create_test_issue()
    
    try:
        # Add a comment
        comment_body = f"Test comment for since filter at {datetime.now().isoformat()}"
        
        @with_retry
        def add_test_comment():
            return add_issue_comment(owner, repo, issue["issue_number"], comment_body)
        
        comment = add_test_comment()
        
        # Get the current time
        now = datetime.now()
        
        # Set since to 1 hour ago
        since = now - timedelta(hours=1)
        
        # List comments since 1 hour ago
        @with_retry
        def list_test_comments_since():
            return list_issue_comments(owner, repo, issue["issue_number"], since=since.isoformat())
        
        recent_comments = list_test_comments_since()
        
        # Verify our comment is in the list
        found = False
        for c in recent_comments:
            if c["id"] == comment["id"]:
                found = True
                assert c["body"] == comment_body
                break
        
        assert found, "Test comment not found in since filter results"
        
        # Set since to 1 hour in the future
        future = now + timedelta(hours=1)
        
        # List comments since 1 hour in the future
        @with_retry
        def list_test_comments_future():
            return list_issue_comments(owner, repo, issue["issue_number"], since=future.isoformat())
        
        future_comments = list_test_comments_future()
        
        # Verify our comment is not in the list
        for c in future_comments:
            assert c["id"] != comment["id"], "Comment found with future since filter"
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
def test_comment_lifecycle(test_owner, test_repo_name, unique_id, with_retry):
    """Test complete comment lifecycle (add → list → update → delete)."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (Comment Lifecycle) {unique_id}"
    
    # Create an issue
    @with_retry
    def create_test_issue():
        return create_issue(owner, repo, title)
    
    issue = create_test_issue()
    
    try:
        # Add a comment
        comment_body = f"Initial comment at {datetime.now().isoformat()}"
        
        @with_retry
        def add_test_comment():
            return add_issue_comment(owner, repo, issue["issue_number"], comment_body)
        
        comment = add_test_comment()
        assert comment["body"] == comment_body
        
        # List comments
        @with_retry
        def list_test_comments():
            return list_issue_comments(owner, repo, issue["issue_number"])
        
        comments = list_test_comments()
        found = False
        for c in comments:
            if c["id"] == comment["id"]:
                found = True
                break
        assert found, "Comment not found in list after adding"
        
        # Update comment
        updated_body = f"Updated comment at {datetime.now().isoformat()}"
        
        @with_retry
        def update_test_comment():
            return update_issue_comment(
                owner, repo, issue["issue_number"], comment["id"], updated_body
            )
        
        updated = update_test_comment()
        assert updated["body"] == updated_body
        
        # List comments again to verify update
        @with_retry
        def list_test_comments_after_update():
            return list_issue_comments(owner, repo, issue["issue_number"])
        
        comments_after_update = list_test_comments_after_update()
        found_updated = False
        for c in comments_after_update:
            if c["id"] == comment["id"]:
                found_updated = True
                assert c["body"] == updated_body
                break
        assert found_updated, "Updated comment not found in list"
        
        # Delete comment
        @with_retry
        def delete_test_comment():
            return delete_issue_comment(owner, repo, issue["issue_number"], comment["id"])
        
        delete_test_comment()
        
        # List comments again to verify deletion
        @with_retry
        def list_test_comments_after_delete():
            return list_issue_comments(owner, repo, issue["issue_number"])
        
        comments_after_delete = list_test_comments_after_delete()
        for c in comments_after_delete:
            assert c["id"] != comment["id"], "Comment still exists after deletion"
    finally:
        # Cleanup
        try:
            @with_retry
            def close_issue():
                return update_issue(owner, repo, issue["issue_number"], state="closed")
            
            close_issue()
        except Exception as e:
            print(f"Failed to close issue during cleanup: {e}")
