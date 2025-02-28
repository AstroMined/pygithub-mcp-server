"""Repository-related schema models.

This module defines Pydantic models for GitHub repository operations
such as creating, searching, and managing repositories.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

from .base import RepositoryRef, FileContent


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


class ListCommitsParams(RepositoryRef):
    """Parameters for listing commits."""

    page: Optional[int] = Field(None, description="Page number")
    per_page: Optional[int] = Field(None, description="Results per page")
    sha: Optional[str] = Field(None, description="Branch name or commit SHA")
