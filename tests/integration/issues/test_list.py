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
        return create_issue(owner, repo, title)
    
    issue = create_test_issue()
    
    try:
        # List issues
        @with_retry
        def list_test_issues():
            return list_issues(owner, repo)
        
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
                return update_issue(owner, repo, issue["issue_number"], state="closed")
            
            close_issue()
        except Exception as e:
            print(f"Failed to close issue during cleanup: {e}")


@pytest.mark.integration
def test_list_issues_state_filter(test_owner, test_repo_name, unique_id, with_retry):
    """Test list_issues with state filter."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    
    # Create an open issue
    open_title = f"Test Issue (Open) {unique_id}"
    
    @with_retry
    def create_open_issue():
        return create_issue(owner, repo, open_title)
    
    open_issue = create_open_issue()
    
    # Create a closed issue
    closed_title = f"Test Issue (Closed) {unique_id}"
    
    @with_retry
    def create_closed_issue():
        issue = create_issue(owner, repo, closed_title)
        update_issue(owner, repo, issue["issue_number"], state="closed")
        return issue
    
    closed_issue = create_closed_issue()
    
    try:
        # List open issues
        @with_retry
        def list_open_issues():
            return list_issues(owner, repo, state="open")
        
        open_issues = list_open_issues()
        
        # Verify open issue is in the list
        found_open = False
        for i in open_issues:
            if i["issue_number"] == open_issue["issue_number"]:
                found_open = True
                assert i["state"] == "open"
                break
        
        assert found_open, "Open test issue not found in open issues list"
        
        # Verify closed issue is not in the list
        for i in open_issues:
            assert i["issue_number"] != closed_issue["issue_number"], "Closed issue found in open issues list"
        
        # List closed issues
        @with_retry
        def list_closed_issues():
            return list_issues(owner, repo, state="closed")
        
        closed_issues = list_closed_issues()
        
        # Verify closed issue is in the list
        found_closed = False
        for i in closed_issues:
            if i["issue_number"] == closed_issue["issue_number"]:
                found_closed = True
                assert i["state"] == "closed"
                break
        
        assert found_closed, "Closed test issue not found in closed issues list"
        
        # Verify open issue is not in the list
        for i in closed_issues:
            assert i["issue_number"] != open_issue["issue_number"], "Open issue found in closed issues list"
        
        # List all issues
        @with_retry
        def list_all_issues():
            return list_issues(owner, repo, state="all")
        
        all_issues = list_all_issues()
        
        # Verify both issues are in the list
        found_open = False
        found_closed = False
        for i in all_issues:
            if i["issue_number"] == open_issue["issue_number"]:
                found_open = True
            elif i["issue_number"] == closed_issue["issue_number"]:
                found_closed = True
        
        assert found_open, "Open test issue not found in all issues list"
        assert found_closed, "Closed test issue not found in all issues list"
    finally:
        # Cleanup
        try:
            @with_retry
            def close_open_issue():
                return update_issue(owner, repo, open_issue["issue_number"], state="closed")
            
            close_open_issue()
        except Exception as e:
            print(f"Failed to close open issue during cleanup: {e}")


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
        return create_issue(owner, repo, title)
    
    issue = create_test_issue()
    
    try:
        # Use a reasonable per_page value that works with real-world repositories
        per_page_value = 5
        
        # Get first page of issues
        @with_retry
        def list_test_issues_page1():
            return list_issues(owner, repo, page=1, per_page=per_page_value)
        
        page1 = list_test_issues_page1()
        
        # Get second page of issues
        @with_retry
        def list_test_issues_page2():
            return list_issues(owner, repo, page=2, per_page=per_page_value)
        
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
                return update_issue(owner, repo, issue["issue_number"], state="closed")
            
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
        issue = create_issue(owner, repo, title)
        update_issue(owner, repo, issue["issue_number"], labels=["bug", "test-label"])
        return issue
    
    issue = create_test_issue()
    
    try:
        # List issues with bug label
        @with_retry
        def list_bug_issues():
            return list_issues(owner, repo, labels=["bug"])
        
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
            return list_issues(owner, repo, labels=["test-label"])
        
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
            return list_issues(owner, repo, labels=[f"nonexistent-{unique_id}"])
        
        nonexistent_label_issues = list_nonexistent_label_issues()
        
        # Verify our issue is not in the list
        for i in nonexistent_label_issues:
            assert i["issue_number"] != issue["issue_number"], "Issue found with non-existent label"
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
def test_list_issues_sort_and_direction(test_owner, test_repo_name, unique_id, with_retry):
    """Test list_issues with sort and direction parameters."""
    # Setup
    owner = test_owner
    repo = test_repo_name
    
    # Create two issues with different timestamps
    title1 = f"Test Issue 1 (Sort) {unique_id}"
    
    @with_retry
    def create_test_issue1():
        return create_issue(owner, repo, title1)
    
    issue1 = create_test_issue1()
    
    # Wait a bit to ensure different timestamps
    import time
    time.sleep(2)
    
    title2 = f"Test Issue 2 (Sort) {unique_id}"
    
    @with_retry
    def create_test_issue2():
        return create_issue(owner, repo, title2)
    
    issue2 = create_test_issue2()
    
    try:
        # List issues sorted by created, ascending
        @with_retry
        def list_created_asc():
            return list_issues(owner, repo, sort="created", direction="asc")
        
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
            return list_issues(owner, repo, sort="created", direction="desc")
        
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
                update_issue(owner, repo, issue1["issue_number"], state="closed")
                update_issue(owner, repo, issue2["issue_number"], state="closed")
            
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
        return create_issue(owner, repo, title)
    
    issue = create_test_issue()
    
    # Get the current time
    now = datetime.now()
    
    # Set since to 1 hour ago
    since = now - timedelta(hours=1)
    
    try:
        # List issues since 1 hour ago
        @with_retry
        def list_issues_since():
            return list_issues(owner, repo, since=since.isoformat())
        
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
            return list_issues(owner, repo, since=future.isoformat())
        
        future_issues = list_issues_future()
        
        # Verify our issue is not in the list
        for i in future_issues:
            assert i["issue_number"] != issue["issue_number"], "Issue found with future since filter"
    finally:
        # Cleanup
        try:
            @with_retry
            def close_issue():
                return update_issue(owner, repo, issue["issue_number"], state="closed")
            
            close_issue()
        except Exception as e:
            print(f"Failed to close issue during cleanup: {e}")
