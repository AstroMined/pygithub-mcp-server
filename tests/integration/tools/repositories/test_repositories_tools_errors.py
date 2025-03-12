"""Integration tests for repository tools error handling.

This module contains integration tests that verify the error handling behavior
of repository tools with the real GitHub API, following the ADR-002 approach
of using real API testing instead of mocks.
"""

import json
import pytest
import uuid
from datetime import datetime

from pygithub_mcp_server.tools.repositories.tools import (
    get_repository,
    search_repositories,
    list_commits,
    get_file_contents,
    create_or_update_file,
    push_files,
    create_branch,
    create_repository,
    fork_repository
)


# Test resource not found errors (404)
@pytest.mark.integration
def test_get_repository_not_found(test_owner, with_retry):
    """Test get_repository with non-existent repository."""
    # Generate a unique repository name that shouldn't exist
    unique_repo = f"nonexistent-repo-{uuid.uuid4().hex[:8]}"
    
    @with_retry
    def get_nonexistent_repo():
        return get_repository({
            "owner": test_owner,
            "repo": unique_repo
        })
    
    # Get response
    result = get_nonexistent_repo()
    
    # Verify error handling
    assert result.get("is_error", False) is True
    assert result["content"][0]["type"] == "error"
    assert "not found" in result["content"][0]["text"].lower()


# Test parameter validation errors
@pytest.mark.integration
def test_create_or_update_file_validation_error(test_owner, test_repo_name, with_retry):
    """Test validation error in create_or_update_file with missing parameters."""
    @with_retry
    def create_file_with_missing_params():
        return create_or_update_file({
            "owner": test_owner,
            "repo": test_repo_name,
            "path": "test-file.md",
            # Missing required 'content' and 'message' parameters
        })
    
    # Call tool with missing parameters
    result = create_file_with_missing_params()
    
    # Verify validation error
    assert result.get("is_error", False) is True
    assert result["content"][0]["type"] == "error"
    assert "validation error" in result["content"][0]["text"].lower()


@pytest.mark.integration
def test_list_commits_validation_error(with_retry):
    """Test validation error in list_commits with missing parameters."""
    @with_retry
    def list_commits_with_missing_params():
        return list_commits({
            # Missing required 'owner' and 'repo' parameters
        })
    
    # Call tool with missing parameters
    result = list_commits_with_missing_params()
    
    # Verify validation error
    assert result.get("is_error", False) is True
    assert result["content"][0]["type"] == "error"
    assert "validation error" in result["content"][0]["text"].lower()


@pytest.mark.integration
def test_push_files_validation_error(test_owner, test_repo_name, with_retry):
    """Test validation error in push_files with missing parameters."""
    @with_retry
    def push_files_with_missing_params():
        return push_files({
            "owner": test_owner,
            "repo": test_repo_name,
            # Missing required 'files', 'branch', and 'message' parameters
        })
    
    # Call tool with missing parameters
    result = push_files_with_missing_params()
    
    # Verify validation error
    assert result.get("is_error", False) is True
    assert result["content"][0]["type"] == "error"
    assert "validation error" in result["content"][0]["text"].lower()


@pytest.mark.integration
def test_create_branch_validation_error(test_owner, with_retry):
    """Test validation error in create_branch with missing parameters."""
    @with_retry
    def create_branch_with_missing_params():
        return create_branch({
            "owner": test_owner,
            # Missing required 'repo' and 'branch' parameters
        })
    
    # Call tool with missing parameters
    result = create_branch_with_missing_params()
    
    # Verify validation error
    assert result.get("is_error", False) is True
    assert result["content"][0]["type"] == "error"
    assert "validation error" in result["content"][0]["text"].lower()


# Test SHA requirement error for file updates
@pytest.mark.integration
def test_create_or_update_file_missing_sha(test_owner, test_repo_name, test_cleanup, with_retry):
    """Test updating a file without providing the required SHA."""
    # First, create a file to ensure it exists
    test_file_path = f"test-file-{uuid.uuid4().hex[:8]}.md"
    
    @with_retry
    def create_initial_file():
        return create_or_update_file({
            "owner": test_owner,
            "repo": test_repo_name,
            "path": test_file_path,
            "content": "# Initial content",
            "message": "Create test file",
            "branch": "main"
        })
    
    # Create initial file
    create_result = create_initial_file()
    assert not create_result.get("is_error", False)
    
    # Register for cleanup
    test_cleanup.add_file(test_owner, test_repo_name, test_file_path)
    
    @with_retry
    def update_without_sha():
        return create_or_update_file({
            "owner": test_owner,
            "repo": test_repo_name,
            "path": test_file_path,
            "content": "# Updated content",
            "message": "Update test file",
            "branch": "main"
            # Missing the required 'sha' parameter for updates
        })
    
    # Try to update without SHA
    result = update_without_sha()
    
    # Verify error handling
    assert result.get("is_error", False) is True
    assert result["content"][0]["type"] == "error"
    # GitHub API requires SHA when updating a file that already exists
    assert "sha" in result["content"][0]["text"].lower()


# Test branch already exists error
@pytest.mark.integration
def test_create_branch_already_exists(test_owner, test_repo_name, with_retry):
    """Test creating a branch that already exists (main branch)."""
    @with_retry
    def create_existing_branch():
        return create_branch({
            "owner": test_owner,
            "repo": test_repo_name,
            "branch": "main",  # Try to create 'main' which should already exist
            "from_branch": "main"
        })
    
    # Try to create the main branch (which already exists)
    result = create_existing_branch()
    
    # Verify error handling
    assert result.get("is_error", False) is True
    assert result["content"][0]["type"] == "error"
    # Error message might vary, but should indicate the reference already exists
    assert "already exists" in result["content"][0]["text"].lower() or "reference already exists" in result["content"][0]["text"].lower()


# Test error for getting file contents that don't exist
@pytest.mark.integration
def test_get_file_contents_not_found(test_owner, test_repo_name, with_retry):
    """Test getting file contents for a file that doesn't exist."""
    # Generate a unique file path that shouldn't exist
    unique_path = f"nonexistent-file-{uuid.uuid4().hex[:8]}.md"
    
    @with_retry
    def get_nonexistent_file():
        return get_file_contents({
            "owner": test_owner,
            "repo": test_repo_name,
            "path": unique_path
        })
    
    # Try to get a non-existent file
    result = get_nonexistent_file()
    
    # Verify error handling
    assert result.get("is_error", False) is True
    assert result["content"][0]["type"] == "error"
    assert "not found" in result["content"][0]["text"].lower()


# Test updating an existing file without SHA (alternative approach)
@pytest.mark.integration
def test_update_existing_file_missing_sha(test_owner, test_repo_name, with_retry):
    """Test updating an existing file without providing the required SHA.

    Note: This test revealed a bug in operations/repositories.py where 
    the code tries to access result["commit"].message, but the correct path 
    should be result["commit"].commit.message
    """
    # Assume README.md exists in the test repository - most repos have this
    # Try to update it without providing the SHA
    @with_retry
    def update_readme_without_sha():
        return create_or_update_file({
            "owner": test_owner,
            "repo": test_repo_name,
            "path": "README.md",
            "content": "# Updated README",
            "message": "Update README",
            "branch": "main"
            # Missing the required 'sha' parameter for updates
        })
    
    # Try to update without SHA
    result = update_readme_without_sha()
    
    # Verify error handling
    assert result.get("is_error", False) is True
    assert result["content"][0]["type"] == "error"
    # GitHub API requires SHA when updating a file that already exists
    assert "sha" in result["content"][0]["text"].lower() or "required" in result["content"][0]["text"].lower()

# Test search with invalid parameters
@pytest.mark.integration
def test_search_repositories_invalid_query(with_retry):
    """Test repository search with invalid query parameters."""
    @with_retry
    def search_with_empty_query():
        return search_repositories({
            "query": ""  # Empty query should be rejected
        })
    
    # Search with empty query
    result = search_with_empty_query()
    
    # Verify error handling - either validation error or API error
    assert result.get("is_error", False) is True
    assert result["content"][0]["type"] == "error"
