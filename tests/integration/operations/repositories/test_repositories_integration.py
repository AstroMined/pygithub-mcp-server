"""Integration tests for repository operations.

This module contains integration tests for repository operations using the real GitHub API.
Following ADR-002, we use real API interactions instead of mocks.
"""

import pytest
from datetime import datetime

from pygithub_mcp_server.operations import repositories
from pygithub_mcp_server.schemas.repositories import (
    SearchRepositoriesParams,
    GetFileContentsParams,
    ListCommitsParams
)
from pygithub_mcp_server.errors import GitHubError


# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration


def test_get_repository_integration(test_owner, test_repo_name, with_retry):
    """Test get_repository with real GitHub API."""
    # Call the operation with real API with retry
    @with_retry
    def get_repo_with_retry():
        return repositories.get_repository(test_owner, test_repo_name)
    
    result = get_repo_with_retry()
    
    # Assert expected behavior
    assert "id" in result
    assert result["name"] == test_repo_name
    assert result["full_name"] == f"{test_owner}/{test_repo_name}"
    assert result["owner"] == test_owner
    assert "private" in result
    assert "html_url" in result


def test_search_repositories_integration(with_retry):
    """Test search_repositories with real GitHub API."""
    # Create parameters - search for repositories with 'python' and 'mcp'
    params = SearchRepositoriesParams(
        query="python mcp in:name,description",
        page=1,
        per_page=5
    )
    
    # Call the operation with real API with retry
    @with_retry
    def search_repos_with_retry():
        return repositories.search_repositories(params)
    
    result = search_repos_with_retry()
    
    # Assert expected behavior
    assert isinstance(result, list)
    # There might be no results if search doesn't match anything,
    # but the operation should at least return an empty list
    
    # If there are results, verify their structure
    if result:
        assert "id" in result[0]
        assert "name" in result[0]
        assert "full_name" in result[0]
        assert "owner" in result[0]
        assert "html_url" in result[0]


def test_get_file_contents_integration(test_owner, test_repo_name, with_retry):
    """Test get_file_contents with real GitHub API."""
    # Create parameters - get README.md which should exist in most repos
    params = GetFileContentsParams(
        owner=test_owner,
        repo=test_repo_name,
        path="README.md"
    )
    
    @with_retry
    def get_contents_with_retry():
        try:
            return repositories.get_file_contents(params)
        except Exception as e:
            # Store error details in a property that can be checked later
            get_contents_with_retry.error = e
            raise
    
    try:
        # Call the operation with real API
        result = get_contents_with_retry()
        
        # Assert expected behavior - if README.md exists
        assert "name" in result
        assert result["path"] == "README.md"
        assert "sha" in result
        assert "size" in result
        assert "encoding" in result  # Should be base64
        assert "content" in result   # Base64 encoded content
        assert "html_url" in result
    except GitHubError as e:
        # If README.md doesn't exist, this is fine for the test
        # as long as it's a specific "not found" error
        error_msg = str(e).lower()
        if "not found" not in error_msg and "404" not in error_msg:
            raise  # Re-raise if it's not a "not found" error


def test_list_commits_integration(test_owner, test_repo_name, with_retry):
    """Test list_commits with real GitHub API."""
    # Create parameters with pagination to limit results
    params = ListCommitsParams(
        owner=test_owner,
        repo=test_repo_name,
        page=1,
        per_page=5
    )
    
    # Call the operation with real API with retry
    @with_retry
    def list_commits_with_retry():
        return repositories.list_commits(params)
    
    result = list_commits_with_retry()
    
    # Assert expected behavior
    assert isinstance(result, list)
    
    # Most repositories should have at least one commit
    if result:
        commit = result[0]
        assert "sha" in commit
        assert "message" in commit
        assert "author" in commit
        assert "name" in commit["author"]
        assert "email" in commit["author"]
        assert "date" in commit["author"]
        assert "html_url" in commit


# The remaining tests would require write permissions,
# which aren't always available in test environments
# For example, create_repository, fork_repository, etc.

# Here's an outline of what a create_branch test would look like
# but it's commented out since it requires write permissions:

"""
def test_create_branch_integration(test_owner, test_repo_name, unique_id, test_cleanup, with_retry):
    # Create parameters for new branch
    branch_name = f"test-branch-{unique_id}"
    params = CreateBranchParams(
        owner=test_owner,
        repo=test_repo_name,
        branch=branch_name
    )
    
    # Call operation with real API with retry
    @with_retry
    def create_branch_with_retry():
        return repositories.create_branch(params)
    
    result = create_branch_with_retry()
    
    # Register for cleanup
    test_cleanup.add_branch(test_owner, test_repo_name, branch_name)
    
    # Assert expected behavior
    assert result["name"] == branch_name
    assert "sha" in result
    assert "url" in result
"""
