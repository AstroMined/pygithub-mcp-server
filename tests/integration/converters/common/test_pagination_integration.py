"""Integration tests for pagination utilities with real GitHub API.

This module tests the pagination utility functions using the real GitHub API,
adhering to ADR-002: Real API Testing approach.
"""

import pytest
import time
from random import randint

from github import GithubException

from pygithub_mcp_server.client import GitHubClient
from pygithub_mcp_server.converters.common.pagination import get_paginated_items
from pygithub_mcp_server.converters.issues.issues import convert_issue


@pytest.mark.integration
def test_pagination_with_real_api(test_owner, test_repo_name, unique_id, with_retry):
    """Test pagination utility with real GitHub API calls."""
    # Setup - create a set of issues to paginate
    issues_to_create = 3
    created_issues = []
    
    client = GitHubClient.get_instance()
    repository = client.get_repo(f"{test_owner}/{test_repo_name}")
    
    try:
        # Create test issues
        for i in range(issues_to_create):
            @with_retry
            def create_test_issue():
                title = f"Test Issue {i} for Pagination {unique_id}"
                issue = repository.create_issue(title=title)
                return issue
            
            issue = create_test_issue()
            created_issues.append(issue)
            
            # Add a small delay to ensure different timestamps
            time.sleep(1)
        
        # Get issues using the GitHub API
        @with_retry
        def get_paginated_issues():
            paginated_issues = repository.get_issues(state="open")
            return paginated_issues
        
        paginated_issues = get_paginated_issues()
        
        # Test pagination utility with different parameters
        # Test 1: Get all issues
        @with_retry
        def get_all_issues():
            all_issues = get_paginated_items(paginated_issues)
            return all_issues
        
        all_issues = get_all_issues()
        assert len(all_issues) >= issues_to_create
        
        # Test 2: Get specific page of issues
        per_page = 2
        @with_retry
        def get_page_issues():
            page_issues = get_paginated_items(paginated_issues, page=1, per_page=per_page)
            return page_issues
        
        page_issues = get_page_issues()
        assert len(page_issues) <= per_page
        
        # Test 3: Test with non-existent results (using a filter that returns nothing)
        @with_retry
        def get_filtered_issues():
            # Use a random label that won't exist
            random_label = f"nonexistent-{unique_id}-{randint(1000, 9999)}"
            filtered_paginated_issues = repository.get_issues(
                state="open", 
                labels=[random_label]
            )
            return filtered_paginated_issues
        
        filtered_paginated_issues = get_filtered_issues()
        
        @with_retry
        def get_empty_results():
            empty_results = get_paginated_items(filtered_paginated_issues)
            return empty_results
        
        empty_results = get_empty_results()
        assert empty_results == []
        
    finally:
        # Clean up test issues
        for issue in created_issues:
            @with_retry
            def close_issue(issue_number):
                try:
                    issue = repository.get_issue(issue_number)
                    issue.edit(state="closed")
                except GithubException as e:
                    # Ignore 404 errors (issue may already be closed or deleted)
                    if e.status != 404:
                        raise
            
            close_issue(issue.number)


@pytest.mark.integration
def test_pagination_with_converted_items(test_owner, test_repo_name, unique_id, with_retry):
    """Test pagination utility with real API and object conversion."""
    # In real usage, we often convert GitHub objects to our schema
    # This test verifies our pagination utility works well with that pattern
    
    client = GitHubClient.get_instance()
    repository = client.get_repo(f"{test_owner}/{test_repo_name}")
    
    created_issues = []
    
    try:
        # Create a few test issues
        for i in range(2):
            @with_retry
            def create_test_issue():
                title = f"Test Issue {i} for Conversion {unique_id}"
                issue = repository.create_issue(title=title)
                return issue
            
            issue = create_test_issue()
            created_issues.append(issue)
            time.sleep(1)  # Small delay to ensure different timestamps
        
        # Get issues and paginate with conversion
        @with_retry
        def get_paginated_issues():
            paginated_issues = repository.get_issues(state="open")
            return paginated_issues
        
        paginated_issues = get_paginated_issues()
        
        @with_retry
        def get_and_convert_issues():
            # Get paginated issues and convert them to our schema
            issues = get_paginated_items(paginated_issues)
            converted_issues = [convert_issue(issue) for issue in issues]
            return converted_issues
        
        converted_issues = get_and_convert_issues()
        
        # Verify the conversion worked
        assert len(converted_issues) >= 2
        for issue in converted_issues:
            assert "issue_number" in issue
            assert "title" in issue
            assert "state" in issue
    
    finally:
        # Clean up
        for issue in created_issues:
            @with_retry
            def close_issue(issue_number):
                try:
                    issue = repository.get_issue(issue_number)
                    issue.edit(state="closed")
                except GithubException as e:
                    # Ignore 404 errors
                    if e.status != 404:
                        raise
            
            close_issue(issue.number)
