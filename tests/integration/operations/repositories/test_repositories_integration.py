"""Integration tests for repository operations.

This module contains integration tests for repository operations using the real GitHub API.
Following ADR-002, we use real API interactions instead of mocks.
"""

import os
import uuid
import pytest
from datetime import datetime

from pygithub_mcp_server.operations import repositories
from pygithub_mcp_server.schemas.repositories import (
    SearchRepositoriesParams,
    GetFileContentsParams,
    ListCommitsParams
)
from pygithub_mcp_server.errors import GitHubError


# Skip all tests if the integration marker is not provided
pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.environ.get("GITHUB_TEST_OWNER") is None or 
        os.environ.get("GITHUB_TEST_REPO") is None,
        reason="GITHUB_TEST_OWNER and GITHUB_TEST_REPO environment variables must be set"
    )
]


@pytest.fixture
def test_owner():
    """Get the GitHub owner for test operations."""
    return os.environ.get("GITHUB_TEST_OWNER")


@pytest.fixture
def test_repo():
    """Get the GitHub repository for test operations."""
    return os.environ.get("GITHUB_TEST_REPO")


@pytest.fixture
def test_id():
    """Generate a unique test identifier."""
    return str(uuid.uuid4())[:8]


@pytest.fixture
def test_cleanup():
    """Fixture to track and clean up test resources."""
    class TestCleanup:
        def __init__(self):
            self.branches = []
            
        def add_branch(self, owner, repo, branch):
            """Track a branch for cleanup."""
            self.branches.append((owner, repo, branch))
            
        def cleanup_all(self):
            """Clean up all tracked resources."""
            # Here we would implement cleanup logic for created resources
            # For branches, this would involve deleting them
            # This is not implemented in this example
            pass
            
    cleanup = TestCleanup()
    yield cleanup
    cleanup.cleanup_all()


def test_get_repository_integration(test_owner, test_repo):
    """Test get_repository with real GitHub API."""
    # Call the operation with real API
    result = repositories.get_repository(test_owner, test_repo)
    
    # Assert expected behavior
    assert "id" in result
    assert result["name"] == test_repo
    assert result["full_name"] == f"{test_owner}/{test_repo}"
    assert result["owner"] == test_owner
    assert "private" in result
    assert "html_url" in result


def test_search_repositories_integration():
    """Test search_repositories with real GitHub API."""
    # Create parameters - search for repositories with 'python' and 'mcp'
    params = SearchRepositoriesParams(
        query="python mcp in:name,description",
        page=1,
        per_page=5
    )
    
    # Call the operation with real API
    result = repositories.search_repositories(params)
    
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


def test_get_file_contents_integration(test_owner, test_repo):
    """Test get_file_contents with real GitHub API."""
    # Create parameters - get README.md which should exist in most repos
    params = GetFileContentsParams(
        owner=test_owner,
        repo=test_repo,
        path="README.md"
    )
    
    try:
        # Call the operation with real API
        result = repositories.get_file_contents(params)
        
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
        if e.status != 404:
            raise  # Re-raise if it's not a "not found" error


def test_list_commits_integration(test_owner, test_repo):
    """Test list_commits with real GitHub API."""
    # Create parameters with pagination to limit results
    params = ListCommitsParams(
        owner=test_owner,
        repo=test_repo,
        page=1,
        per_page=5
    )
    
    # Call the operation with real API
    result = repositories.list_commits(params)
    
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
def test_create_branch_integration(test_owner, test_repo, test_id, test_cleanup):
    # Create parameters for new branch
    branch_name = f"test-branch-{test_id}"
    params = CreateBranchParams(
        owner=test_owner,
        repo=test_repo,
        branch=branch_name
    )
    
    # Call operation with real API
    result = repositories.create_branch(params)
    
    # Register for cleanup
    test_cleanup.add_branch(test_owner, test_repo, branch_name)
    
    # Assert expected behavior
    assert result["name"] == branch_name
    assert "sha" in result
    assert "url" in result
"""
