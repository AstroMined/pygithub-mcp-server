"""Unit tests for repository tools.

This module contains unit tests for repository-related MCP tools
following the real API testing strategy from ADR-002.
"""

import pytest
import json
import logging
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


from pygithub_mcp_server.tools.repositories.tools import (
    get_repository,
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
    SearchRepositoriesParams,
    GetFileContentsParams,
    CreateOrUpdateFileParams,
    PushFilesParams,
    CreateBranchParams,
    ListCommitsParams,
    ForkRepositoryParams
)
from pygithub_mcp_server.errors import GitHubError


# Test objects using dataclasses instead of mocks
@dataclass
class RepositoryOperation:
    """Test class for repository operations."""
    
    result: Any = None
    validation_error: Optional[Exception] = None
    github_error: Optional[GitHubError] = None
    other_error: Optional[Exception] = None


# Python dictionary to store test operation results based on params
test_operations = {}

# Register test operations
def register_get_repository(params, result=None, validation_error=None, github_error=None, other_error=None):
    """Register get_repository test operation."""
    key = f"get_repository:{params.get('owner')}:{params.get('repo')}"
    test_operations[key] = RepositoryOperation(
        result=result,
        validation_error=validation_error,
        github_error=github_error,
        other_error=other_error
    )

def register_create_repository(params, result=None, validation_error=None, github_error=None, other_error=None):
    """Register create_repository test operation."""
    key = f"create_repository:{params.get('name')}"
    test_operations[key] = RepositoryOperation(
        result=result,
        validation_error=validation_error,
        github_error=github_error,
        other_error=other_error
    )

def register_fork_repository(params, result=None, validation_error=None, github_error=None, other_error=None):
    """Register fork_repository test operation."""
    key = f"fork_repository:{params.get('owner')}:{params.get('repo')}"
    test_operations[key] = RepositoryOperation(
        result=result,
        validation_error=validation_error,
        github_error=github_error,
        other_error=other_error
    )

def register_search_repositories(params, result=None, validation_error=None, github_error=None, other_error=None):
    """Register search_repositories test operation."""
    key = f"search_repositories:{params.get('query')}"
    test_operations[key] = RepositoryOperation(
        result=result,
        validation_error=validation_error,
        github_error=github_error,
        other_error=other_error
    )

def register_get_file_contents(params, result=None, validation_error=None, github_error=None, other_error=None):
    """Register get_file_contents test operation."""
    key = f"get_file_contents:{params.get('owner')}:{params.get('repo')}:{params.get('path')}"
    test_operations[key] = RepositoryOperation(
        result=result,
        validation_error=validation_error,
        github_error=github_error,
        other_error=other_error
    )

def register_create_or_update_file(params, result=None, validation_error=None, github_error=None, other_error=None):
    """Register create_or_update_file test operation."""
    key = f"create_or_update_file:{params.get('owner')}:{params.get('repo')}:{params.get('path')}"
    test_operations[key] = RepositoryOperation(
        result=result,
        validation_error=validation_error,
        github_error=github_error,
        other_error=other_error
    )

def register_push_files(params, result=None, validation_error=None, github_error=None, other_error=None):
    """Register push_files test operation."""
    key = f"push_files:{params.get('owner')}:{params.get('repo')}"
    test_operations[key] = RepositoryOperation(
        result=result,
        validation_error=validation_error,
        github_error=github_error,
        other_error=other_error
    )

def register_create_branch(params, result=None, validation_error=None, github_error=None, other_error=None):
    """Register create_branch test operation."""
    key = f"create_branch:{params.get('owner')}:{params.get('repo')}:{params.get('branch')}"
    test_operations[key] = RepositoryOperation(
        result=result,
        validation_error=validation_error,
        github_error=github_error,
        other_error=other_error
    )

def register_list_commits(params, result=None, validation_error=None, github_error=None, other_error=None):
    """Register list_commits test operation."""
    key = f"list_commits:{params.get('owner')}:{params.get('repo')}"
    test_operations[key] = RepositoryOperation(
        result=result,
        validation_error=validation_error,
        github_error=github_error,
        other_error=other_error
    )


# Setup tests for each tool operation
@pytest.fixture
def setup_tests(monkeypatch):
    """Set up test operations."""
    # Reset test operations
    test_operations.clear()

    # Sample test data
    repo_data = {
        "id": 12345,
        "name": "test-repo",
        "full_name": "test-owner/test-repo",
        "owner": "test-owner",
        "private": False,
        "html_url": "https://github.com/test-owner/test-repo",
        "description": "Test repository"
    }
    
    fork_data = {
        "id": 67890,
        "name": "test-repo",
        "full_name": "test-org/test-repo",
        "owner": "test-org",
        "private": False,
        "html_url": "https://github.com/test-org/test-repo",
        "description": "Fork of test-owner/test-repo"
    }
    
    search_data = [
        {
            "id": 12345,
            "name": "repo1",
            "full_name": "owner/repo1",
            "owner": "owner",
            "private": False,
            "html_url": "https://github.com/owner/repo1",
            "description": "Test repository 1"
        },
        {
            "id": 67890,
            "name": "repo2",
            "full_name": "owner/repo2",
            "owner": "owner",
            "private": False,
            "html_url": "https://github.com/owner/repo2",
            "description": "Test repository 2"
        }
    ]
    
    file_data = {
        "name": "README.md",
        "path": "README.md",
        "sha": "file123",
        "size": 100,
        "type": "file",
        "encoding": "base64",
        "content": "SGVsbG8gV29ybGQh",  # base64 encoded "Hello World!"
        "url": "https://api.github.com/repos/test-owner/test-repo/contents/README.md",
        "html_url": "https://github.com/test-owner/test-repo/blob/main/README.md",
        "download_url": "https://raw.githubusercontent.com/test-owner/test-repo/main/README.md"
    }
    
    dir_data = {
        "is_directory": True,
        "path": "src",
        "contents": [
            {
                "name": "file1.md",
                "path": "src/file1.md",
                "sha": "file1",
                "size": 100,
                "type": "file",
                "url": "https://api.github.com/repos/test-owner/test-repo/contents/src/file1.md",
                "html_url": "https://github.com/test-owner/test-repo/blob/main/src/file1.md",
                "download_url": "https://raw.githubusercontent.com/test-owner/test-repo/main/src/file1.md"
            },
            {
                "name": "file2.py",
                "path": "src/file2.py",
                "sha": "file2",
                "size": 200,
                "type": "file",
                "url": "https://api.github.com/repos/test-owner/test-repo/contents/src/file2.py",
                "html_url": "https://github.com/test-owner/test-repo/blob/main/src/file2.py",
                "download_url": "https://raw.githubusercontent.com/test-owner/test-repo/main/src/file2.py"
            }
        ]
    }
    
    create_file_data = {
        "commit": {
            "sha": "newcommit123",
            "message": "Create README",
            "html_url": "https://github.com/test-owner/test-repo/commit/newcommit123"
        },
        "content": {
            "path": "README.md",
            "sha": "newfile123",
            "size": 15,
            "html_url": "https://github.com/test-owner/test-repo/blob/main/README.md"
        }
    }
    
    push_files_data = {
        "message": "Add initial files",
        "branch": "main",
        "files": [
            {
                "path": "README.md",
                "sha": "file1"
            },
            {
                "path": "src/main.py",
                "sha": "file2"
            }
        ]
    }
    
    branch_data = {
        "name": "feature",
        "sha": "abc123def456",
        "url": "https://api.github.com/repos/test-owner/test-repo/git/refs/heads/feature"
    }
    
    commits_data = [
        {
            "sha": "abc123",
            "message": "First commit",
            "author": {
                "name": "Test User",
                "email": "test@example.com",
                "date": "2025-03-07T12:34:56Z"
            },
            "html_url": "https://github.com/test-owner/test-repo/commit/abc123"
        },
        {
            "sha": "def456",
            "message": "Second commit",
            "author": {
                "name": "Test User",
                "email": "test@example.com",
                "date": "2025-03-07T13:45:07Z"
            },
            "html_url": "https://github.com/test-owner/test-repo/commit/def456"
        }
    ]
    
    # Success case registrations
    register_get_repository({"owner": "test-owner", "repo": "test-repo"}, result=repo_data)
    register_create_repository({"name": "test-repo"}, result=repo_data)
    register_fork_repository({"owner": "test-owner", "repo": "test-repo"}, result=fork_data)
    register_search_repositories({"query": "language:python"}, result=search_data)
    register_get_file_contents({"owner": "test-owner", "repo": "test-repo", "path": "README.md"}, result=file_data)
    register_get_file_contents({"owner": "test-owner", "repo": "test-repo", "path": "src"}, result=dir_data)
    register_create_or_update_file({"owner": "test-owner", "repo": "test-repo", "path": "README.md"}, result=create_file_data)
    register_push_files({"owner": "test-owner", "repo": "test-repo"}, result=push_files_data)
    register_create_branch({"owner": "test-owner", "repo": "test-repo", "branch": "feature"}, result=branch_data)
    register_list_commits({"owner": "test-owner", "repo": "test-repo"}, result=commits_data)
    
    # Error case registrations
    not_found_error = GitHubError("Repository not found", response={"status": 404})
    register_get_repository({"owner": "not-found", "repo": "test-repo"}, github_error=not_found_error)
    
    validation_error = ValueError("Invalid repository name")
    register_create_repository({"name": ""}, validation_error=validation_error)
    
    rate_limit_error = GitHubError("API rate limit exceeded", response={"status": 403})
    register_search_repositories({"query": "rate-limited"}, github_error=rate_limit_error)
    
    unexpected_error = Exception("Unexpected error")
    register_create_branch({"owner": "error", "repo": "test-repo", "branch": "feature"}, other_error=unexpected_error)
    
    # Monkeypatch repository operations functions
    def get_repository_mock(owner, repo):
        key = f"get_repository:{owner}:{repo}"
        op = test_operations.get(key)
        if op is None:
            return None
        
        if op.validation_error:
            raise op.validation_error
        if op.github_error:
            raise op.github_error
        if op.other_error:
            raise op.other_error
        
        return op.result
    
    def create_repository_mock(params):
        key = f"create_repository:{params.name}"
        op = test_operations.get(key)
        if op is None:
            return None
        
        if op.validation_error:
            raise op.validation_error
        if op.github_error:
            raise op.github_error
        if op.other_error:
            raise op.other_error
        
        return op.result
    
    def fork_repository_mock(params):
        key = f"fork_repository:{params.owner}:{params.repo}"
        op = test_operations.get(key)
        if op is None:
            return None
        
        if op.validation_error:
            raise op.validation_error
        if op.github_error:
            raise op.github_error
        if op.other_error:
            raise op.other_error
        
        return op.result
    
    def search_repositories_mock(params):
        key = f"search_repositories:{params.query}"
        op = test_operations.get(key)
        if op is None:
            return None
        
        if op.validation_error:
            raise op.validation_error
        if op.github_error:
            raise op.github_error
        if op.other_error:
            raise op.other_error
        
        return op.result
    
    def get_file_contents_mock(params):
        key = f"get_file_contents:{params.owner}:{params.repo}:{params.path}"
        op = test_operations.get(key)
        if op is None:
            return None
        
        if op.validation_error:
            raise op.validation_error
        if op.github_error:
            raise op.github_error
        if op.other_error:
            raise op.other_error
        
        return op.result
    
    def create_or_update_file_mock(params):
        key = f"create_or_update_file:{params.owner}:{params.repo}:{params.path}"
        op = test_operations.get(key)
        if op is None:
            return None
        
        if op.validation_error:
            raise op.validation_error
        if op.github_error:
            raise op.github_error
        if op.other_error:
            raise op.other_error
        
        return op.result
    
    def push_files_mock(params):
        key = f"push_files:{params.owner}:{params.repo}"
        op = test_operations.get(key)
        if op is None:
            return None
        
        if op.validation_error:
            raise op.validation_error
        if op.github_error:
            raise op.github_error
        if op.other_error:
            raise op.other_error
        
        return op.result
    
    def create_branch_mock(params):
        key = f"create_branch:{params.owner}:{params.repo}:{params.branch}"
        op = test_operations.get(key)
        if op is None:
            return None
        
        if op.validation_error:
            raise op.validation_error
        if op.github_error:
            raise op.github_error
        if op.other_error:
            raise op.other_error
        
        return op.result
    
    def list_commits_mock(params):
        key = f"list_commits:{params.owner}:{params.repo}"
        op = test_operations.get(key)
        if op is None:
            return None
        
        if op.validation_error:
            raise op.validation_error
        if op.github_error:
            raise op.github_error
        if op.other_error:
            raise op.other_error
        
        return op.result
    
    # Patch the operations functions
    monkeypatch.setattr("pygithub_mcp_server.operations.repositories.get_repository", get_repository_mock)
    monkeypatch.setattr("pygithub_mcp_server.operations.repositories.create_repository", create_repository_mock)
    monkeypatch.setattr("pygithub_mcp_server.operations.repositories.fork_repository", fork_repository_mock)
    monkeypatch.setattr("pygithub_mcp_server.operations.repositories.search_repositories", search_repositories_mock)
    monkeypatch.setattr("pygithub_mcp_server.operations.repositories.get_file_contents", get_file_contents_mock)
    monkeypatch.setattr("pygithub_mcp_server.operations.repositories.create_or_update_file", create_or_update_file_mock)
    monkeypatch.setattr("pygithub_mcp_server.operations.repositories.push_files", push_files_mock)
    monkeypatch.setattr("pygithub_mcp_server.operations.repositories.create_branch", create_branch_mock)
    monkeypatch.setattr("pygithub_mcp_server.operations.repositories.list_commits", list_commits_mock)


def test_get_repository_tool_success(setup_tests):
    """Test get_repository tool with success case."""
    # Call the tool
    result = get_repository({"owner": "test-owner", "repo": "test-repo"})
    
    # Assert expected behavior
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "text"
    
    # Verify content can be parsed as JSON
    content = json.loads(result["content"][0]["text"])
    assert content["id"] == 12345
    assert content["name"] == "test-repo"
    assert content["full_name"] == "test-owner/test-repo"
    assert content["owner"] == "test-owner"


def test_get_repository_tool_error(setup_tests):
    """Test get_repository tool with error case."""
    # Call the tool
    result = get_repository({"owner": "not-found", "repo": "test-repo"})
    
    # Assert expected behavior
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "error"
    assert "not found" in result["content"][0]["text"].lower()
    assert "is_error" in result
    assert result["is_error"] is True


def test_create_repository_tool_success(setup_tests):
    """Test create_repository tool with success case."""
    # Call the tool
    result = create_repository({
        "name": "test-repo", 
        "description": "Test repository", 
        "private": True, 
        "auto_init": True
    })
    
    # Assert expected behavior
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "text"
    
    # Verify content can be parsed as JSON
    content = json.loads(result["content"][0]["text"])
    assert content["id"] == 12345
    assert content["name"] == "test-repo"
    assert content["full_name"] == "test-owner/test-repo"
    assert content["owner"] == "test-owner"


def test_create_repository_tool_validation_error(setup_tests):
    """Test create_repository tool with validation error."""
    # Call the tool
    result = create_repository({"name": ""})
    
    # Assert expected behavior
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "error"
    assert "validation error" in result["content"][0]["text"].lower()
    assert "is_error" in result
    assert result["is_error"] is True


def test_fork_repository_tool(setup_tests):
    """Test fork_repository tool."""
    # Call the tool
    result = fork_repository({
        "owner": "test-owner", 
        "repo": "test-repo", 
        "organization": "test-org"
    })
    
    # Assert expected behavior
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "text"
    
    # Verify content can be parsed as JSON
    content = json.loads(result["content"][0]["text"])
    assert content["id"] == 67890
    assert content["name"] == "test-repo"
    assert content["full_name"] == "test-org/test-repo"
    assert content["owner"] == "test-org"
    assert "fork of" in content["description"].lower()


def test_search_repositories_tool(setup_tests):
    """Test search_repositories tool."""
    # Call the tool
    result = search_repositories({"query": "language:python"})
    
    # Assert expected behavior
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "text"
    
    # Verify content can be parsed as JSON
    content = json.loads(result["content"][0]["text"])
    assert len(content) == 2
    assert content[0]["name"] == "repo1"
    assert content[0]["full_name"] == "owner/repo1"
    assert content[1]["name"] == "repo2"


def test_search_repositories_tool_rate_limit(setup_tests):
    """Test search_repositories tool with rate limit error."""
    # Call the tool
    result = search_repositories({"query": "rate-limited"})
    
    # Assert expected behavior
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "error"
    assert "rate limit" in result["content"][0]["text"].lower()
    assert "is_error" in result
    assert result["is_error"] is True


def test_get_file_contents_tool_file(setup_tests):
    """Test get_file_contents tool for a file."""
    # Call the tool
    result = get_file_contents({
        "owner": "test-owner", 
        "repo": "test-repo", 
        "path": "README.md"
    })
    
    # Assert expected behavior
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "text"
    
    # Verify content can be parsed as JSON
    content = json.loads(result["content"][0]["text"])
    assert content["name"] == "README.md"
    assert content["path"] == "README.md"
    assert content["sha"] == "file123"
    assert content["encoding"] == "base64"
    assert content["content"] == "SGVsbG8gV29ybGQh"  # base64 encoded "Hello World!"


def test_get_file_contents_tool_directory(setup_tests):
    """Test get_file_contents tool for a directory."""
    # Call the tool
    result = get_file_contents({
        "owner": "test-owner", 
        "repo": "test-repo", 
        "path": "src"
    })
    
    # Assert expected behavior
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "text"
    
    # Verify content can be parsed as JSON
    content = json.loads(result["content"][0]["text"])
    assert content["is_directory"] is True
    assert content["path"] == "src"
    assert len(content["contents"]) == 2
    assert content["contents"][0]["name"] == "file1.md"
    assert content["contents"][1]["name"] == "file2.py"


def test_create_or_update_file_tool(setup_tests):
    """Test create_or_update_file tool."""
    # Call the tool
    result = create_or_update_file({
        "owner": "test-owner", 
        "repo": "test-repo", 
        "path": "README.md", 
        "content": "# Test Repository", 
        "message": "Create README", 
        "branch": "main"
    })
    
    # Assert expected behavior
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "text"
    
    # Verify content can be parsed as JSON
    content = json.loads(result["content"][0]["text"])
    assert content["commit"]["sha"] == "newcommit123"
    assert content["commit"]["message"] == "Create README"
    assert content["content"]["path"] == "README.md"
    assert content["content"]["sha"] == "newfile123"


def test_push_files_tool(setup_tests):
    """Test push_files tool."""
    # Call the tool
    result = push_files({
        "owner": "test-owner", 
        "repo": "test-repo", 
        "branch": "main", 
        "files": [
            {"path": "README.md", "content": "# Test Repository"},
            {"path": "src/main.py", "content": "print('Hello World')"}
        ], 
        "message": "Add initial files"
    })
    
    # Assert expected behavior
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "text"
    
    # Verify content can be parsed as JSON
    content = json.loads(result["content"][0]["text"])
    assert content["message"] == "Add initial files"
    assert content["branch"] == "main"
    assert len(content["files"]) == 2
    assert content["files"][0]["path"] == "README.md"
    assert content["files"][1]["path"] == "src/main.py"


def test_create_branch_tool(setup_tests):
    """Test create_branch tool."""
    # Call the tool
    result = create_branch({
        "owner": "test-owner", 
        "repo": "test-repo", 
        "branch": "feature", 
        "from_branch": "main"
    })
    
    # Assert expected behavior
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "text"
    
    # Verify content can be parsed as JSON
    content = json.loads(result["content"][0]["text"])
    assert content["name"] == "feature"
    assert content["sha"] == "abc123def456"
    assert "url" in content


def test_create_branch_tool_unexpected_error(setup_tests):
    """Test create_branch tool with unexpected error."""
    # Call the tool
    result = create_branch({
        "owner": "error", 
        "repo": "test-repo", 
        "branch": "feature"
    })
    
    # Assert expected behavior
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "error"
    assert "internal server error" in result["content"][0]["text"].lower()
    assert "is_error" in result
    assert result["is_error"] is True


# Custom Validation Error class that mimics Pydantic's ValidationError should be defined before use
@dataclass
class ValidationErrorDetail:
    """Test class for validation error detail."""
    loc: List[str]
    msg: str
    type: str

@dataclass
class CustomValidationError(Exception):
    """Test class for Pydantic validation errors."""
    errors: List[ValidationErrorDetail]
    
    def __str__(self):
        """Return string representation."""
        return f"Validation error: {'; '.join(e.msg for e in self.errors)}"

def test_list_commits_tool(setup_tests):
    """Test list_commits tool."""
    # Call the tool
    result = list_commits({
        "owner": "test-owner", 
        "repo": "test-repo", 
        "page": 1, 
        "per_page": 10
    })
    
    # Assert expected behavior
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "text"
    
    # Verify content can be parsed as JSON
    content = json.loads(result["content"][0]["text"])
    assert len(content) == 2
    assert content[0]["sha"] == "abc123"
    assert content[0]["message"] == "First commit"
    assert "author" in content[0]
    assert content[1]["sha"] == "def456"
    assert content[1]["message"] == "Second commit"


def test_validation_error_handling(setup_tests):
    """Test handling of validation errors."""
    # Register validation error with our custom class
    validation_error = CustomValidationError([
        ValidationErrorDetail(
            loc=["name"],
            msg="field required",
            type="value_error.missing"
        )
    ])
    
    register_create_repository(
        {"name": "invalid-repo"},
        validation_error=validation_error
    )
    
    # Call the tool
    result = create_repository({"name": "invalid-repo"})
    
    # Assert expected behavior
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "error"
    assert "validation error" in result["content"][0]["text"].lower()
    assert "is_error" in result
    assert result["is_error"] is True


def test_get_repository_traceback_logging(setup_tests, caplog):
    """Test traceback logging for unexpected errors."""
    caplog.set_level(logging.ERROR)
    
    # Register unexpected error
    unexpected_error = Exception("Unexpected server error")
    register_get_repository(
        {"owner": "error-traceback", "repo": "test-repo"}, 
        other_error=unexpected_error
    )
    
    # Call the tool
    result = get_repository({"owner": "error-traceback", "repo": "test-repo"})
    
    # Assert expected behavior
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "error"
    assert "internal server error" in result["content"][0]["text"].lower()
    assert "unexpected server error" in result["content"][0]["text"].lower()
    assert "is_error" in result
    assert result["is_error"] is True
    
    # Check logging
    assert "Unexpected error" in caplog.text


def test_different_github_error_types(setup_tests):
    """Test handling of different GitHub error types."""
    # Register different error types
    not_authorized_error = GitHubError("Unauthorized", response={"status": 401})
    register_get_repository(
        {"owner": "unauthorized", "repo": "test-repo"},
        github_error=not_authorized_error
    )
    
    forbidden_error = GitHubError("Forbidden", response={"status": 403})
    register_get_repository(
        {"owner": "forbidden", "repo": "test-repo"},
        github_error=forbidden_error
    )
    
    validation_failed_error = GitHubError("Validation Failed", response={"status": 422})
    register_get_repository(
        {"owner": "validation-failed", "repo": "test-repo"},
        github_error=validation_failed_error
    )
    
    # Test unauthorized error
    result = get_repository({"owner": "unauthorized", "repo": "test-repo"})
    assert result["is_error"] is True
    assert "unauthorized" in result["content"][0]["text"].lower()
    
    # Test forbidden error
    result = get_repository({"owner": "forbidden", "repo": "test-repo"})
    assert result["is_error"] is True
    assert "forbidden" in result["content"][0]["text"].lower()
    
    # Test validation failed error
    result = get_repository({"owner": "validation-failed", "repo": "test-repo"})
    assert result["is_error"] is True
    assert "validation failed" in result["content"][0]["text"].lower()


def test_github_error_without_response(setup_tests):
    """Test handling of GitHub error without response property."""
    # Register error without response property
    no_response_error = GitHubError("Generic GitHub error")  # No response property
    register_get_repository(
        {"owner": "no-response", "repo": "test-repo"},
        github_error=no_response_error
    )
    
    # Test error without response
    result = get_repository({"owner": "no-response", "repo": "test-repo"})
    assert result["is_error"] is True
    assert "github error" in result["content"][0]["text"].lower()


def test_empty_error_message(setup_tests):
    """Test handling of error with empty message."""
    # Register error with empty message
    empty_message_error = Exception("")  # Empty error message
    register_get_repository(
        {"owner": "empty-message", "repo": "test-repo"},
        other_error=empty_message_error
    )
    
    # Test error with empty message
    result = get_repository({"owner": "empty-message", "repo": "test-repo"})
    assert result["is_error"] is True
    assert "unexpected error occurred" in result["content"][0]["text"].lower()


def test_search_repositories_missing_query(setup_tests):
    """Test search_repositories tool with missing query parameter."""
    # Register a validation error for missing query
    validation_error = CustomValidationError([
        ValidationErrorDetail(
            loc=["query"],
            msg="field required",
            type="value_error.missing"
        )
    ])
    
    register_search_repositories({}, validation_error=validation_error)
    
    # Call the tool with empty params
    result = search_repositories({})  # Missing required query parameter
    
    # Assert expected behavior
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "error"
    assert "validation error" in result["content"][0]["text"].lower()
    assert "is_error" in result
    assert result["is_error"] is True
