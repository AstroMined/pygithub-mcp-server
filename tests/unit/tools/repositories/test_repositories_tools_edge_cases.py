"""Edge case tests for repository tools.

This module contains targeted tests for edge cases and error conditions
in repository tools to improve test coverage.
"""

import json
import pytest
import logging
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

from pygithub_mcp_server.tools.repositories.tools import (
    create_repository,
    fork_repository,
    search_repositories,
    get_file_contents,
    create_or_update_file,
    push_files,
    create_branch,
    list_commits
)
from pygithub_mcp_server.schemas.repositories import (
    CreateRepositoryParams,
    ForkRepositoryParams,
    SearchRepositoriesParams,
    GetFileContentsParams,
    CreateOrUpdateFileParams,
    PushFilesParams,
    CreateBranchParams,
    ListCommitsParams
)
from pygithub_mcp_server.errors import GitHubError

# Test fixtures and utilities that mirror the approach in test_repositories_tools.py
@dataclass
class RepositoryOperation:
    """Test class for repository operations."""
    result: Any = None
    validation_error: Optional[Exception] = None
    github_error: Optional[GitHubError] = None
    other_error: Optional[Exception] = None

# Dictionary to store test operations and results
test_operations = {}

def register_operation(op_type, params, **kwargs):
    """Register a test operation with its expected result or error."""
    key_parts = [op_type]
    
    # Add key components based on common parameters
    for param_key in ["owner", "repo", "name", "query", "path", "branch"]:
        if param_key in params:
            key_parts.append(f"{params[param_key]}")
    
    key = ":".join(key_parts)
    test_operations[key] = RepositoryOperation(**kwargs)
    return key

# Setup for tests
@pytest.fixture
def setup_edge_case_tests(monkeypatch):
    """Set up tests for edge cases and error conditions."""
    # Clear existing operations
    test_operations.clear()
    
    # Mock implementation for repository operations
    def mock_operation(op_type):
        def operation_handler(params):
            # Convert params to dict if it's a Pydantic model
            param_dict = params
            if not isinstance(params, dict):
                param_dict = params.dict()
            
            # Build key for operation lookup
            key_parts = [op_type]
            for param_key in ["owner", "repo", "name", "query", "path", "branch"]:
                if hasattr(params, param_key):
                    key_parts.append(f"{getattr(params, param_key)}")
                elif param_key in param_dict:
                    key_parts.append(f"{param_dict[param_key]}")
            
            key = ":".join(key_parts)
            op = test_operations.get(key)
            
            if op is None:
                # No registered operation found
                return {}
            
            if op.validation_error:
                raise op.validation_error
            if op.github_error:
                raise op.github_error
            if op.other_error:
                raise op.other_error
            
            return op.result
        return operation_handler
    
    # Patch all operations
    operations = [
        "create_repository", 
        "fork_repository", 
        "search_repositories",
        "get_file_contents", 
        "create_or_update_file", 
        "push_files",
        "create_branch", 
        "list_commits"
    ]
    
    for op in operations:
        monkeypatch.setattr(
            f"pygithub_mcp_server.operations.repositories.{op}", 
            mock_operation(op)
        )

#
# Tests targeting specific missing coverage areas
#

# Lines 57-58: Create repository error handling
def test_create_repository_error_handling(setup_edge_case_tests):
    """Test create_repository error handling (lines 57-58)."""
    # Register a GitHub API error for repository creation
    github_error = GitHubError("Repository creation failed", response={"status": 422, "message": "Validation Failed"})
    register_operation(
        "create_repository", 
        {"name": "error-repo"}, 
        github_error=github_error
    )
    
    # Call the tool with parameters that will trigger the error
    result = create_repository({"name": "error-repo"})
    
    # Verify error handling
    assert result.get("is_error", False) is True
    assert "error" in result["content"][0]["type"]
    assert "repository creation failed" in result["content"][0]["text"].lower()

# Lines 111-112: Fork repository error paths
def test_fork_repository_error_handling(setup_edge_case_tests):
    """Test fork_repository error handling (lines 111-112)."""
    # Register a GitHub API error for repository forking
    github_error = GitHubError("Fork operation failed", response={"status": 403, "message": "Forbidden"})
    register_operation(
        "fork_repository", 
        {"owner": "test-owner", "repo": "forbidden-repo"}, 
        github_error=github_error
    )
    
    # Call the tool with parameters that will trigger the error
    result = fork_repository({"owner": "test-owner", "repo": "forbidden-repo"})
    
    # Verify error handling
    assert result.get("is_error", False) is True
    assert "error" in result["content"][0]["type"]
    assert "fork operation failed" in result["content"][0]["text"].lower()

# Lines 151-167: Repository search edge cases
def test_search_repositories_empty_results(setup_edge_case_tests):
    """Test search_repositories with empty results (lines 151-167)."""
    # Register an empty result for search
    register_operation(
        "search_repositories", 
        {"query": "nonexistent-repo-xyz"}, 
        result=[]
    )
    
    # Call the tool
    result = search_repositories({"query": "nonexistent-repo-xyz"})
    
    # Verify handling of empty results
    assert not result.get("is_error", False)
    assert "text" in result["content"][0]
    
    # Verify content can be parsed as JSON and is an empty array
    content = json.loads(result["content"][0]["text"])
    assert isinstance(content, list)
    assert len(content) == 0

def test_search_repositories_validation_error(setup_edge_case_tests):
    """Test search_repositories with validation error (lines 151-167)."""
    # Register a validation error
    validation_error = ValueError("Invalid query parameter")
    register_operation(
        "search_repositories", 
        {"query": ""}, 
        validation_error=validation_error
    )
    
    # Call the tool
    result = search_repositories({"query": ""})
    
    # Verify validation error handling
    assert result.get("is_error", False) is True
    assert "error" in result["content"][0]["type"]
    assert "validation error" in result["content"][0]["text"].lower()

# Lines 210-214: File contents parameter validation
def test_get_file_contents_parameter_validation(setup_edge_case_tests):
    """Test get_file_contents parameter validation (lines 210-214)."""
    # Call the tool with missing path parameter
    result = get_file_contents({"owner": "test-owner", "repo": "test-repo"})
    
    # Verify validation error handling for missing parameters
    assert result.get("is_error", False) is True
    assert "error" in result["content"][0]["type"]
    assert "validation error" in result["content"][0]["text"].lower()

# Lines 246-262: File update error cases
def test_create_or_update_file_error_handling(setup_edge_case_tests):
    """Test create_or_update_file error handling (lines 246-262)."""
    # Register a GitHub API error for file update
    github_error = GitHubError("File update failed", response={"status": 422, "message": "Validation Failed", "errors": [{"resource": "File", "field": "sha", "code": "required"}]})
    register_operation(
        "create_or_update_file", 
        {"owner": "test-owner", "repo": "test-repo", "path": "README.md"}, 
        github_error=github_error
    )
    
    # Call the tool
    result = create_or_update_file({
        "owner": "test-owner", 
        "repo": "test-repo", 
        "path": "README.md",
        "content": "# Updated content",
        "message": "Update README",
        "branch": "main"
    })
    
    # Verify error handling
    assert result.get("is_error", False) is True
    assert "error" in result["content"][0]["type"]
    assert "file update failed" in result["content"][0]["text"].lower()

def test_create_or_update_file_validation_error(setup_edge_case_tests):
    """Test create_or_update_file validation error (lines 246-262)."""
    # Call with missing required parameters
    result = create_or_update_file({
        "owner": "test-owner",
        "repo": "test-repo",
        "path": "README.md"
        # Missing content and message
    })
    
    # Verify validation error handling
    assert result.get("is_error", False) is True
    assert "error" in result["content"][0]["type"]
    assert "validation error" in result["content"][0]["text"].lower()

# Lines 297-313: Push files validation
def test_push_files_validation_error(setup_edge_case_tests):
    """Test push_files validation error (lines 297-313)."""
    # Call with missing required parameters
    result = push_files({
        "owner": "test-owner",
        "repo": "test-repo"
        # Missing files, message, and branch
    })
    
    # Verify validation error handling
    assert result.get("is_error", False) is True
    assert "error" in result["content"][0]["type"]
    assert "validation error" in result["content"][0]["text"].lower()

def test_push_files_error_handling(setup_edge_case_tests):
    """Test push_files error handling (lines 297-313)."""
    # Register a GitHub API error for push files
    github_error = GitHubError("Push operation failed", response={"status": 422, "message": "Validation Failed"})
    register_operation(
        "push_files", 
        {"owner": "test-owner", "repo": "error-repo"}, 
        github_error=github_error
    )
    
    # Call the tool
    result = push_files({
        "owner": "test-owner", 
        "repo": "error-repo",
        "branch": "main",
        "files": [{"path": "test.txt", "content": "test"}],
        "message": "Add test file"
    })
    
    # Verify error handling
    assert result.get("is_error", False) is True
    assert "error" in result["content"][0]["type"]
    assert "push operation failed" in result["content"][0]["text"].lower()

# Lines 346-362: Branch creation edge cases
def test_create_branch_validation_error(setup_edge_case_tests):
    """Test create_branch validation error (lines 346-362)."""
    # Call with missing required parameters
    result = create_branch({
        "owner": "test-owner"
        # Missing repo and branch
    })
    
    # Verify validation error handling
    assert result.get("is_error", False) is True
    assert "error" in result["content"][0]["type"]
    assert "validation error" in result["content"][0]["text"].lower()

def test_create_branch_error_handling(setup_edge_case_tests):
    """Test create_branch error handling (lines 346-362)."""
    # Register a GitHub API error for branch creation
    github_error = GitHubError("Branch already exists", response={"status": 422, "message": "Reference already exists"})
    register_operation(
        "create_branch", 
        {"owner": "test-owner", "repo": "test-repo", "branch": "existing-branch"}, 
        github_error=github_error
    )
    
    # Call the tool
    result = create_branch({
        "owner": "test-owner", 
        "repo": "test-repo",
        "branch": "existing-branch",
        "from_branch": "main"
    })
    
    # Verify error handling
    assert result.get("is_error", False) is True
    assert "error" in result["content"][0]["type"]
    assert "branch already exists" in result["content"][0]["text"].lower()

# Lines 395-396, 401-402: Commit list parameter validation
def test_list_commits_parameter_validation(setup_edge_case_tests):
    """Test list_commits parameter validation (lines 395-396, 401-402)."""
    # Call with missing required parameters
    result = list_commits({
        # Missing owner and repo
    })
    
    # Verify validation error handling
    assert result.get("is_error", False) is True
    assert "error" in result["content"][0]["type"]
    assert "validation error" in result["content"][0]["text"].lower()

# Lines 443-459: User repository listing
def test_list_commits_error_handling(setup_edge_case_tests):
    """Test list_commits error handling (lines 443-459)."""
    # Register a GitHub API error for listing commits
    github_error = GitHubError("Not found", response={"status": 404, "message": "Not Found"})
    register_operation(
        "list_commits", 
        {"owner": "nonexistent", "repo": "test-repo"}, 
        github_error=github_error
    )
    
    # Call the tool
    result = list_commits({
        "owner": "nonexistent", 
        "repo": "test-repo"
    })
    
    # Verify error handling
    assert result.get("is_error", False) is True
    assert "error" in result["content"][0]["type"]
    assert "not found" in result["content"][0]["text"].lower()
