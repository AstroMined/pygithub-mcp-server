"""List issues integration tests.

This module tests the list_issues operation using the real GitHub API.
"""

import pytest
from datetime import datetime, timedelta

from pygithub_mcp_server.operations.issues import (
    create_issue,
    list_issues,
    update_issue,
)
from pygithub_mcp_server.schemas.issues import (
    CreateIssueParams,
    ListIssuesParams,
    UpdateIssueParams,
)


@pytest.mark.integration
def test_list_issues_basic(test_owner, test_repo_name, unique_id, with_retry):
    """Test basic list_issues functionality."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    
    # Create a test issue to ensure we have at least one
    title = f"Test Issue (List Basic) {unique_id}"
    
    @with_retry
    def create_test_issue():
        return create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title
        ))
    
    issue = create_test_issue()
    
    try:
        # List issues
        @with_retry
        def list_test_issues():
            return list_issues(ListIssuesParams(
                owner=owner,
                repo=repo,
                per_page=20,    # Limit results to avoid hanging
                page=1          # Only get first page
            ))
        
        issues = list_test_issues()
        
        # Verify
        assert isinstance(issues, list)
        assert len(issues) > 0
        
        # Verify our test issue is in the list
        found = False
        for i in issues:
            if i["issue_number"] == issue["issue_number"]:
                found = True
                assert i["title"] == title
                break
        
        assert found, "Test issue not found in list_issues results"
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
def test_list_issues_state_filter(test_owner, test_repo_name, unique_id, with_retry):
    """Test list_issues with state filter."""
    # Setup
    print("\n--- DEBUG: Starting test_list_issues_state_filter ---")
    owner = test_owner
    repo = test_repo_name
    
    # Create an open issue
    open_title = f"Test Issue (Open) {unique_id}"
    print(f"DEBUG: Creating open issue with title: {open_title}")
    
    try:
        @with_retry
        def create_open_issue():
            result = create_issue(CreateIssueParams(
                owner=owner,
                repo=repo,
                title=open_title
            ))
            print(f"DEBUG: Open issue created successfully with number: {result.get('issue_number', 'UNKNOWN')}")
            return result
        
        open_issue = create_open_issue()
        print(f"DEBUG: Open issue creation completed, issue number: {open_issue.get('issue_number', 'UNKNOWN')}")
    except Exception as e:
        print(f"DEBUG ERROR: Failed to create open issue: {type(e).__name__}: {str(e)}")
        raise
    
    # Create a closed issue
    closed_title = f"Test Issue (Closed) {unique_id}"
    print(f"DEBUG: Creating closed issue with title: {closed_title}")
    
    try:
        @with_retry
        def create_closed_issue():
            issue = create_issue(CreateIssueParams(
                owner=owner,
                repo=repo,
                title=closed_title
            ))
            print(f"DEBUG: Closed issue created, now closing it. Issue number: {issue.get('issue_number', 'UNKNOWN')}")
            
            update_issue(UpdateIssueParams(
                owner=owner,
                repo=repo,
                issue_number=issue["issue_number"],
                state="closed"
            ))
            print(f"DEBUG: Issue {issue.get('issue_number', 'UNKNOWN')} successfully closed")
            return issue
        
        closed_issue = create_closed_issue()
        print(f"DEBUG: Closed issue creation completed, issue number: {closed_issue.get('issue_number', 'UNKNOWN')}")
    except Exception as e:
        print(f"DEBUG ERROR: Failed to create/close issue: {type(e).__name__}: {str(e)}")
        raise
    
    try:
        # List open issues
        print("DEBUG: Listing open issues")
        try:
            @with_retry
            def list_open_issues():
                result = list_issues(ListIssuesParams(
                    owner=owner,
                    repo=repo,
                    state="open",
                    per_page=20,    # Limit results to avoid hanging
                    page=1          # Only get first page
                ))
                print(f"DEBUG: Retrieved {len(result)} open issues")
                return result
            
            open_issues = list_open_issues()
            print("DEBUG: Open issues listing completed")
        except Exception as e:
            print(f"DEBUG ERROR: Failed to list open issues: {type(e).__name__}: {str(e)}")
            raise
        
        # Verify open issue is in the list
        print("DEBUG: Verifying open issue is in the list")
        found_open = False
        for i in open_issues:
            if i["issue_number"] == open_issue["issue_number"]:
                found_open = True
                assert i["state"] == "open"
                break
        
        assert found_open, "Open test issue not found in open issues list"
        print("DEBUG: Open issue verification passed")
        
        # Verify closed issue is not in the list
        print("DEBUG: Verifying closed issue is NOT in the open issues list")
        for i in open_issues:
            assert i["issue_number"] != closed_issue["issue_number"], "Closed issue found in open issues list"
        print("DEBUG: Closed issue verification passed (not in open issues)")
        
        # List closed issues
        print("DEBUG: Listing closed issues")
        try:
            @with_retry
            def list_closed_issues():
                result = list_issues(ListIssuesParams(
                    owner=owner,
                    repo=repo,
                    state="closed",
                    per_page=20,    # Limit results to avoid hanging
                    page=1          # Only get first page
                ))
                print(f"DEBUG: Retrieved {len(result)} closed issues")
                return result
            
            closed_issues = list_closed_issues()
            print("DEBUG: Closed issues listing completed")
        except Exception as e:
            print(f"DEBUG ERROR: Failed to list closed issues: {type(e).__name__}: {str(e)}")
            raise
        
        # Verify closed issue is in the list
        print("DEBUG: Verifying closed issue is in the list")
        found_closed = False
        for i in closed_issues:
            if i["issue_number"] == closed_issue["issue_number"]:
                found_closed = True
                assert i["state"] == "closed"
                break
        
        assert found_closed, "Closed test issue not found in closed issues list"
        print("DEBUG: Closed issue verification passed")
        
        # Verify open issue is not in the list
        print("DEBUG: Verifying open issue is NOT in the closed issues list")
        for i in closed_issues:
            assert i["issue_number"] != open_issue["issue_number"], "Open issue found in closed issues list"
        print("DEBUG: Open issue verification passed (not in closed issues)")
        
        # List all issues
        print("DEBUG: Listing all issues")
        try:
            @with_retry
            def list_all_issues():
                result = list_issues(ListIssuesParams(
                    owner=owner,
                    repo=repo,
                    state="all",
                    per_page=20,    # Limit results to avoid hanging
                    page=1          # Only get first page
                ))
                print(f"DEBUG: Retrieved {len(result)} total issues")
                return result
            
            all_issues = list_all_issues()
            print("DEBUG: All issues listing completed")
        except Exception as e:
            print(f"DEBUG ERROR: Failed to list all issues: {type(e).__name__}: {str(e)}")
            raise
        
        # Verify both issues are in the list
        print("DEBUG: Verifying both issues are in the 'all issues' list")
        found_open = False
        found_closed = False
        for i in all_issues:
            if i["issue_number"] == open_issue["issue_number"]:
                found_open = True
                print(f"DEBUG: Found open issue {open_issue['issue_number']} in all issues list")
            elif i["issue_number"] == closed_issue["issue_number"]:
                found_closed = True
                print(f"DEBUG: Found closed issue {closed_issue['issue_number']} in all issues list")
        
        assert found_open, "Open test issue not found in all issues list"
        assert found_closed, "Closed test issue not found in all issues list"
        print("DEBUG: Both issues verification passed")
    finally:
        # Cleanup
        print("DEBUG: Starting cleanup")
        try:
            @with_retry
            def close_open_issue():
                result = update_issue(UpdateIssueParams(
                    owner=owner,
                    repo=repo,
                    issue_number=open_issue["issue_number"],
                    state="closed"
                ))
                print(f"DEBUG: Successfully closed open issue {open_issue['issue_number']} during cleanup")
                return result
            
            close_open_issue()
        except Exception as e:
            print(f"DEBUG ERROR: Failed to close open issue during cleanup: {type(e).__name__}: {str(e)}")

        print("DEBUG: Test completed")


@pytest.mark.integration
def test_list_issues_pagination(test_owner, test_repo_name, unique_id, with_retry):
    """Test list_issues pagination with dynamic expectations."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    
    # Create a test issue to ensure we have at least one
    title = f"Test Issue (Pagination) {unique_id}"
    
    @with_retry
    def create_test_issue():
        return create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title
        ))
    
    issue = create_test_issue()
    
    try:
        # Use a reasonable per_page value that works with real-world repositories
        per_page_value = 5
        
        # Get first page of issues
        @with_retry
        def list_test_issues_page1():
            return list_issues(ListIssuesParams(
                owner=owner,
                repo=repo,
                page=1,
                per_page=per_page_value
            ))
        
        page1 = list_test_issues_page1()
        
        # Get second page of issues
        @with_retry
        def list_test_issues_page2():
            return list_issues(ListIssuesParams(
                owner=owner,
                repo=repo,
                page=2,
                per_page=per_page_value
            ))
        
        page2 = list_test_issues_page2()
        
        # Verify pagination mechanics work
        # 1. Check per_page limit is respected
        assert isinstance(page1, list)
        assert len(page1) <= per_page_value, f"Page 1 should contain at most {per_page_value} issues"
        
        # 2. Verify our test issue is in the results (in either page)
        found = False
        for i in page1 + page2:
            if i["issue_number"] == issue["issue_number"]:
                found = True
                assert i["title"] == title
                break
        
        assert found, "Test issue not found in paginated results"
        
        # 3. If we have enough data, verify pages are different
        if len(page1) == per_page_value and len(page2) > 0:
            # Extract issue numbers for better comparison
            page1_ids = {i["issue_number"] for i in page1}
            page2_ids = {i["issue_number"] for i in page2}
            # There should be at least some difference between pages
            assert page1_ids != page2_ids, "Page 1 and Page 2 contain identical issues"
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
def test_list_issues_labels_filter(test_owner, test_repo_name, unique_id, with_retry):
    """Test list_issues with labels filter."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    
    # Create an issue with labels
    title = f"Test Issue (Labels Filter) {unique_id}"
    
    @with_retry
    def create_test_issue():
        issue = create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title
        ))
        update_issue(UpdateIssueParams(
            owner=owner,
            repo=repo,
            issue_number=issue["issue_number"],
            labels=["bug", "test-label"]
        ))
        return issue
    
    issue = create_test_issue()
    
    try:
        # List issues with bug label
        @with_retry
        def list_bug_issues():
            return list_issues(ListIssuesParams(
                owner=owner,
                repo=repo,
                labels=["bug"],
                per_page=20,    # Limit results to avoid hanging
                page=1          # Only get first page
            ))
        
        bug_issues = list_bug_issues()
        
        # Verify our issue is in the list
        found = False
        for i in bug_issues:
            if i["issue_number"] == issue["issue_number"]:
                found = True
                label_names = [label["name"] for label in i["labels"]]
                assert "bug" in label_names
                break
        
        assert found, "Test issue not found in bug label filter results"
        
        # List issues with test-label
        @with_retry
        def list_test_label_issues():
            return list_issues(ListIssuesParams(
                owner=owner,
                repo=repo,
                labels=["test-label"],
                per_page=20,    # Limit results to avoid hanging
                page=1          # Only get first page
            ))
        
        test_label_issues = list_test_label_issues()
        
        # Verify our issue is in the list
        found = False
        for i in test_label_issues:
            if i["issue_number"] == issue["issue_number"]:
                found = True
                label_names = [label["name"] for label in i["labels"]]
                assert "test-label" in label_names
                break
        
        assert found, "Test issue not found in test-label filter results"
        
        # List issues with non-existent label
        @with_retry
        def list_nonexistent_label_issues():
            return list_issues(ListIssuesParams(
                owner=owner,
                repo=repo,
                labels=[f"nonexistent-{unique_id}"],
                per_page=20,    # Limit results to avoid hanging
                page=1          # Only get first page
            ))
        
        nonexistent_label_issues = list_nonexistent_label_issues()
        
        # Verify our issue is not in the list
        for i in nonexistent_label_issues:
            assert i["issue_number"] != issue["issue_number"], "Issue found with non-existent label"
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
def test_list_issues_sort_and_direction(test_owner, test_repo_name, unique_id, with_retry):
    """Test list_issues with sort and direction parameters."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    
    # Create two issues with different timestamps
    title1 = f"Test Issue 1 (Sort) {unique_id}"
    
    @with_retry
    def create_test_issue1():
        return create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title1
        ))
    
    issue1 = create_test_issue1()
    
    # Wait a bit to ensure different timestamps
    import time
    time.sleep(2)
    
    title2 = f"Test Issue 2 (Sort) {unique_id}"
    
    @with_retry
    def create_test_issue2():
        return create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title2
        ))
    
    issue2 = create_test_issue2()
    
    try:
        # List issues sorted by created, ascending
        @with_retry
        def list_created_asc():
            return list_issues(ListIssuesParams(
                owner=owner,
                repo=repo,
                sort="created",
                direction="asc",
                per_page=20,    # Limit results to avoid hanging
                page=1          # Only get first page
            ))
        
        created_asc = list_created_asc()
        
        # Find positions of our test issues
        pos1 = None
        pos2 = None
        for i, issue in enumerate(created_asc):
            if issue["issue_number"] == issue1["issue_number"]:
                pos1 = i
            elif issue["issue_number"] == issue2["issue_number"]:
                pos2 = i
            
            if pos1 is not None and pos2 is not None:
                break
        
        # Verify issue1 comes before issue2 in ascending order
        if pos1 is not None and pos2 is not None:
            assert pos1 < pos2, "Issues not in ascending order by created date"
        
        # List issues sorted by created, descending
        @with_retry
        def list_created_desc():
            return list_issues(ListIssuesParams(
                owner=owner,
                repo=repo,
                sort="created",
                direction="desc",
                per_page=20,    # Limit results to avoid hanging
                page=1          # Only get first page
            ))
        
        created_desc = list_created_desc()
        
        # Find positions of our test issues
        pos1 = None
        pos2 = None
        for i, issue in enumerate(created_desc):
            if issue["issue_number"] == issue1["issue_number"]:
                pos1 = i
            elif issue["issue_number"] == issue2["issue_number"]:
                pos2 = i
            
            if pos1 is not None and pos2 is not None:
                break
        
        # Verify issue2 comes before issue1 in descending order
        if pos1 is not None and pos2 is not None:
            assert pos2 < pos1, "Issues not in descending order by created date"
    finally:
        # Cleanup
        try:
            @with_retry
            def close_issues():
                update_issue(UpdateIssueParams(
                    owner=owner,
                    repo=repo,
                    issue_number=issue1["issue_number"],
                    state="closed"
                ))
                update_issue(UpdateIssueParams(
                    owner=owner,
                    repo=repo,
                    issue_number=issue2["issue_number"],
                    state="closed"
                ))
            
            close_issues()
        except Exception as e:
            print(f"Failed to close issues during cleanup: {e}")


@pytest.mark.integration
def test_list_issues_since(test_owner, test_repo_name, unique_id, with_retry):
    """Test list_issues with since parameter."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    
    # Create an issue
    title = f"Test Issue (Since) {unique_id}"
    
    @with_retry
    def create_test_issue():
        return create_issue(CreateIssueParams(
            owner=owner,
            repo=repo,
            title=title
        ))
    
    issue = create_test_issue()
    
    # Get the current time
    now = datetime.now()
    
    # Set since to 1 hour ago
    since = now - timedelta(hours=1)
    
    try:
        # List issues since 1 hour ago
        @with_retry
        def list_issues_since():
            return list_issues(ListIssuesParams(
                owner=owner,
                repo=repo,
                since=since.isoformat() + "Z",  # Add UTC timezone indicator
                per_page=20,    # Limit results to avoid hanging
                page=1          # Only get first page
            ))
        
        recent_issues = list_issues_since()
        
        # Verify our issue is in the list
        found = False
        for i in recent_issues:
            if i["issue_number"] == issue["issue_number"]:
                found = True
                break
        
        assert found, "Test issue not found in since filter results"
        
        # Set since to 24 hours in the future to ensure timezone differences are covered
        future = now + timedelta(hours=24)
        
        # List issues since 1 hour in the future
        @with_retry
        def list_issues_future():
            return list_issues(ListIssuesParams(
                owner=owner,
                repo=repo,
                since=future.isoformat() + "Z",  # Add UTC timezone indicator
                per_page=20,    # Limit results to avoid hanging
                page=1          # Only get first page
            ))
        
        future_issues = list_issues_future()
        
        # Verify our issue is not in the list
        for i in future_issues:
            assert i["issue_number"] != issue["issue_number"], "Issue found with future since filter"
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
