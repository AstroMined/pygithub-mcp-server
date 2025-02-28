"""Pull request-related schema models.

This module defines Pydantic models for GitHub pull request operations
including creation, updates, and comments.
"""

from typing import Optional
from pydantic import Field

from .base import RepositoryRef


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
