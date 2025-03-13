"""Integration tests for repository file operations.

This module contains integration tests for repository file operations using the real GitHub API.
Following ADR-002, these tests use real API interactions to replace mock-based tests.

This file focuses specifically on file operations like create_or_update_file and push_files
that were previously covered in unit tests/unit/operations/test_repositories_ops.py.
"""

import pytest
import base64
import os

from pygithub_mcp_server.operations import repositories
from pygithub_mcp_server.schemas.repositories import (
    CreateOrUpdateFileParams,
    PushFilesParams,
)
from pygithub_mcp_server.schemas.base import FileContent
from pygithub_mcp_server.errors import GitHubError


# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration


@pytest.mark.integration
def test_create_file_integration(test_owner, test_repo_name, unique_id, test_cleanup, with_retry):
    """Test create_or_update_file operation with a new file."""
    # Create unique file path to avoid conflicts
    file_path = f"test-files/test-create-{unique_id}.md"
    file_content = f"# Test File {unique_id}\n\nThis is a test file created during integration testing."
    commit_message = f"Create test file {unique_id} [integration test]"
    
    # Create parameters
    params = CreateOrUpdateFileParams(
        owner=test_owner,
        repo=test_repo_name,
        path=file_path,
        content=file_content,
        message=commit_message,
        branch="main"  # Assuming main is the default branch
    )
    
    # Call operation with retry
    @with_retry
    def create_file_with_retry():
        return repositories.create_or_update_file(params)
    
    result = create_file_with_retry()
    
    # Register for cleanup - file will be deleted at end of test
    test_cleanup.add_file(test_owner, test_repo_name, file_path)
    
    # Assert expected behavior
    assert "commit" in result
    assert "content" in result
    assert result["commit"]["message"] == commit_message
    assert "html_url" in result["commit"]
    assert result["content"]["path"] == file_path
    assert "sha" in result["content"]
    assert "html_url" in result["content"]


@pytest.mark.integration
def test_update_file_integration(test_owner, test_repo_name, unique_id, test_cleanup, with_retry):
    """Test create_or_update_file operation updating an existing file."""
    # First create a file
    file_path = f"test-files/test-update-{unique_id}.md"
    initial_content = f"# Initial Content {unique_id}\n\nThis file will be updated."
    updated_content = f"# Updated Content {unique_id}\n\nThis file has been updated during integration testing."
    
    # Create initial file
    create_params = CreateOrUpdateFileParams(
        owner=test_owner,
        repo=test_repo_name,
        path=file_path,
        content=initial_content,
        message=f"Create initial file {unique_id} [integration test]",
        branch="main"
    )
    
    @with_retry
    def create_initial_file():
        return repositories.create_or_update_file(create_params)
    
    initial_result = create_initial_file()
    file_sha = initial_result["content"]["sha"]
    
    # Register for cleanup
    test_cleanup.add_file(test_owner, test_repo_name, file_path)
    
    # Now update the file
    update_params = CreateOrUpdateFileParams(
        owner=test_owner,
        repo=test_repo_name,
        path=file_path,
        content=updated_content,
        message=f"Update file {unique_id} [integration test]",
        branch="main",
        sha=file_sha  # Required for updates
    )
    
    @with_retry
    def update_file_with_retry():
        return repositories.create_or_update_file(update_params)
    
    update_result = update_file_with_retry()
    
    # Assert expected behavior
    assert "commit" in update_result
    assert "content" in update_result
    assert "Update file" in update_result["commit"]["message"]
    assert "html_url" in update_result["commit"]
    assert update_result["content"]["path"] == file_path
    assert update_result["content"]["sha"] != file_sha  # SHA should change
    
    # Verify content was actually updated by fetching file
    from pygithub_mcp_server.schemas.repositories import GetFileContentsParams
    
    get_params = GetFileContentsParams(
        owner=test_owner,
        repo=test_repo_name,
        path=file_path
    )
    
    @with_retry
    def get_file_with_retry():
        return repositories.get_file_contents(get_params)
    
    get_result = get_file_with_retry()
    
    # Decode content and verify it matches updated content
    decoded_content = base64.b64decode(get_result["content"]).decode("utf-8")
    assert "Updated Content" in decoded_content


@pytest.mark.integration
def test_push_files_integration(test_owner, test_repo_name, unique_id, test_cleanup, with_retry):
    """Test push_files operation with multiple files at once."""
    # Create unique directory for test files
    test_dir = f"test-push-{unique_id}"
    
    # Prepare multiple files
    files = [
        FileContent(
            path=f"{test_dir}/README.md",
            content=f"# Test Push {unique_id}\n\nThis is the README file."
        ),
        FileContent(
            path=f"{test_dir}/file1.md",
            content=f"# File 1 Content {unique_id}\n\nThis is file 1."
        ),
        FileContent(
            path=f"{test_dir}/file2.md",
            content=f"# File 2 Content {unique_id}\n\nThis is file 2."
        )
    ]
    
    # Create parameters
    params = PushFilesParams(
        owner=test_owner,
        repo=test_repo_name,
        branch="main",
        files=files,
        message=f"Push multiple files {unique_id} [integration test]"
    )
    
    # Call operation with retry
    @with_retry
    def push_files_with_retry():
        return repositories.push_files(params)
    
    result = push_files_with_retry()
    
    # Register files for cleanup
    for file_content in files:
        test_cleanup.add_file(test_owner, test_repo_name, file_content.path)
    
    # Assert expected behavior
    assert "message" in result
    assert f"Push multiple files {unique_id}" in result["message"]
    assert "branch" in result
    assert "files" in result
    assert len(result["files"]) == len(files)
    
    # Verify all file paths are in result
    file_paths = [file_content.path for file_content in files]
    result_paths = [file_info["path"] for file_info in result["files"]]
    
    for path in file_paths:
        assert path in result_paths


@pytest.mark.integration
def test_push_files_error_handling(test_owner, test_repo_name, unique_id, with_retry):
    """Test push_files operation with error handling."""
    # Try pushing files with invalid parameters
    # Missing required content
    files = [
        FileContent(
            path=f"test-error-{unique_id}/file.md",
            content=""  # Empty content should cause an error
        )
    ]
    
    params = PushFilesParams(
        owner=test_owner,
        repo=test_repo_name,
        branch="main",
        files=files,
        message=f"Should fail {unique_id} [integration test]"
    )
    
    # Expect this to fail due to empty content
    @with_retry
    def push_invalid_files():
        try:
            return repositories.push_files(params)
        except Exception as e:
            # Store error to check later
            push_invalid_files.error = e
            raise
    
    # Execute and check for error
    with pytest.raises(GitHubError) as exc_info:
        push_invalid_files()
    
    # Check error message
    error_msg = str(exc_info.value).lower()
    assert "content" in error_msg or "empty" in error_msg or "invalid" in error_msg
