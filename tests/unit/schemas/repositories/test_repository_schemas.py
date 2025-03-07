"""Tests for repository schema validation.

This module contains tests for repository-related schema models
and their validation logic.
"""

import pytest
from pydantic import ValidationError

from pygithub_mcp_server.schemas.repositories import (
    CreateRepositoryParams,
    SearchRepositoriesParams,
    CreateOrUpdateFileParams,
    PushFilesParams,
    GetFileContentsParams,
    ForkRepositoryParams,
    CreateBranchParams,
    ListCommitsParams
)
from pygithub_mcp_server.schemas.base import FileContent, RepositoryRef


def test_repository_ref_validation():
    """Test validation for RepositoryRef schema."""
    # Test valid data
    valid_params = RepositoryRef(owner="test-owner", repo="test-repo")
    assert valid_params.owner == "test-owner"
    assert valid_params.repo == "test-repo"
    
    # Test empty owner
    with pytest.raises(ValidationError) as exc_info:
        RepositoryRef(owner="", repo="test-repo")
    assert "owner" in str(exc_info.value).lower()
    
    # Test empty repo
    with pytest.raises(ValidationError) as exc_info:
        RepositoryRef(owner="test-owner", repo="")
    assert "repo" in str(exc_info.value).lower()


def test_search_repositories_params_validation():
    """Test validation for SearchRepositoriesParams schema."""
    # Test valid data
    valid_params = SearchRepositoriesParams(query="language:python stars:>1000")
    assert valid_params.query == "language:python stars:>1000"
    
    # Test with pagination
    valid_with_pagination = SearchRepositoriesParams(
        query="topic:github-api", 
        page=2, 
        per_page=5
    )
    assert valid_with_pagination.page == 2
    assert valid_with_pagination.per_page == 5
    
    # Test empty query
    with pytest.raises(ValidationError) as exc_info:
        SearchRepositoriesParams(query="")
    assert "query" in str(exc_info.value).lower()
    
    # Test invalid page
    with pytest.raises(ValidationError) as exc_info:
        SearchRepositoriesParams(query="test", page=0)
    assert "page" in str(exc_info.value).lower()
    
    # Test invalid per_page
    with pytest.raises(ValidationError) as exc_info:
        SearchRepositoriesParams(query="test", per_page=101)
    assert "per_page" in str(exc_info.value).lower()


def test_create_repository_params_validation():
    """Test validation for CreateRepositoryParams schema."""
    # Test valid data with minimal fields
    valid_params = CreateRepositoryParams(name="test-repo")
    assert valid_params.name == "test-repo"
    assert valid_params.description is None
    assert valid_params.private is None
    assert valid_params.auto_init is None
    
    # Test with all fields
    valid_with_all = CreateRepositoryParams(
        name="test-repo", 
        description="Test repository", 
        private=True, 
        auto_init=True
    )
    assert valid_with_all.name == "test-repo"
    assert valid_with_all.description == "Test repository"
    assert valid_with_all.private is True
    assert valid_with_all.auto_init is True
    
    # Test empty name
    with pytest.raises(ValidationError) as exc_info:
        CreateRepositoryParams(name="")
    assert "name" in str(exc_info.value).lower()


def test_get_file_contents_params_validation():
    """Test validation for GetFileContentsParams schema."""
    # Test valid data with minimal fields
    valid_params = GetFileContentsParams(
        owner="test-owner", 
        repo="test-repo", 
        path="README.md"
    )
    assert valid_params.owner == "test-owner"
    assert valid_params.repo == "test-repo"
    assert valid_params.path == "README.md"
    assert valid_params.branch is None
    
    # Test with branch
    valid_with_branch = GetFileContentsParams(
        owner="test-owner", 
        repo="test-repo", 
        path="src/main.py", 
        branch="feature"
    )
    assert valid_with_branch.path == "src/main.py"
    assert valid_with_branch.branch == "feature"
    
    # Test empty path
    with pytest.raises(ValidationError) as exc_info:
        GetFileContentsParams(owner="test-owner", repo="test-repo", path="")
    assert "path" in str(exc_info.value).lower()


def test_create_or_update_file_params_validation():
    """Test validation for CreateOrUpdateFileParams schema."""
    # Test valid data for creation
    valid_params = CreateOrUpdateFileParams(
        owner="test-owner",
        repo="test-repo",
        path="README.md",
        content="# Test Repository",
        message="Create README",
        branch="main"
    )
    assert valid_params.owner == "test-owner"
    assert valid_params.repo == "test-repo"
    assert valid_params.path == "README.md"
    assert valid_params.content == "# Test Repository"
    assert valid_params.message == "Create README"
    assert valid_params.branch == "main"
    assert valid_params.sha is None
    
    # Test valid data for update
    valid_update = CreateOrUpdateFileParams(
        owner="test-owner",
        repo="test-repo",
        path="README.md",
        content="# Updated Repository",
        message="Update README",
        branch="main",
        sha="abc123"
    )
    assert valid_update.sha == "abc123"
    
    # Test empty path
    with pytest.raises(ValidationError) as exc_info:
        CreateOrUpdateFileParams(
            owner="test-owner",
            repo="test-repo",
            path="",
            content="test",
            message="test",
            branch="main"
        )
    assert "path" in str(exc_info.value).lower()
    
    # Test empty content
    with pytest.raises(ValidationError) as exc_info:
        CreateOrUpdateFileParams(
            owner="test-owner",
            repo="test-repo",
            path="test.md",
            content="",
            message="test",
            branch="main"
        )
    assert "content" in str(exc_info.value).lower()
    
    # Test empty message
    with pytest.raises(ValidationError) as exc_info:
        CreateOrUpdateFileParams(
            owner="test-owner",
            repo="test-repo",
            path="test.md",
            content="test",
            message="",
            branch="main"
        )
    assert "message" in str(exc_info.value).lower()
    
    # Test empty branch
    with pytest.raises(ValidationError) as exc_info:
        CreateOrUpdateFileParams(
            owner="test-owner",
            repo="test-repo",
            path="test.md",
            content="test",
            message="test",
            branch=""
        )
    assert "branch" in str(exc_info.value).lower()


def test_push_files_params_validation():
    """Test validation for PushFilesParams schema."""
    # Test valid data
    files = [
        FileContent(path="README.md", content="# Test Repository"),
        FileContent(path="src/main.py", content="print('Hello World')")
    ]
    valid_params = PushFilesParams(
        owner="test-owner",
        repo="test-repo",
        branch="main",
        files=files,
        message="Add initial files"
    )
    assert valid_params.owner == "test-owner"
    assert valid_params.repo == "test-repo"
    assert valid_params.branch == "main"
    assert len(valid_params.files) == 2
    assert valid_params.files[0].path == "README.md"
    assert valid_params.files[1].path == "src/main.py"
    assert valid_params.message == "Add initial files"
    
    # Test empty files list
    with pytest.raises(ValidationError) as exc_info:
        PushFilesParams(
            owner="test-owner",
            repo="test-repo",
            branch="main",
            files=[],
            message="Add files"
        )
    assert "files" in str(exc_info.value).lower()
    
    # Test empty message
    with pytest.raises(ValidationError) as exc_info:
        PushFilesParams(
            owner="test-owner",
            repo="test-repo",
            branch="main",
            files=files,
            message=""
        )
    assert "message" in str(exc_info.value).lower()
    
    # Test empty branch
    with pytest.raises(ValidationError) as exc_info:
        PushFilesParams(
            owner="test-owner",
            repo="test-repo",
            branch="",
            files=files,
            message="Add files"
        )
    assert "branch" in str(exc_info.value).lower()


def test_fork_repository_params_validation():
    """Test validation for ForkRepositoryParams schema."""
    # Test valid data with minimal fields
    valid_params = ForkRepositoryParams(
        owner="test-owner",
        repo="test-repo"
    )
    assert valid_params.owner == "test-owner"
    assert valid_params.repo == "test-repo"
    assert valid_params.organization is None
    
    # Test with organization
    valid_with_org = ForkRepositoryParams(
        owner="test-owner",
        repo="test-repo",
        organization="test-org"
    )
    assert valid_with_org.organization == "test-org"


def test_create_branch_params_validation():
    """Test validation for CreateBranchParams schema."""
    # Test valid data with minimal fields
    valid_params = CreateBranchParams(
        owner="test-owner",
        repo="test-repo",
        branch="feature"
    )
    assert valid_params.owner == "test-owner"
    assert valid_params.repo == "test-repo"
    assert valid_params.branch == "feature"
    assert valid_params.from_branch is None
    
    # Test with from_branch
    valid_with_source = CreateBranchParams(
        owner="test-owner",
        repo="test-repo",
        branch="feature",
        from_branch="dev"
    )
    assert valid_with_source.from_branch == "dev"
    
    # Test empty branch
    with pytest.raises(ValidationError) as exc_info:
        CreateBranchParams(
            owner="test-owner",
            repo="test-repo",
            branch=""
        )
    assert "branch" in str(exc_info.value).lower()


def test_list_commits_params_validation():
    """Test validation for ListCommitsParams schema."""
    # Test valid data with minimal fields
    valid_params = ListCommitsParams(
        owner="test-owner",
        repo="test-repo"
    )
    assert valid_params.owner == "test-owner"
    assert valid_params.repo == "test-repo"
    assert valid_params.page is None
    assert valid_params.per_page is None
    assert valid_params.sha is None
    
    # Test with all fields
    valid_with_all = ListCommitsParams(
        owner="test-owner",
        repo="test-repo",
        page=2,
        per_page=10,
        sha="main"
    )
    assert valid_with_all.page == 2
    assert valid_with_all.per_page == 10
    assert valid_with_all.sha == "main"
    
    # Test invalid page
    with pytest.raises(ValidationError) as exc_info:
        ListCommitsParams(
            owner="test-owner",
            repo="test-repo",
            page=0
        )
    assert "page" in str(exc_info.value).lower()
    
    # Test invalid per_page
    with pytest.raises(ValidationError) as exc_info:
        ListCommitsParams(
            owner="test-owner",
            repo="test-repo",
            per_page=101
        )
    assert "per_page" in str(exc_info.value).lower()
