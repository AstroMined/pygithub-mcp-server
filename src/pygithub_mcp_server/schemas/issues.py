"""Issue-related schema models.

This module defines Pydantic models for GitHub issue operations
including issue creation, updates, comments, and labels.

All models include strict validation to ensure data integrity
before passing to PyGithub methods.
"""

from datetime import datetime
from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field, field_validator, ConfigDict

from .base import RepositoryRef

# Valid values for issue state
VALID_ISSUE_STATES = ["open", "closed", "all"]

# Valid values for sort field
VALID_SORT_VALUES = ["created", "updated", "comments"]

# Valid values for direction
VALID_DIRECTION_VALUES = ["asc", "desc"]


class CreateIssueParams(RepositoryRef):
    """Parameters for creating an issue."""

    model_config = ConfigDict(strict=True)
    
    title: str = Field(..., description="Issue title", strict=True)
    body: Optional[str] = Field(None, description="Issue description", strict=True)
    assignees: List[str] = Field(default_factory=list, description="Usernames to assign", strict=True)
    labels: List[str] = Field(default_factory=list, description="Labels to add", strict=True)
    milestone: Optional[int] = Field(None, description="Milestone number", strict=True)
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        """Validate that title is not empty."""
        if not v.strip():
            raise ValueError("title cannot be empty")
        return v


class ListIssuesParams(RepositoryRef):
    """Parameters for listing issues."""

    model_config = ConfigDict(strict=True)
    
    state: Optional[str] = Field(
        None, 
        description=f"Issue state: {', '.join(VALID_ISSUE_STATES)}"
    )
    labels: Optional[List[str]] = Field(
        None, 
        description="Filter by labels (list of label names)"
    )
    sort: Optional[str] = Field(
        None, 
        description=f"Sort by: {', '.join(VALID_SORT_VALUES)}"
    )
    direction: Optional[str] = Field(
        None, 
        description=f"Sort direction: {', '.join(VALID_DIRECTION_VALUES)}"
    )
    since: Optional[datetime] = Field(
        None, 
        description="Filter by date (ISO 8601 format with timezone: YYYY-MM-DDThh:mm:ssZ)"
    )
    page: Optional[int] = Field(
        None, 
        description="Page number for pagination (1-based)"
    )
    per_page: Optional[int] = Field(
        None, 
        description="Results per page (max 100)"
    )
    
    @field_validator('state')
    @classmethod
    def validate_state(cls, v):
        """Validate that state is one of the allowed values."""
        if v is not None and v not in VALID_ISSUE_STATES:
            raise ValueError(f"Invalid state: {v}. Must be one of: {', '.join(VALID_ISSUE_STATES)}")
        return v
    
    @field_validator('sort')
    @classmethod
    def validate_sort(cls, v):
        """Validate that sort is one of the allowed values."""
        if v is not None and v not in VALID_SORT_VALUES:
            raise ValueError(f"Invalid sort value: {v}. Must be one of: {', '.join(VALID_SORT_VALUES)}")
        return v
    
    @field_validator('direction')
    @classmethod
    def validate_direction(cls, v):
        """Validate that direction is one of the allowed values."""
        if v is not None and v not in VALID_DIRECTION_VALUES:
            raise ValueError(f"Invalid direction: {v}. Must be one of: {', '.join(VALID_DIRECTION_VALUES)}")
        return v
    
    @field_validator('page')
    @classmethod
    def validate_page(cls, v):
        """Validate that page is a positive integer."""
        if v is not None and v < 1:
            raise ValueError("Page number must be a positive integer")
        return v
    
    @field_validator('per_page')
    @classmethod
    def validate_per_page(cls, v):
        """Validate that per_page is a positive integer <= 100."""
        if v is not None:
            if v < 1:
                raise ValueError("Results per page must be a positive integer")
            if v > 100:
                raise ValueError("Results per page cannot exceed 100")
        return v
    
    @field_validator('since', mode='before')
    @classmethod
    def validate_since(cls, v):
        """Convert string dates to datetime objects.
        
        Accepts:
        - ISO 8601 format strings with timezone (e.g., "2020-01-01T00:00:00Z")
        - datetime objects
        
        Returns:
        - datetime object
        
        Raises:
        - ValueError: If the string is not a valid ISO 8601 datetime with timezone
        """
        if isinstance(v, str):
            # Check for ISO format with time component and timezone
            if not ('T' in v and ('+' in v or 'Z' in v or '-' in v.split('T')[1])):
                raise ValueError(
                    f"Invalid ISO format datetime: {v}. "
                    f"Must be in format YYYY-MM-DDThh:mm:ss+00:00 or YYYY-MM-DDThh:mm:ssZ"
                )
            
            try:
                # Handle 'Z' timezone indicator by replacing with +00:00
                v = v.replace('Z', '+00:00')
                return datetime.fromisoformat(v)
            except ValueError:
                raise ValueError(
                    f"Invalid ISO format datetime: {v}. "
                    f"Contains invalid date/time components."
                )
        return v


class GetIssueParams(RepositoryRef):
    """Parameters for getting an issue."""

    model_config = ConfigDict(strict=True)
    
    issue_number: int = Field(..., description="Issue number to retrieve", strict=True)


class UpdateIssueParams(RepositoryRef):
    """Parameters for updating an issue."""

    model_config = ConfigDict(strict=True)
    
    issue_number: int = Field(..., description="Issue number to update")
    title: Optional[str] = Field(None, description="New title")
    body: Optional[str] = Field(None, description="New description")
    state: Optional[str] = Field(
        None, 
        description="New state (open or closed)"
    )
    labels: Optional[List[str]] = Field(
        None, 
        description="New labels (list of label names)"
    )
    assignees: Optional[List[str]] = Field(
        None, 
        description="New assignees (list of usernames)"
    )
    milestone: Optional[int] = Field(
        None, 
        description="New milestone number (or None to clear)"
    )
    
    @field_validator('state')
    @classmethod
    def validate_state(cls, v):
        """Validate that state is one of the allowed values."""
        # For update, only open and closed are valid (not 'all')
        valid_states = ["open", "closed"]
        if v is not None and v not in valid_states:
            raise ValueError(f"Invalid state: {v}. Must be one of: {', '.join(valid_states)}")
        return v
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        """Validate that title is not empty if provided."""
        if v is not None and not v.strip():
            raise ValueError("title cannot be empty")
        return v


class IssueCommentParams(RepositoryRef):
    """Parameters for adding a comment to an issue."""

    model_config = ConfigDict(strict=True)
    
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

    model_config = ConfigDict(strict=True)
    
    issue_number: int = Field(..., description="Issue number to list comments for")
    since: Optional[datetime] = Field(
        None, 
        description="Filter by date (ISO 8601 format with timezone: YYYY-MM-DDThh:mm:ssZ)"
    )
    page: Optional[int] = Field(
        None, 
        description="Page number for pagination (1-based)"
    )
    per_page: Optional[int] = Field(
        None, 
        description="Results per page (max 100)"
    )
    
    @field_validator('page')
    @classmethod
    def validate_page(cls, v):
        """Validate that page is a positive integer."""
        if v is not None and v < 1:
            raise ValueError("Page number must be a positive integer")
        return v
    
    @field_validator('per_page')
    @classmethod
    def validate_per_page(cls, v):
        """Validate that per_page is a positive integer <= 100."""
        if v is not None:
            if v < 1:
                raise ValueError("Results per page must be a positive integer")
            if v > 100:
                raise ValueError("Results per page cannot exceed 100")
        return v
    
    @field_validator('since', mode='before')
    @classmethod
    def validate_since(cls, v):
        """Convert string dates to datetime objects.
        
        Accepts:
        - ISO 8601 format strings with timezone (e.g., "2020-01-01T00:00:00Z")
        - datetime objects
        
        Returns:
        - datetime object
        
        Raises:
        - ValueError: If the string is not a valid ISO 8601 datetime with timezone
        """
        if isinstance(v, str):
            # Check for ISO format with time component and timezone
            if not ('T' in v and ('+' in v or 'Z' in v or '-' in v.split('T')[1])):
                raise ValueError(
                    f"Invalid ISO format datetime: {v}. "
                    f"Must be in format YYYY-MM-DDThh:mm:ss+00:00 or YYYY-MM-DDThh:mm:ssZ"
                )
            
            try:
                # Handle 'Z' timezone indicator by replacing with +00:00
                v = v.replace('Z', '+00:00')
                return datetime.fromisoformat(v)
            except ValueError:
                raise ValueError(
                    f"Invalid ISO format datetime: {v}. "
                    f"Contains invalid date/time components."
                )
        return v


class UpdateIssueCommentParams(RepositoryRef):
    """Parameters for updating an issue comment."""

    model_config = ConfigDict(strict=True)
    
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

    model_config = ConfigDict(strict=True)
    
    issue_number: int = Field(..., description="Issue number containing the comment")
    comment_id: int = Field(..., description="Comment ID to delete")


class AddIssueLabelsParams(RepositoryRef):
    """Parameters for adding labels to an issue."""

    model_config = ConfigDict(strict=True)
    
    issue_number: int = Field(..., description="Issue number")
    labels: List[str] = Field(..., description="Labels to add")
    
    @field_validator('labels')
    @classmethod
    def validate_labels(cls, v):
        """Validate that labels list is not empty."""
        if not v:
            raise ValueError("labels list cannot be empty")
        return v


class RemoveIssueLabelParams(RepositoryRef):
    """Parameters for removing a label from an issue."""

    model_config = ConfigDict(strict=True)
    
    issue_number: int = Field(..., description="Issue number")
    label: str = Field(..., description="Label to remove")
    
    @field_validator('label')
    @classmethod
    def validate_label(cls, v):
        """Validate that label is not empty."""
        if not v.strip():
            raise ValueError("label cannot be empty")
        return v
