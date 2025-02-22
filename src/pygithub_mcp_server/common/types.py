"""Type definitions and schema models for GitHub MCP Server.

This module defines Pydantic models for request/response validation and
JSON schema generation. These models correspond to GitHub API structures
and MCP tool interfaces.
"""

from datetime import datetime
from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field


class RepositoryRef(BaseModel):
    """Reference to a GitHub repository."""

    owner: str = Field(..., description="Repository owner (username or organization)")
    repo: str = Field(..., description="Repository name")


class FileContent(BaseModel):
    """Content of a file to create or update."""

    path: str = Field(..., description="Path where to create/update the file")
    content: str = Field(..., description="Content of the file")


class CreateOrUpdateFileParams(RepositoryRef):
    """Parameters for creating or updating a single file."""

    path: str = Field(..., description="Path where to create/update the file")
    content: str = Field(..., description="Content of the file")
    message: str = Field(..., description="Commit message")
    branch: str = Field(..., description="Branch to create/update the file in")
    sha: Optional[str] = Field(None, description="SHA of file being replaced (for updates)")


class PushFilesParams(RepositoryRef):
    """Parameters for pushing multiple files in a single commit."""

    branch: str = Field(..., description="Branch to push to")
    files: List[FileContent] = Field(..., description="Files to push")
    message: str = Field(..., description="Commit message")


class SearchRepositoriesParams(BaseModel):
    """Parameters for searching repositories."""

    query: str = Field(..., description="Search query")
    page: Optional[int] = Field(None, description="Page number for pagination")
    per_page: Optional[int] = Field(
        None, description="Number of results per page (default: 30, max: 100)"
    )


class CreateRepositoryParams(BaseModel):
    """Parameters for creating a new repository."""

    name: str = Field(..., description="Repository name")
    description: Optional[str] = Field(None, description="Repository description")
    private: Optional[bool] = Field(None, description="Whether repo should be private")
    auto_init: Optional[bool] = Field(
        None, description="Initialize repository with README"
    )


class GetFileContentsParams(RepositoryRef):
    """Parameters for getting file contents."""

    path: str = Field(..., description="Path to file/directory")
    branch: Optional[str] = Field(None, description="Branch to get contents from")


class CreateIssueParams(RepositoryRef):
    """Parameters for creating an issue."""

    title: str = Field(..., description="Issue title")
    body: Optional[str] = Field(None, description="Issue description")
    assignees: List[str] = Field(default_factory=list, description="Usernames to assign")
    labels: List[str] = Field(default_factory=list, description="Labels to add")
    milestone: Optional[int] = Field(None, description="Milestone number")


class CreatePullRequestParams(RepositoryRef):
    """Parameters for creating a pull request."""

    title: str = Field(..., description="Pull request title")
    head: str = Field(..., description="Branch containing changes")
    base: str = Field(..., description="Branch to merge into")
    body: Optional[str] = Field(None, description="Pull request description")
    draft: Optional[bool] = Field(None, description="Create as draft PR")
    maintainer_can_modify: Optional[bool] = Field(
        None, description="Allow maintainer edits"
    )


class ForkRepositoryParams(RepositoryRef):
    """Parameters for forking a repository."""

    organization: Optional[str] = Field(
        None, description="Organization to fork to (defaults to user account)"
    )


class CreateBranchParams(RepositoryRef):
    """Parameters for creating a branch."""

    branch: str = Field(..., description="Name for new branch")
    from_branch: Optional[str] = Field(
        None, description="Source branch (defaults to repo default)"
    )


class ListIssuesParams(RepositoryRef):
    """Parameters for listing issues."""

    state: Optional[str] = Field(None, description="Issue state (open, closed, all)")
    labels: Optional[List[str]] = Field(None, description="Filter by labels")
    sort: Optional[str] = Field(
        None, description="Sort by (created, updated, comments)"
    )
    direction: Optional[str] = Field(None, description="Sort direction (asc, desc)")
    since: Optional[datetime] = Field(None, description="Filter by date")
    page: Optional[int] = Field(None, description="Page number")
    per_page: Optional[int] = Field(None, description="Results per page")


class UpdateIssueParams(RepositoryRef):
    """Parameters for updating an issue."""

    issue_number: int = Field(..., description="Issue number to update")
    title: Optional[str] = Field(None, description="New title")
    body: Optional[str] = Field(None, description="New description")
    state: Optional[str] = Field(None, description="New state (open or closed)")
    labels: Optional[List[str]] = Field(None, description="New labels")
    assignees: Optional[List[str]] = Field(None, description="New assignees")
    milestone: Optional[int] = Field(None, description="New milestone number")


class IssueCommentParams(RepositoryRef):
    """Parameters for adding a comment to an issue."""

    issue_number: int = Field(..., description="Issue number to comment on")
    body: str = Field(..., description="Comment text")


class SearchParams(BaseModel):
    """Base parameters for search operations."""

    q: str = Field(..., description="Search query")
    sort: Optional[str] = Field(None, description="Sort field")
    order: Optional[str] = Field(None, description="Sort order (asc or desc)")
    per_page: Optional[int] = Field(
        None, description="Results per page (max 100)"
    )
    page: Optional[int] = Field(None, description="Page number")


class SearchCodeParams(SearchParams):
    """Parameters for searching code."""

    pass


class SearchIssuesParams(SearchParams):
    """Parameters for searching issues and pull requests."""

    pass


class SearchUsersParams(SearchParams):
    """Parameters for searching users."""

    pass


class ListCommitsParams(RepositoryRef):
    """Parameters for listing commits."""

    page: Optional[int] = Field(None, description="Page number")
    per_page: Optional[int] = Field(None, description="Results per page")
    sha: Optional[str] = Field(None, description="Branch name or commit SHA")


class GetIssueParams(RepositoryRef):
    """Parameters for getting an issue."""

    issue_number: int = Field(..., description="Issue number to retrieve")


# Response types
class ToolResponse(BaseModel):
    """Base model for tool responses."""

    content: List[dict] = Field(..., description="Response content")
    is_error: Optional[bool] = Field(None, description="Whether response is an error")


class TextContent(BaseModel):
    """Text content in a tool response."""

    type: Literal["text"] = "text"
    text: str = Field(..., description="Text content")


class ErrorContent(BaseModel):
    """Error content in a tool response."""

    type: Literal["error"] = "error"
    text: str = Field(..., description="Error message")


ResponseContent = Union[TextContent, ErrorContent]
