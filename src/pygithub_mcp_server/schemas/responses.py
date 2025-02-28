"""Response schema models.

This module defines Pydantic models for MCP tool responses
including text and error content types.
"""

from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field


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


# Define the union type for response content
ResponseContent = Union[TextContent, ErrorContent]
