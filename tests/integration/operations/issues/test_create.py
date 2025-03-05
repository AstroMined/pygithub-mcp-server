"""Tests for issue creation operations.

This module tests the issue creation operations with various parameters.
"""

import pytest
from datetime import datetime

from pygithub_mcp_server.operations.issues import create_issue, get_issue
from pygithub_mcp_server.schemas.issues import CreateIssueParams, GetIssueParams


@pytest.mark.integration
def test_create_issue_required_params(test_owner, test_repo_name, unique_id, with_retry):
    """Test creating an issue with only required parameters."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (Required Params) {unique_id}"
    
    # Create an issue with only required parameters
    @with_retry
    def create_test_issue():
        return create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title
        ))
    
    issue = create_test_issue()
    
    # Verify
    assert issue["title"] == title
    assert "issue_number" in issue
    assert "created_at" in issue
    assert "user" in issue
    
    # Verify issue state is 'open' by default
    assert issue["state"] == "open"
    
    # Verify empty fields have appropriate defaults
    assert not issue["body"] or issue["body"] == ""
    assert not issue["labels"] or len(issue["labels"]) == 0
    assert not issue["assignees"] or len(issue["assignees"]) == 0
    assert issue["milestone"] is None


@pytest.mark.integration
def test_create_issue_all_params(test_owner, test_repo_name, unique_id, with_retry):
    """Test creating an issue with all parameters."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (All Params) {unique_id}"
    body = f"This is a test issue created at {datetime.now().isoformat()}"
    labels = ["bug", "question"]  # These labels must exist in the test repo
    assignees = [test_owner]  # Self-assign for testing
    
    # Create an issue with all parameters
    @with_retry
    def create_test_issue():
        return create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title,
            body=body,
            labels=labels,
            assignees=assignees
        ))
    
    issue = create_test_issue()
    
    # Verify
    assert issue["title"] == title
    assert issue["body"] == body
    assert "issue_number" in issue
    assert "created_at" in issue
    assert "user" in issue
    
    # Verify issue state is 'open' by default
    assert issue["state"] == "open"
    
    # Verify labels and assignees
    assert len(issue["labels"]) > 0
    for label in issue["labels"]:
        assert label["name"] in labels
        
    assert len(issue["assignees"]) > 0
    for assignee in issue["assignees"]:
        assert assignee["login"] in assignees


@pytest.mark.integration
def test_create_and_verify_issue(test_owner, test_repo_name, unique_id, with_retry):
    """Test creating an issue and then verifying it with get_issue."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue (Create & Verify) {unique_id}"
    body = f"This is a test issue created at {datetime.now().isoformat()}"
    
    # Create an issue
    @with_retry
    def create_test_issue():
        return create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title,
            body=body
        ))
    
    created_issue = create_test_issue()
    issue_number = created_issue["issue_number"]
    
    # Get the issue to verify it was created correctly
    @with_retry
    def get_test_issue():
        return get_issue(GetIssueParams(
            owner=owner,
            repo=repo,
            issue_number=issue_number
        ))
    
    retrieved_issue = get_test_issue()
    
    # Verify the retrieved issue matches what we created
    assert retrieved_issue["issue_number"] == issue_number
    assert retrieved_issue["title"] == title
    assert retrieved_issue["body"] == body
    assert retrieved_issue["state"] == "open"
