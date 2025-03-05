"""Simple test to isolate the issue."""

import pytest
import logging
import time

from pygithub_mcp_server.schemas.issues import (
    CreateIssueParams,
    ListIssuesParams,
    UpdateIssueParams,
)
from pygithub_mcp_server.operations.issues import (
    create_issue,
    list_issues,
    update_issue,
)

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Make sure we see debug output
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

@pytest.mark.integration
def test_simple_issue_creation(test_owner, test_repo_name, unique_id, with_retry):
    """Simple test to verify issue creation works."""
    print("DEBUG: Starting simple test")
    
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Simple Test Issue {unique_id}"
    
    # Create a test issue
    print(f"DEBUG: Creating issue with title: {title}")
    issue = create_issue(CreateIssueParams(
        owner=owner,
        repo=repo,
        title=title
    ))
    
    print(f"DEBUG: Issue created with number: {issue.get('issue_number', 'UNKNOWN')}")
    
    # Clean up
    print("DEBUG: Cleaning up the issue")
    update_issue(UpdateIssueParams(
        owner=owner,
        repo=repo,
        issue_number=issue["issue_number"],
        state="closed"
    ))
    
    print("DEBUG: Test completed successfully")
    
    # Basic assertion to make the test pass
    assert "issue_number" in issue


@pytest.mark.integration
def test_simple_list_issues(test_owner, test_repo_name, unique_id, with_retry):
    """Test listing issues."""
    print("DEBUG: Starting simple list issues test")
    
    # Setup
    owner = test_owner
    repo = test_repo_name
    
    # Create a test issue
    title = f"List Test Issue {unique_id}"
    print(f"DEBUG: Creating issue with title: {title}")
    issue = create_issue(CreateIssueParams(
        owner=owner,
        repo=repo,
        title=title
    ))
    
    print(f"DEBUG: Issue created with number: {issue['issue_number']}")
    
    try:
        # List issues
        print("DEBUG: Listing issues")
        issues = list_issues(ListIssuesParams(
            owner=owner,
            repo=repo
        ))
        
        print(f"DEBUG: Listed {len(issues)} issues")
        
        # Verify our test issue is in the list
        found = False
        for i in issues:
            if i["issue_number"] == issue["issue_number"]:
                found = True
                print(f"DEBUG: Found our test issue in the list")
                assert i["title"] == title
                break
        
        assert found, "Test issue not found in list_issues results"
        print("DEBUG: Issue verification successful")
        
    finally:
        # Clean up
        print("DEBUG: Cleaning up the issue")
        update_issue(UpdateIssueParams(
            owner=owner,
            repo=repo,
            issue_number=issue["issue_number"],
            state="closed"
        ))
        
        print("DEBUG: Test completed successfully")


@pytest.mark.integration
def test_list_issues_with_state(test_owner, test_repo_name, unique_id, with_retry):
    """Test listing issues with state filter."""
    print("\n--- DEBUG: Starting test_list_issues_with_state ---")
    
    # Setup
    owner = test_owner
    repo = test_repo_name
    
    # Create an open issue
    open_title = f"Open Issue {unique_id}"
    print(f"DEBUG: Creating open issue with title: {open_title}")
    open_issue = create_issue(CreateIssueParams(
        owner=owner,
        repo=repo,
        title=open_title
    ))
    print(f"DEBUG: Open issue created with number: {open_issue['issue_number']}")
    
    # Create and immediately close an issue
    closed_title = f"Closed Issue {unique_id}"
    print(f"DEBUG: Creating closed issue with title: {closed_title}")
    closed_issue = create_issue(CreateIssueParams(
        owner=owner,
        repo=repo,
        title=closed_title
    ))
    print(f"DEBUG: Closed issue created with number: {closed_issue['issue_number']}")
    
    # Close the issue
    print(f"DEBUG: Closing issue {closed_issue['issue_number']}")
    update_issue(UpdateIssueParams(
        owner=owner,
        repo=repo,
        issue_number=closed_issue["issue_number"],
        state="closed"
    ))
    print(f"DEBUG: Issue {closed_issue['issue_number']} closed successfully")
    
    # Wait a moment for GitHub API to process the state change
    print("DEBUG: Waiting for API to process state changes...")
    time.sleep(2)
    
    try:
        # Test each state filter separately to isolate the issue, but with pagination limits
        # since the repository has hundreds of issues
        
        # 1. First, get a limited set of issues without a state filter
        print("DEBUG: Listing limited issues without state filter")
        all_issues = list_issues(ListIssuesParams(
            owner=owner,
            repo=repo,
            per_page=10,  # Limit to just 10 issues
            page=1        # Just get the first page
        ))
        print(f"DEBUG: Listed {len(all_issues)} issues without state filter")
        
        # 2. Now test with explicit "open" state - this should find our open issue
        print("DEBUG: Listing open issues")
        open_issues = list_issues(ListIssuesParams(
            owner=owner,
            repo=repo,
            state="open",
            per_page=10,
            page=1
        ))
        print(f"DEBUG: Listed {len(open_issues)} open issues")
        
        # Verify our open issue is in the list
        found_open = False
        for i in open_issues:
            if i["issue_number"] == open_issue["issue_number"]:
                found_open = True
                print(f"DEBUG: Found our open issue in open issues list")
                break
        assert found_open, "Open test issue not found in open issues list"
        
        # 3. Test with closed state - should find our closed issue
        print("DEBUG: Listing closed issues (limited)")
        closed_issues = list_issues(ListIssuesParams(
            owner=owner,
            repo=repo,
            state="closed",
            per_page=20,   # Use a slightly higher limit as there are more closed issues
            page=1
        ))
        print(f"DEBUG: Listed {len(closed_issues)} closed issues")
        
        # Since our closed issue was just created, it should be near the top of the list
        found_closed = False
        for i in closed_issues:
            if i["issue_number"] == closed_issue["issue_number"]:
                found_closed = True
                print(f"DEBUG: Found our closed issue in closed issues list")
                break
        assert found_closed, "Closed test issue not found in closed issues list"
        
        # 4. Test with "all" state - both issues should be found
        print("DEBUG: Listing 'all' issues (limited)")
        all_state_issues = list_issues(ListIssuesParams(
            owner=owner,
            repo=repo,
            state="all",
            per_page=20,
            page=1
        ))
        print(f"DEBUG: Listed {len(all_state_issues)} issues with 'all' state")
        
        print("DEBUG: All state filter tests completed successfully")
    finally:
        # Clean up
        print("DEBUG: Cleaning up issues")
        update_issue(UpdateIssueParams(
            owner=owner,
            repo=repo,
            issue_number=open_issue["issue_number"],
            state="closed"
        ))
        print("DEBUG: Cleanup completed successfully")
