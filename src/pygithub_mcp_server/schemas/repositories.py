"""Repository-related schema models.

This module defines Pydantic models for GitHub repository operations
such as creating, searching, and managing repositories.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

from .base import RepositoryRef, FileContent


class CreateOrUpdateFileParams(RepositoryRef):
    """Parameters for creating or updating a single file."""

    model_config = ConfigDict(strict=True)
    
    path: str = Field(..., description="Path where to create/update the file")
    content: str = Field(..., description="Content of the file")
    message: str = Field(..., description="Commit message")
    branch: str = Field(..., description="Branch to create/update the file in")
    sha: Optional[str] = Field(None, description="SHA of file being replaced (for updates)")

    @field_validator('path')
    @classmethod
    def validate_path(cls, v):
        """Validate that path is not empty."""
        if not v.strip():
            raise ValueError("path cannot be empty")
        return v

    @field_validator('content')
    @classmethod
    def validate_content(cls, v):
        """Validate that content is not empty."""
        if not v.strip():
            raise ValueError("content cannot be empty")
        return v

    @field_validator('message')
    @classmethod
    def validate_message(cls, v):
        """Validate that message is not empty."""
        if not v.strip():
            raise ValueError("message cannot be empty")
        return v

    @field_validator('branch')
    @classmethod
    def validate_branch(cls, v):
        """Validate that branch is not empty."""
        if not v.strip():
            raise ValueError("branch cannot be empty")
        return v


class PushFilesParams(RepositoryRef):
    """Parameters for pushing multiple files in a single commit."""

    model_config = ConfigDict(strict=True)
    
    branch: str = Field(..., description="Branch to push to")
    files: List[FileContent] = Field(..., description="Files to push")
    message: str = Field(..., description="Commit message")

    @field_validator('branch')
    @classmethod
    def validate_branch(cls, v):
        """Validate that branch is not empty."""
        if not v.strip():
            raise ValueError("branch cannot be empty")
        return v

    @field_validator('files')
    @classmethod
    def validate_files(cls, v):
        """Validate that files list is not empty."""
        if not v:
            raise ValueError("files list cannot be empty")
        return v

    @field_validator('message')
    @classmethod
    def validate_message(cls, v):
        """Validate that message is not empty."""
        if not v.strip():
            raise ValueError("message cannot be empty")
        return v


class SearchRepositoriesParams(BaseModel):
    """Parameters for searching repositories."""

    model_config = ConfigDict(strict=True)
    
    query: str = Field(..., description="Search query")
    page: Optional[int] = Field(None, description="Page number for pagination")
    per_page: Optional[int] = Field(
        None, description="Number of results per page (default: 30, max: 100)"
    )

    @field_validator('query')
    @classmethod
    def validate_query(cls, v):
        """Validate that query is not empty."""
        if not v.strip():
            raise ValueError("query cannot be empty")
        return v

    @field_validator('page')
    @classmethod
    def validate_page(cls, v):
        """Validate that page is a positive integer."""
        if v is not None and v < 1:
            raise ValueError("page must be a positive integer")
        return v

    @field_validator('per_page')
    @classmethod
    def validate_per_page(cls, v):
        """Validate that per_page is within allowed range."""
        if v is not None:
            if v < 1:
                raise ValueError("per_page must be a positive integer")
            if v > 100:
                raise ValueError("per_page cannot exceed 100")
        return v


class CreateRepositoryParams(BaseModel):
    """Parameters for creating a new repository."""

    model_config = ConfigDict(strict=True)
    
    name: str = Field(..., description="Repository name")
    description: Optional[str] = Field(None, description="Repository description")
    private: Optional[bool] = Field(None, description="Whether repo should be private")
    auto_init: Optional[bool] = Field(
        None, description="Initialize repository with README"
    )

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate that name is not empty."""
        if not v.strip():
            raise ValueError("name cannot be empty")
        return v


class GetFileContentsParams(RepositoryRef):
    """Parameters for getting file contents."""

    model_config = ConfigDict(strict=True)
    
    path: str = Field(..., description="Path to file/directory")
    branch: Optional[str] = Field(None, description="Branch to get contents from")

    @field_validator('path')
    @classmethod
    def validate_path(cls, v):
        """Validate that path is not empty."""
        if not v.strip():
            raise ValueError("path cannot be empty")
        return v


class ForkRepositoryParams(RepositoryRef):
    """Parameters for forking a repository."""

    model_config = ConfigDict(strict=True)
    
    organization: Optional[str] = Field(
        None, description="Organization to fork to (defaults to user account)"
    )


class CreateBranchParams(RepositoryRef):
    """Parameters for creating a branch."""

    model_config = ConfigDict(strict=True)
    
    branch: str = Field(..., description="Name for new branch")
    from_branch: Optional[str] = Field(
        None, description="Source branch (defaults to repo default)"
    )

    @field_validator('branch')
    @classmethod
    def validate_branch(cls, v):
        """Validate that branch is not empty."""
        if not v.strip():
            raise ValueError("branch cannot be empty")
        return v


class ListCommitsParams(RepositoryRef):
    """Parameters for listing commits."""

    model_config = ConfigDict(strict=True)
    
    page: Optional[int] = Field(None, description="Page number")
    per_page: Optional[int] = Field(None, description="Results per page")
    sha: Optional[str] = Field(None, description="Branch name or commit SHA")

    @field_validator('page')
    @classmethod
    def validate_page(cls, v):
        """Validate that page is a positive integer."""
        if v is not None and v < 1:
            raise ValueError("page must be a positive integer")
        return v

    @field_validator('per_page')
    @classmethod
    def validate_per_page(cls, v):
        """Validate that per_page is within allowed range."""
        if v is not None:
            if v < 1:
                raise ValueError("per_page must be a positive integer")
            if v > 100:
                raise ValueError("per_page cannot exceed 100")
        return v
