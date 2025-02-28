"""Base schema models used across multiple domains.

This module defines common Pydantic models that are used by multiple
domain-specific schema modules.
"""

from pydantic import BaseModel, Field, field_validator


class RepositoryRef(BaseModel):
    """Reference to a GitHub repository."""

    owner: str = Field(..., description="Repository owner (username or organization)")
    repo: str = Field(..., description="Repository name")

    @field_validator('owner')
    @classmethod
    def validate_owner(cls, v):
        """Validate that owner is not empty."""
        if not v.strip():
            raise ValueError("owner cannot be empty")
        return v

    @field_validator('repo')
    @classmethod
    def validate_repo(cls, v):
        """Validate that repo is not empty."""
        if not v.strip():
            raise ValueError("repo cannot be empty")
        return v


class FileContent(BaseModel):
    """Content of a file to create or update."""

    path: str = Field(..., description="Path where to create/update the file")
    content: str = Field(..., description="Content of the file")

    @field_validator('path')
    @classmethod
    def validate_path(cls, v):
        """Validate that path is not empty."""
        if not v.strip():
            raise ValueError("path cannot be empty")
        return v
