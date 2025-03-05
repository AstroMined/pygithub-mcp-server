"""Issue labels integration tests.

This module tests the issue label operations using the real GitHub API.
"""

import pytest
from datetime import datetime

from pygithub_mcp_server.operations.issues import (
    create_issue,
    update_issue,
    add_issue_labels,
    remove_issue_label,
)
from pygithub_mcp_server.schemas.issues import (
    CreateIssueParams,
    UpdateIssueParams,
    AddIssueLabelsParams,
    RemoveIssueLabelParams,
)


@pytest.mark.integration
def test_add_issue_labels(test_owner, test_repo_name, unique_id, with_retry):
    """Test adding labels to an issue."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (Add Labels) {unique_id}"
    
    # Create an issue
    @with_retry
    def create_test_issue():
        return create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title
        ))
    
    issue = create_test_issue()
    
    try:
        # Add labels
        @with_retry
        def add_test_labels():
            return add_issue_labels(AddIssueLabelsParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"],
                labels=["bug", "enhancement"]
            ))
        
        labels = add_test_labels()
        
        # Verify
        assert isinstance(labels, list)
        assert len(labels) >= 2
        
        label_names = [label["name"] for label in labels]
        assert "bug" in label_names
        assert "enhancement" in label_names
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
def test_remove_issue_label(test_owner, test_repo_name, unique_id, with_retry):
    """Test removing a label from an issue."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (Remove Label) {unique_id}"
    
    # Create an issue with labels
    @with_retry
    def create_test_issue():
        issue = create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title
        ))
        add_issue_labels(AddIssueLabelsParams(
            owner=owner,
            repo=repo,
            issue_number=issue["issue_number"],
            labels=["bug", "enhancement"]
        ))
        return issue
    
    issue = create_test_issue()
    
    try:
        # Verify labels were added
        @with_retry
        def get_issue_with_labels():
            return update_issue(UpdateIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"]
            ))  # Using update with no changes to get current state
        
        issue_with_labels = get_issue_with_labels()
        label_names = [label["name"] for label in issue_with_labels["labels"]]
        assert "bug" in label_names
        assert "enhancement" in label_names
        
        # Remove one label
        @with_retry
        def remove_test_label():
            return remove_issue_label(RemoveIssueLabelParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"],
                label="bug"
            ))
        
        remove_test_label()
        
        # Verify label was removed
        @with_retry
        def get_issue_after_remove():
            return update_issue(UpdateIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"]
            ))  # Using update with no changes to get current state
        
        issue_after_remove = get_issue_after_remove()
        label_names_after = [label["name"] for label in issue_after_remove["labels"]]
        assert "bug" not in label_names_after
        assert "enhancement" in label_names_after
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
def test_add_issue_labels_multiple_calls(test_owner, test_repo_name, unique_id, with_retry):
    """Test adding labels to an issue with multiple calls."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (Add Labels Multiple) {unique_id}"
    
    # Create an issue
    @with_retry
    def create_test_issue():
        return create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title
        ))
    
    issue = create_test_issue()
    
    try:
        # Add first label
        @with_retry
        def add_first_label():
            return add_issue_labels(AddIssueLabelsParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"],
                labels=["bug"]
            ))
        
        first_labels = add_first_label()
        
        # Verify
        assert isinstance(first_labels, list)
        assert any(label["name"] == "bug" for label in first_labels)
        
        # Add second label
        @with_retry
        def add_second_label():
            return add_issue_labels(AddIssueLabelsParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"],
                labels=["enhancement"]
            ))
        
        second_labels = add_second_label()
        
        # Verify both labels are present
        assert isinstance(second_labels, list)
        label_names = [label["name"] for label in second_labels]
        assert "bug" in label_names
        assert "enhancement" in label_names
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
def test_remove_nonexistent_label(test_owner, test_repo_name, unique_id, with_retry):
    """Test removing a non-existent label from an issue."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (Remove Nonexistent Label) {unique_id}"
    
    # Create an issue
    @with_retry
    def create_test_issue():
        return create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title
        ))
    
    issue = create_test_issue()
    
    try:
        # Remove a non-existent label
        nonexistent_label = f"nonexistent-{unique_id}"
        
        @with_retry
        def remove_nonexistent_label():
            # This should not raise an error, GitHub API silently ignores removing non-existent labels
            return remove_issue_label(RemoveIssueLabelParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"],
                label=nonexistent_label
            ))
        
        # This should not raise an exception
        remove_nonexistent_label()
        
        # Verify issue state is still accessible
        @with_retry
        def get_issue_after_remove():
            return update_issue(UpdateIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"]
            ))  # Using update with no changes to get current state
        
        issue_after_remove = get_issue_after_remove()
        assert issue_after_remove["issue_number"] == issue["issue_number"]
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
def test_label_lifecycle(test_owner, test_repo_name, unique_id, with_retry):
    """Test complete label lifecycle (add → verify → remove → verify)."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (Label Lifecycle) {unique_id}"
    
    # Create an issue
    @with_retry
    def create_test_issue():
        return create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title
        ))
    
    issue = create_test_issue()
    
    try:
        # Verify no labels initially
        assert not issue["labels"], "Issue should not have labels initially"
        
        # Add labels
        @with_retry
        def add_test_labels():
            return add_issue_labels(AddIssueLabelsParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"],
                labels=["bug", "enhancement", "documentation"]
            ))
        
        labels = add_test_labels()
        
        # Verify labels were added
        assert len(labels) >= 3
        label_names = [label["name"] for label in labels]
        assert "bug" in label_names
        assert "enhancement" in label_names
        assert "documentation" in label_names
        
        # Remove one label
        @with_retry
        def remove_bug_label():
            return remove_issue_label(RemoveIssueLabelParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"],
                label="bug"
            ))
        
        remove_bug_label()
        
        # Verify label was removed
        @with_retry
        def get_issue_after_remove():
            return update_issue(UpdateIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"]
            ))  # Using update with no changes to get current state
        
        issue_after_remove = get_issue_after_remove()
        label_names_after = [label["name"] for label in issue_after_remove["labels"]]
        assert "bug" not in label_names_after
        assert "enhancement" in label_names_after
        assert "documentation" in label_names_after
        
        # Remove another label
        @with_retry
        def remove_enhancement_label():
            return remove_issue_label(RemoveIssueLabelParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"],
                label="enhancement"
            ))
        
        remove_enhancement_label()
        
        # Verify second label was removed
        @with_retry
        def get_issue_after_second_remove():
            return update_issue(UpdateIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"]
            ))
        
        issue_after_second_remove = get_issue_after_second_remove()
        label_names_after_second = [label["name"] for label in issue_after_second_remove["labels"]]
        assert "bug" not in label_names_after_second
        assert "enhancement" not in label_names_after_second
        assert "documentation" in label_names_after_second
        
        # Remove last label
        @with_retry
        def remove_documentation_label():
            return remove_issue_label(RemoveIssueLabelParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"],
                label="documentation"
            ))
        
        remove_documentation_label()
        
        # Verify all labels are removed
        @with_retry
        def get_issue_after_all_removed():
            return update_issue(UpdateIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"]
            ))
        
        issue_after_all_removed = get_issue_after_all_removed()
        assert not issue_after_all_removed["labels"], "All labels should be removed"
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
