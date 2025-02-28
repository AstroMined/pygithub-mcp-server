"""Issue-related schema models.

This module defines Pydantic models for GitHub issue operations
including issue creation, updates, comments, and labels.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from .base import RepositoryRef


class CreateIssueParams(RepositoryRef):
    """Parameters for creating an issue."""

    title: str = Field(..., description="Issue title")
    body: Optional[str] = Field(None, description="Issue description")
    assignees: List[str] = Field(default_factory=list, description="Usernames to assign")
    labels: List[str] = Field(default_factory=list, description="Labels to add")
    milestone: Optional[int] = Field(None, description="Milestone number")
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        """Validate that title is not empty."""
        if not v.strip():
            raise ValueError("title cannot be empty")
        return v


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


class GetIssueParams(RepositoryRef):
    """Parameters for getting an issue."""

    issue_number: int = Field(..., description="Issue number to retrieve")


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
    
    @field_validator('body')
    @classmethod
    def validate_body(cls, v):
        """Validate that body is not empty."""
        if not v.strip():
            raise ValueError("body cannot be empty")
        return v


class ListIssueCommentsParams(RepositoryRef):
    """Parameters for listing comments on an issue."""

    issue_number: int = Field(..., description="Issue number to list comments for")
    since: Optional[datetime] = Field(None, description="Filter by date")
    page: Optional[int] = Field(None, description="Page number")
    per_page: Optional[int] = Field(None, description="Results per page")


class UpdateIssueCommentParams(RepositoryRef):
    """Parameters for updating an issue comment."""

    issue_number: int = Field(..., description="Issue number containing the comment")
    comment_id: int = Field(..., description="Comment ID to update")
    body: str = Field(..., description="New comment text")
    
    @field_validator('body')
    @classmethod
    def validate_body(cls, v):
        """Validate that body is not empty."""
        if not v.strip():
            raise ValueError("body cannot be empty")
        return v


class DeleteIssueCommentParams(RepositoryRef):
    """Parameters for deleting an issue comment."""

    issue_number: int = Field(..., description="Issue number containing the comment")
    comment_id: int = Field(..., description="Comment ID to delete")


class AddIssueLabelsParams(RepositoryRef):
    """Parameters for adding labels to an issue."""

    issue_number: int = Field(..., description="Issue number")
    labels: List[str] = Field(..., description="Labels to add")


class RemoveIssueLabelParams(RepositoryRef):
    """Parameters for removing a label from an issue."""

    issue_number: int = Field(..., description="Issue number")
    label: str = Field(..., description="Label to remove")
    
    @field_validator('label')
    @classmethod
    def validate_label(cls, v):
        """Validate that label is not empty."""
        if not v.strip():
            raise ValueError("label cannot be empty")
        return v
