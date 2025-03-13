"""Integration tests for repository branch operations.

This module contains integration tests for repository branch operations using the real GitHub API.
Following ADR-002, these tests use real API interactions to replace mock-based tests.

This file focuses specifically on branch operations like create_branch and other branch-related
functionality that was previously covered in unit tests/unit/operations/test_repositories_ops.py.
"""

import pytest
import uuid

from pygithub_mcp_server.operations import repositories
from pygithub_mcp_server.schemas.repositories import (
    CreateBranchParams,
    ListCommitsParams
)
from pygithub_mcp_server.errors import GitHubError


# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration


@pytest.mark.integration
def test_create_branch_integration(test_owner, test_repo_name, unique_id, test_cleanup, with_retry):
    """Test create_branch operation with the real GitHub API."""
    # Create a unique branch name to avoid conflicts
    branch_name = f"test-branch-{unique_id}"
    
    # Create parameters using main as source branch
    params = CreateBranchParams(
        owner=test_owner,
        repo=test_repo_name,
        branch=branch_name,
        from_branch="main"  # Assume main branch exists
    )
    
    # Call operation with retry
    @with_retry
    def create_branch_with_retry():
        return repositories.create_branch(params)
    
    result = create_branch_with_retry()
    
    # Register for cleanup - branch will be deleted at end of test
    test_cleanup.add_branch(test_owner, test_repo_name, branch_name)
    
    # Assert expected behavior
    assert result["name"] == branch_name
    assert "sha" in result
    assert "url" in result


@pytest.mark.integration
def test_create_branch_error_handling(test_owner, test_repo_name, with_retry):
    """Test create_branch error handling with invalid parameters."""
    # Try to create a branch with an invalid source branch
    invalid_source = f"nonexistent-branch-{uuid.uuid4().hex[:8]}"
    branch_name = f"test-error-branch-{uuid.uuid4().hex[:8]}"
    
    params = CreateBranchParams(
        owner=test_owner,
        repo=test_repo_name,
        branch=branch_name,
        from_branch=invalid_source
    )
    
    # Expect this to fail due to invalid source branch
    @with_retry
    def create_branch_with_invalid_source():
        try:
            return repositories.create_branch(params)
        except Exception as e:
            # Store error to check later
            create_branch_with_invalid_source.error = e
            raise
    
    # Execute and check for error
    with pytest.raises(GitHubError) as exc_info:
        create_branch_with_invalid_source()
    
    # Check error message
    error_msg = str(exc_info.value).lower()
    assert "not found" in error_msg or "does not exist" in error_msg or "no such" in error_msg


@pytest.mark.integration
def test_create_branch_and_list_commits(test_owner, test_repo_name, unique_id, test_cleanup, with_retry):
    """Test creating a branch and then listing its commits."""
    # First create a branch
    branch_name = f"test-branch-commits-{unique_id}"
    
    create_params = CreateBranchParams(
        owner=test_owner,
        repo=test_repo_name,
        branch=branch_name,
        from_branch="main"
    )
    
    @with_retry
    def create_branch_with_retry():
        return repositories.create_branch(create_params)
    
    create_result = create_branch_with_retry()
    
    # Register for cleanup
    test_cleanup.add_branch(test_owner, test_repo_name, branch_name)
    
    # Now list commits for this branch
    list_params = ListCommitsParams(
        owner=test_owner,
        repo=test_repo_name,
        sha=branch_name,  # Specify our new branch
        page=1,
        per_page=5
    )
    
    @with_retry
    def list_commits_with_retry():
        return repositories.list_commits(list_params)
    
    commits_result = list_commits_with_retry()
    
    # Assert expected behavior
    assert isinstance(commits_result, list)
    assert len(commits_result) > 0  # Should have at least one commit
    
    # The SHA of the first commit should match the SHA from create_branch
    assert create_result["sha"] in [commit["sha"] for commit in commits_result]
    
    # Verify commit structure
    first_commit = commits_result[0]
    assert "sha" in first_commit
    assert "message" in first_commit
    assert "author" in first_commit
    assert "name" in first_commit["author"]
    assert "email" in first_commit["author"]
    assert "date" in first_commit["author"]
    assert "html_url" in first_commit
