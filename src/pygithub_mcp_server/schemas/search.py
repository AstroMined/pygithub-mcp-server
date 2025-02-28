"""Search-related schema models.

This module defines Pydantic models for GitHub search operations
across repositories, code, issues, and users.
"""

from typing import Optional
from pydantic import BaseModel, Field


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
