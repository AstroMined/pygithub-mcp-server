"""Update issue integration tests.

This module tests the update_issue operation using the real GitHub API.
"""

import pytest
from datetime import datetime

from pygithub_mcp_server.operations.issues import create_issue, get_issue, update_issue
from pygithub_mcp_server.schemas.issues import (
    CreateIssueParams,
    GetIssueParams,
    UpdateIssueParams,
)


@pytest.mark.integration
def test_update_issue_title(test_owner, test_repo_name, unique_id, with_retry):
    """Test updating an issue's title."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (Update Title) {unique_id}"
    
    # Create issue
    @with_retry
    def create_test_issue():
        return create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title
        ))
    
    issue = create_test_issue()
    
    try:
        # Update issue title
        updated_title = f"Updated Title {unique_id}"
        
        @with_retry
        def update_test_issue():
            return update_issue(UpdateIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"],
                title=updated_title
            ))
        
        updated = update_test_issue()
        
        # Verify
        assert updated["title"] == updated_title
        assert updated["issue_number"] == issue["issue_number"]
        assert updated["state"] == "open"  # State should not change
        
        # Verify with get_issue
        @with_retry
        def get_test_issue():
            return get_issue(GetIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"]
            ))
        
        fetched = get_test_issue()
        assert fetched["title"] == updated_title
    finally:
        # Cleanup
        try:
            @with_retry
            def close_issue():
                return update_issue(UpdateIssueParams(
                    owner=owner,
                    repo=repo,
                    issue_number=issue["issue_number"],
                    state="closed"
                ))
            
            close_issue()
        except Exception as e:
            print(f"Failed to close issue during cleanup: {e}")


@pytest.mark.integration
def test_update_issue_body(test_owner, test_repo_name, unique_id, with_retry):
    """Test updating an issue's body."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (Update Body) {unique_id}"
    body = "Initial body"
    
    # Create issue
    @with_retry
    def create_test_issue():
        return create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title,
            body=body
        ))
    
    issue = create_test_issue()
    
    try:
        # Update issue body
        updated_body = f"Updated body at {datetime.now().isoformat()}"
        
        @with_retry
        def update_test_issue():
            return update_issue(UpdateIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"],
                body=updated_body
            ))
        
        updated = update_test_issue()
        
        # Verify
        assert updated["body"] == updated_body
        assert updated["title"] == title  # Title should not change
        assert updated["issue_number"] == issue["issue_number"]
        
        # Verify with get_issue
        @with_retry
        def get_test_issue():
            return get_issue(GetIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"]
            ))
        
        fetched = get_test_issue()
        assert fetched["body"] == updated_body
    finally:
        # Cleanup
        try:
            @with_retry
            def close_issue():
                return update_issue(UpdateIssueParams(
                    owner=owner,
                    repo=repo,
                    issue_number=issue["issue_number"],
                    state="closed"
                ))
            
            close_issue()
        except Exception as e:
            print(f"Failed to close issue during cleanup: {e}")


@pytest.mark.integration
def test_update_issue_state(test_owner, test_repo_name, unique_id, with_retry):
    """Test updating an issue's state (open/closed)."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (Update State) {unique_id}"
    
    # Create issue
    @with_retry
    def create_test_issue():
        return create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title
        ))
    
    issue = create_test_issue()
    assert issue["state"] == "open"
    
    try:
        # Close the issue
        @with_retry
        def close_test_issue():
            return update_issue(UpdateIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"],
                state="closed"
            ))
        
        closed = close_test_issue()
        
        # Verify
        assert closed["state"] == "closed"
        assert closed["title"] == title  # Title should not change
        
        # Verify with get_issue
        @with_retry
        def get_closed_issue():
            return get_issue(GetIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"]
            ))
        
        fetched_closed = get_closed_issue()
        assert fetched_closed["state"] == "closed"
        
        # Reopen the issue
        @with_retry
        def reopen_test_issue():
            return update_issue(UpdateIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"],
                state="open"
            ))
        
        reopened = reopen_test_issue()
        
        # Verify
        assert reopened["state"] == "open"
        
        # Verify with get_issue
        @with_retry
        def get_reopened_issue():
            return get_issue(GetIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"]
            ))
        
        fetched_reopened = get_reopened_issue()
        assert fetched_reopened["state"] == "open"
    finally:
        # Cleanup
        try:
            @with_retry
            def ensure_closed():
                return update_issue(UpdateIssueParams(
                    owner=owner,
                    repo=repo,
                    issue_number=issue["issue_number"],
                    state="closed"
                ))
            
            ensure_closed()
        except Exception as e:
            print(f"Failed to close issue during cleanup: {e}")


@pytest.mark.integration
def test_update_issue_labels(test_owner, test_repo_name, unique_id, with_retry):
    """Test updating an issue's labels."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (Update Labels) {unique_id}"
    
    # Create issue
    @with_retry
    def create_test_issue():
        return create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title
        ))
    
    issue = create_test_issue()
    
    try:
        # Update issue labels
        @with_retry
        def update_test_issue_labels():
            return update_issue(UpdateIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"],
                labels=["test-label", "bug"]
            ))
        
        updated = update_test_issue_labels()
        
        # Verify
        assert len(updated["labels"]) == 2
        label_names = [label["name"] for label in updated["labels"]]
        assert "test-label" in label_names
        assert "bug" in label_names
        
        # Update with different labels (should replace, not add)
        @with_retry
        def update_test_issue_labels_again():
            return update_issue(UpdateIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"],
                labels=["enhancement"]
            ))
        
        updated_again = update_test_issue_labels_again()
        
        # Verify
        assert len(updated_again["labels"]) == 1
        assert updated_again["labels"][0]["name"] == "enhancement"
    finally:
        # Cleanup
        try:
            @with_retry
            def close_issue():
                return update_issue(UpdateIssueParams(
                    owner=owner,
                    repo=repo,
                    issue_number=issue["issue_number"],
                    state="closed"
                ))
            
            close_issue()
        except Exception as e:
            print(f"Failed to close issue during cleanup: {e}")


@pytest.mark.integration
def test_update_issue_multiple_fields(test_owner, test_repo_name, unique_id, with_retry):
    """Test updating multiple issue fields at once."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (Update Multiple) {unique_id}"
    
    # Create issue
    @with_retry
    def create_test_issue():
        return create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title
        ))
    
    issue = create_test_issue()
    
    try:
        # Update multiple fields
        updated_title = f"Updated Title {unique_id}"
        updated_body = f"Updated body at {datetime.now().isoformat()}"
        
        @with_retry
        def update_test_issue_multiple():
            return update_issue(UpdateIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"],
                title=updated_title,
                body=updated_body,
                labels=["test-label"],
                assignees=[owner]  # Assign to the repo owner
            ))
        
        updated = update_test_issue_multiple()
        
        # Verify
        assert updated["title"] == updated_title
        assert updated["body"] == updated_body
        assert any(label["name"] == "test-label" for label in updated["labels"])
        assert any(assignee["login"] == owner for assignee in updated["assignees"])
    finally:
        # Cleanup
        try:
            @with_retry
            def close_issue():
                return update_issue(UpdateIssueParams(
                    owner=owner,
                    repo=repo,
                    issue_number=issue["issue_number"],
                    state="closed"
                ))
            
            close_issue()
        except Exception as e:
            print(f"Failed to close issue during cleanup: {e}")


@pytest.mark.integration
def test_update_issue_no_changes(test_owner, test_repo_name, unique_id, with_retry):
    """Test update_issue with no changes."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (No Changes) {unique_id}"
    
    # Create issue
    @with_retry
    def create_test_issue():
        return create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title
        ))
    
    issue = create_test_issue()
    
    try:
        # Update with no changes
        @with_retry
        def update_test_issue_no_changes():
            return update_issue(UpdateIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"]
            ))
        
        updated = update_test_issue_no_changes()
        
        # Verify
        assert updated["title"] == title
        assert updated["issue_number"] == issue["issue_number"]
        assert updated["state"] == "open"
    finally:
        # Cleanup
        try:
            @with_retry
            def close_issue():
                return update_issue(UpdateIssueParams(
                    owner=owner,
                    repo=repo,
                    issue_number=issue["issue_number"],
                    state="closed"
                ))
            
            close_issue()
        except Exception as e:
            print(f"Failed to close issue during cleanup: {e}")
