"""Tests for response schema models.

This module tests the schema models used for MCP tool responses.
"""

import pytest
from pydantic import ValidationError

from pygithub_mcp_server.schemas.responses import (
    ToolResponse,
    TextContent,
    ErrorContent,
    ResponseContent,
)


class TestToolResponse:
    """Tests for the ToolResponse schema."""

    def test_valid_data(self, valid_tool_response_data):
        """Test that valid data passes validation."""
        response = ToolResponse(**valid_tool_response_data)
        assert response.content == valid_tool_response_data["content"]
        assert response.is_error == valid_tool_response_data["is_error"]

    def test_minimal_valid_data(self):
        """Test with minimal valid data (only required fields)."""
        # Only content is required
        response = ToolResponse(
            content=[{"type": "text", "text": "Operation completed successfully."}]
        )
        assert len(response.content) == 1
        assert response.content[0]["type"] == "text"
        assert response.content[0]["text"] == "Operation completed successfully."
        assert response.is_error is None

    def test_missing_required_fields(self):
        """Test that missing required fields raise validation errors."""
        # Missing content
        with pytest.raises(ValidationError) as exc_info:
            ToolResponse()
        assert "content" in str(exc_info.value).lower()

    def test_invalid_content_type(self):
        """Test that invalid content type raises validation error."""
        # String instead of list
        with pytest.raises(ValidationError) as exc_info:
            ToolResponse(content="Invalid content")
        assert "content" in str(exc_info.value).lower()

    def test_empty_content_list(self):
        """Test behavior with empty content list."""
        # Empty content list - should be valid
        with pytest.raises(ValidationError) as exc_info:
            ToolResponse(content=[])
        assert "content" in str(exc_info.value).lower()

    def test_is_error_values(self):
        """Test behavior with different is_error values."""
        # True is_error
        response = ToolResponse(
            content=[{"type": "error", "text": "An error occurred."}],
            is_error=True
        )
        assert response.is_error is True

        # False is_error
        response = ToolResponse(
            content=[{"type": "text", "text": "Operation completed successfully."}],
            is_error=False
        )
        assert response.is_error is False

        # None is_error (default)
        response = ToolResponse(
            content=[{"type": "text", "text": "Operation completed successfully."}]
        )
        assert response.is_error is None


class TestTextContent:
    """Tests for the TextContent schema."""

    def test_valid_data(self, valid_text_content_data):
        """Test that valid data passes validation."""
        content = TextContent(**valid_text_content_data)
        assert content.type == "text"
        assert content.text == valid_text_content_data["text"]

    def test_missing_required_fields(self):
        """Test that missing required fields raise validation errors."""
        # Missing text
        with pytest.raises(ValidationError) as exc_info:
            TextContent()
        assert "text" in str(exc_info.value).lower()

    def test_invalid_type_value(self):
        """Test that invalid type value raises validation error."""
        # Invalid type value
        with pytest.raises(ValidationError) as exc_info:
            TextContent(type="invalid", text="Some text")
        assert "type" in str(exc_info.value).lower()

    def test_empty_text(self):
        """Test behavior with empty text."""
        # Empty text - should be valid
        content = TextContent(text="")
        assert content.type == "text"
        assert content.text == ""


class TestErrorContent:
    """Tests for the ErrorContent schema."""

    def test_valid_data(self, valid_error_content_data):
        """Test that valid data passes validation."""
        content = ErrorContent(**valid_error_content_data)
        assert content.type == "error"
        assert content.text == valid_error_content_data["text"]

    def test_missing_required_fields(self):
        """Test that missing required fields raise validation errors."""
        # Missing text
        with pytest.raises(ValidationError) as exc_info:
            ErrorContent()
        assert "text" in str(exc_info.value).lower()

    def test_invalid_type_value(self):
        """Test that invalid type value raises validation error."""
        # Invalid type value
        with pytest.raises(ValidationError) as exc_info:
            ErrorContent(type="invalid", text="An error occurred.")
        assert "type" in str(exc_info.value).lower()

    def test_empty_text(self):
        """Test behavior with empty text."""
        # Empty text - should be valid
        content = ErrorContent(text="")
        assert content.type == "error"
        assert content.text == ""


class TestResponseContent:
    """Tests for the ResponseContent union type."""

    def test_text_content(self):
        """Test that TextContent is a valid ResponseContent."""
        content: ResponseContent = TextContent(text="Operation completed successfully.")
        assert content.type == "text"
        assert content.text == "Operation completed successfully."

    def test_error_content(self):
        """Test that ErrorContent is a valid ResponseContent."""
        content: ResponseContent = ErrorContent(text="An error occurred.")
        assert content.type == "error"
        assert content.text == "An error occurred."
