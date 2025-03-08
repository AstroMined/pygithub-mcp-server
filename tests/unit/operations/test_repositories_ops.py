"""Unit tests for repository operations.

This module contains unit tests for repository-related operations
following the real API testing strategy from ADR-002.
"""

import pytest
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

from pygithub_mcp_server.operations import repositories
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
from pygithub_mcp_server.schemas.base import FileContent


# Test objects using dataclasses instead of mocks
@dataclass
class RepositoryOwner:
    """Test class for repository owner."""
    
    login: str
    id: int = 12345
    html_url: str = "https://github.com/test-owner"


@dataclass
class Repository:
    """Test class for repository."""
    
    id: int
    name: str
    full_name: str
    owner: RepositoryOwner
    private: bool = False
    html_url: str = "https://github.com/owner/repo"
    description: str = None
    default_branch: str = "main"

    def get_git_ref(self, ref_name: str):
        """Return test GitRef object."""
        return GitRef(sha="abc123def456", url=f"https://api.github.com/repos/{self.full_name}/git/refs/{ref_name}")
        
    def create_git_ref(self, ref_name: str, sha: str):
        """Return test GitRef object for a new ref."""
        return GitRef(sha=sha, url=f"https://api.github.com/repos/{self.full_name}/git/refs/{ref_name}")
        
    def create_fork(self, **kwargs):
        """Return test Repository object for a fork."""
        org = kwargs.get("organization", "test-user")
        fork_name = f"{org}/{self.name}"
        return Repository(
            id=self.id + 1000,  # Different ID for fork
            name=self.name,
            full_name=fork_name,
            owner=RepositoryOwner(login=org, id=67890),  # Different owner for fork
            description=f"Fork of {self.full_name}",
            html_url=f"https://github.com/{fork_name}"
        )
        
    def get_commits(self, **kwargs):
        """Return test PaginatedList of commits."""
        return [
            Commit(
                sha="abc123",
                commit=CommitDetails(
                    message="First commit",
                    author=CommitAuthor(name="Test User", email="test@example.com", date=datetime.now(tz=timezone.utc))
                ),
                html_url=f"https://github.com/{self.full_name}/commit/abc123"
            ),
            Commit(
                sha="def456",
                commit=CommitDetails(
                    message="Second commit",
                    author=CommitAuthor(name="Test User", email="test@example.com", date=datetime.now(tz=timezone.utc))
                ),
                html_url=f"https://github.com/{self.full_name}/commit/def456"
            )
        ]
        
    def get_contents(self, **kwargs):
        """Return test ContentFile object or list."""
        path = kwargs.get("path", "")
        if path.endswith(".md") or path.endswith(".py"):
            # Single file
            return ContentFile(
                name=path.split("/")[-1],
                path=path,
                sha="file123",
                size=100,
                type="file",
                encoding="base64",
                content="SGVsbG8gV29ybGQh",  # base64 encoded "Hello World!"
                url=f"https://api.github.com/repos/{self.full_name}/contents/{path}",
                html_url=f"https://github.com/{self.full_name}/blob/main/{path}",
                download_url=f"https://raw.githubusercontent.com/{self.full_name}/main/{path}"
            )
        else:
            # Directory
            return [
                ContentFile(
                    name="file1.md",
                    path=f"{path}/file1.md" if path else "file1.md",
                    sha="file1",
                    size=100,
                    type="file",
                    url=f"https://api.github.com/repos/{self.full_name}/contents/{path}/file1.md",
                    html_url=f"https://github.com/{self.full_name}/blob/main/{path}/file1.md",
                    download_url=f"https://raw.githubusercontent.com/{self.full_name}/main/{path}/file1.md"
                ),
                ContentFile(
                    name="file2.py",
                    path=f"{path}/file2.py" if path else "file2.py",
                    sha="file2",
                    size=200,
                    type="file",
                    url=f"https://api.github.com/repos/{self.full_name}/contents/{path}/file2.py",
                    html_url=f"https://github.com/{self.full_name}/blob/main/{path}/file2.py",
                    download_url=f"https://raw.githubusercontent.com/{self.full_name}/main/{path}/file2.py"
                )
            ]
            
    def create_file(self, **kwargs):
        """Return test result for file creation/update."""
        path = kwargs.get("path", "")
        message = kwargs.get("message", "")
        content = kwargs.get("content", "")
        branch = kwargs.get("branch", "main")
        
        return {
            "commit": CommitDetails(
                sha="newcommit123",
                message=message,
                html_url=f"https://github.com/{self.full_name}/commit/newcommit123"
            ),
            "content": ContentFile(
                name=path.split("/")[-1],
                path=path,
                sha="newfile123",
                size=len(content),
                type="file",
                url=f"https://api.github.com/repos/{self.full_name}/contents/{path}",
                html_url=f"https://github.com/{self.full_name}/blob/{branch}/{path}",
                download_url=f"https://raw.githubusercontent.com/{self.full_name}/main/{path}"
            )
        }


@dataclass
class ContentFile:
    """Test class for content file."""
    
    name: str
    path: str
    sha: str
    size: int
    type: str
    url: str
    html_url: str
    download_url: str
    encoding: Optional[str] = None
    content: Optional[str] = None


@dataclass
class GitRef:
    """Test class for git reference."""
    
    sha: str
    url: str
    object: Any = field(default=None)
    
    def __post_init__(self):
        """Initialize GitRefObject if not provided."""
        if self.object is None:
            self.object = GitRefObject(sha=self.sha)


@dataclass
class GitRefObject:
    """Test class for git reference object."""
    
    sha: str
    type: str = "commit"
    url: str = "https://api.github.com/repos/owner/repo/git/commits/abc123"


@dataclass
class CommitAuthor:
    """Test class for commit author."""
    
    name: str
    email: str
    date: datetime


@dataclass
class CommitDetails:
    """Test class for commit details."""
    
    message: str
    sha: Optional[str] = None
    author: Optional[CommitAuthor] = None
    html_url: Optional[str] = None


@dataclass
class Commit:
    """Test class for commit."""
    
    sha: str
    commit: CommitDetails
    html_url: str


@dataclass
class SearchResult:
    """Test class for search result."""
    
    id: int
    name: str
    full_name: str
    owner: RepositoryOwner
    private: bool = False
    html_url: str = "https://github.com/owner/repo"
    description: str = None


@dataclass
class GitHubUser:
    """Test class for GitHub user."""
    
    login: str
    id: int = 12345
    
    def create_repo(self, **kwargs):
        """Return test Repository object."""
        name = kwargs.get("name", "test-repo")
        description = kwargs.get("description")
        private = kwargs.get("private", False)
        return Repository(
            id=54321,
            name=name,
            full_name=f"{self.login}/{name}",
            owner=RepositoryOwner(login=self.login, id=self.id),
            private=private,
            description=description,
            html_url=f"https://github.com/{self.login}/{name}"
        )


@dataclass
class GitHubSearch:
    """Test class for GitHub search."""
    
    def search_repositories(self, query: str):
        """Return test search results."""
        return [
            SearchResult(
                id=12345,
                name="repo1",
                full_name="owner/repo1",
                owner=RepositoryOwner(login="owner"),
                description="Test repository 1"
            ),
            SearchResult(
                id=67890,
                name="repo2",
                full_name="owner/repo2",
                owner=RepositoryOwner(login="owner"),
                description="Test repository 2"
            )
        ]


@dataclass
class GitHub:
    """Test class for PyGithub."""
    
    def get_user(self):
        """Return test User object."""
        return GitHubUser(login="test-user")
    
    def search_repositories(self, query: str):
        """Return test search results."""
        return [
            SearchResult(
                id=12345,
                name="repo1",
                full_name="owner/repo1",
                owner=RepositoryOwner(login="owner"),
                description="Test repository 1"
            ),
            SearchResult(
                id=67890,
                name="repo2",
                full_name="owner/repo2",
                owner=RepositoryOwner(login="owner"),
                description="Test repository 2"
            )
        ]


class TestGitHubClient:
    """Test class for GitHub client."""
    
    def __init__(self, github=None):
        """Initialize the test GitHub client."""
        self.github = github or GitHub()
    
    def get_repo(self, full_name: str):
        """Return test Repository object."""
        owner, repo = full_name.split("/")
        return Repository(
            id=54321,
            name=repo,
            full_name=full_name,
            owner=RepositoryOwner(login=owner),
            html_url=f"https://github.com/{full_name}"
        )


# Tests using dataclasses instead of mocks
def test_get_repository(monkeypatch):
    """Test get_repository operation."""
    # Create test client
    test_client = TestGitHubClient()
    
    # Monkey patch the get_instance method
    monkeypatch.setattr(
        "pygithub_mcp_server.client.client.GitHubClient.get_instance",
        lambda: test_client
    )
    
    # Call the operation
    result = repositories.get_repository("test-owner", "test-repo")
    
    # Assert expected behavior
    assert result["id"] == 54321
    assert result["name"] == "test-repo"
    assert result["full_name"] == "test-owner/test-repo"
    assert result["owner"] == "test-owner"
    assert result["private"] is False
    assert result["html_url"] == "https://github.com/test-owner/test-repo"


def test_create_repository(monkeypatch):
    """Test create_repository operation."""
    # Create test client
    test_client = TestGitHubClient()
    
    # Monkey patch the get_instance method
    monkeypatch.setattr(
        "pygithub_mcp_server.client.client.GitHubClient.get_instance",
        lambda: test_client
    )
    
    # Create parameters
    params = CreateRepositoryParams(
        name="new-repo",
        description="New test repository",
        private=True,
        auto_init=True
    )
    
    # Call the operation
    result = repositories.create_repository(params)
    
    # Assert expected behavior
    assert result["name"] == "new-repo"
    assert result["full_name"] == "test-user/new-repo"
    assert result["owner"] == "test-user"
    assert result["private"] is True
    assert result["description"] == "New test repository"
    assert result["html_url"] == "https://github.com/test-user/new-repo"


def test_fork_repository(monkeypatch):
    """Test fork_repository operation."""
    # Create test client
    test_client = TestGitHubClient()
    
    # Monkey patch the get_instance method
    monkeypatch.setattr(
        "pygithub_mcp_server.client.client.GitHubClient.get_instance",
        lambda: test_client
    )
    
    # Create parameters
    params = ForkRepositoryParams(
        owner="test-owner",
        repo="test-repo",
        organization="test-org"
    )
    
    # Call the operation
    result = repositories.fork_repository(params)
    
    # Assert expected behavior
    assert result["name"] == "test-repo"
    assert result["full_name"] == "test-org/test-repo"
    assert result["owner"] == "test-org"
    assert "Fork of" in result["description"]
    assert result["html_url"] == "https://github.com/test-org/test-repo"


def test_search_repositories(monkeypatch):
    """Test search_repositories operation."""
    # Create test client
    test_client = TestGitHubClient()
    
    # Monkey patch the get_instance method
    monkeypatch.setattr(
        "pygithub_mcp_server.client.client.GitHubClient.get_instance",
        lambda: test_client
    )
    
    # Create parameters
    params = SearchRepositoriesParams(
        query="language:python stars:>1000",
        page=1,
        per_page=10
    )
    
    # Call the operation
    result = repositories.search_repositories(params)
    
    # Assert expected behavior
    assert len(result) == 2
    assert result[0]["name"] == "repo1"
    assert result[0]["full_name"] == "owner/repo1"
    assert result[0]["owner"] == "owner"
    assert result[1]["name"] == "repo2"


def test_get_file_contents_file(monkeypatch):
    """Test get_file_contents operation for a file."""
    # Create test client
    test_client = TestGitHubClient()
    
    # Monkey patch the get_instance method
    monkeypatch.setattr(
        "pygithub_mcp_server.client.client.GitHubClient.get_instance",
        lambda: test_client
    )
    
    # Create parameters
    params = GetFileContentsParams(
        owner="test-owner",
        repo="test-repo",
        path="README.md",
        branch="main"
    )
    
    # Monkey patch the convert_file_content function
    monkeypatch.setattr(
        "pygithub_mcp_server.converters.repositories.contents.convert_file_content",
        lambda file: {
            "name": file.name,
            "path": file.path,
            "sha": file.sha,
            "size": file.size,
            "type": file.type,
            "encoding": file.encoding,
            "content": file.content,
            "url": file.url,
            "html_url": file.html_url,
            "download_url": file.download_url
        }
    )
    
    # Call the operation
    result = repositories.get_file_contents(params)
    
    # Assert expected behavior
    assert result["name"] == "README.md"
    assert result["path"] == "README.md"
    assert result["sha"] == "file123"
    assert result["size"] == 100
    assert result["type"] == "file"
    assert result["encoding"] == "base64"
    assert result["content"] == "SGVsbG8gV29ybGQh"


def test_get_file_contents_directory(monkeypatch):
    """Test get_file_contents operation for a directory."""
    # Create test client
    test_client = TestGitHubClient()
    
    # Monkey patch the get_instance method
    monkeypatch.setattr(
        "pygithub_mcp_server.client.client.GitHubClient.get_instance",
        lambda: test_client
    )
    
    # Create parameters
    params = GetFileContentsParams(
        owner="test-owner",
        repo="test-repo",
        path="src",
        branch="main"
    )
    
    # Monkey patch the convert_file_content function
    monkeypatch.setattr(
        "pygithub_mcp_server.converters.repositories.contents.convert_file_content",
        lambda file: {
            "name": file.name,
            "path": file.path,
            "sha": file.sha,
            "size": file.size,
            "type": file.type,
            "url": file.url,
            "html_url": file.html_url,
            "download_url": file.download_url
        }
    )
    
    # Call the operation
    result = repositories.get_file_contents(params)
    
    # Assert expected behavior
    assert result["is_directory"] is True
    assert result["path"] == "src"
    assert len(result["contents"]) == 2
    assert result["contents"][0]["name"] == "file1.md"
    assert result["contents"][1]["name"] == "file2.py"


def test_create_or_update_file(monkeypatch):
    """Test create_or_update_file operation."""
    # Create test client
    test_client = TestGitHubClient()
    
    # Monkey patch the get_instance method
    monkeypatch.setattr(
        "pygithub_mcp_server.client.client.GitHubClient.get_instance",
        lambda: test_client
    )
    
    # Create parameters
    params = CreateOrUpdateFileParams(
        owner="test-owner",
        repo="test-repo",
        path="README.md",
        content="# New Content",
        message="Update README",
        branch="main"
    )
    
    # Call the operation
    result = repositories.create_or_update_file(params)
    
    # Assert expected behavior
    assert result["commit"]["sha"] == "newcommit123"
    assert result["commit"]["message"] == "Update README"
    assert "html_url" in result["commit"]
    assert result["content"]["path"] == "README.md"
    assert result["content"]["sha"] == "newfile123"
    assert "html_url" in result["content"]


def test_push_files(monkeypatch):
    """Test push_files operation."""
    # Create test client
    test_client = TestGitHubClient()
    
    # Monkey patch the get_instance method
    monkeypatch.setattr(
        "pygithub_mcp_server.client.client.GitHubClient.get_instance",
        lambda: test_client
    )
    
    # Create parameters
    files = [
        FileContent(path="README.md", content="# Test Repository"),
        FileContent(path="src/main.py", content="print('Hello World')")
    ]
    params = PushFilesParams(
        owner="test-owner",
        repo="test-repo",
        branch="main",
        files=files,
        message="Add initial files"
    )
    
    # Call the operation
    result = repositories.push_files(params)
    
    # Assert expected behavior
    assert result["message"] == "Add initial files"
    assert result["branch"] == "main"
    assert len(result["files"]) == 2
    assert result["files"][0]["path"] == "README.md"
    assert result["files"][1]["path"] == "src/main.py"


def test_create_branch(monkeypatch):
    """Test create_branch operation."""
    # Create test client
    test_client = TestGitHubClient()
    
    # Monkey patch the get_instance method
    monkeypatch.setattr(
        "pygithub_mcp_server.client.client.GitHubClient.get_instance",
        lambda: test_client
    )
    
    # Create parameters
    params = CreateBranchParams(
        owner="test-owner",
        repo="test-repo",
        branch="feature",
        from_branch="main"
    )
    
    # Call the operation
    result = repositories.create_branch(params)
    
    # Assert expected behavior
    assert result["name"] == "feature"
    assert result["sha"] == "abc123def456"
    assert "url" in result


def test_list_commits(monkeypatch):
    """Test list_commits operation."""
    # Create test client
    test_client = TestGitHubClient()
    
    # Monkey patch the get_instance method
    monkeypatch.setattr(
        "pygithub_mcp_server.client.client.GitHubClient.get_instance",
        lambda: test_client
    )
    
    # Create parameters
    params = ListCommitsParams(
        owner="test-owner",
        repo="test-repo",
        page=1,
        per_page=10
    )
    
    # Call the operation
    result = repositories.list_commits(params)
    
    # Assert expected behavior
    assert len(result) == 2
    assert result[0]["sha"] == "abc123"
    assert result[0]["message"] == "First commit"
    assert "author" in result[0]
    assert "html_url" in result[0]
    assert result[1]["sha"] == "def456"
    assert result[1]["message"] == "Second commit"
