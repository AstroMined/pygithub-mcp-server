"""Tests for response conversion functions.

This module tests the response conversion functions used to convert between
PyGithub objects and our response formats.
"""

import pytest
from datetime import datetime, timezone

from pygithub_mcp_server.converters.responses import (
    create_tool_response,
    create_error_response,
)


class TestCreateToolResponse:
    """Tests for create_tool_response function."""

    def test_with_string_content(self):
        """Test with string content."""
        response = create_tool_response("Test response")
        
        assert not response["is_error"]
        assert len(response["content"]) == 1
        assert response["content"][0]["type"] == "text"
        assert response["content"][0]["text"] == "Test response"

    def test_with_dict_content(self):
        """Test with dictionary content."""
        data = {"key": "value", "nested": {"inner": "data"}}
        response = create_tool_response(data)
        
        assert not response["is_error"]
        assert len(response["content"]) == 1
        assert response["content"][0]["type"] == "text"
        # Should be JSON-formatted
        assert "key" in response["content"][0]["text"]
        assert "value" in response["content"][0]["text"]
        assert "nested" in response["content"][0]["text"]
        assert "inner" in response["content"][0]["text"]
        assert "data" in response["content"][0]["text"]

    def test_with_list_content(self):
        """Test with list content."""
        data = [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]
        response = create_tool_response(data)
        
        assert not response["is_error"]
        assert len(response["content"]) == 1
        assert response["content"][0]["type"] == "text"
        # Should be JSON-formatted
        assert "id" in response["content"][0]["text"]
        assert "name" in response["content"][0]["text"]
        assert "Item 1" in response["content"][0]["text"]
        assert "Item 2" in response["content"][0]["text"]

    def test_with_error_flag(self):
        """Test with error flag set."""
        response = create_tool_response("Error message", is_error=True)
        
        assert response["is_error"]
        assert len(response["content"]) == 1
        assert response["content"][0]["type"] == "text"
        assert response["content"][0]["text"] == "Error message"

    def test_with_none_content(self):
        """Test with None content."""
        response = create_tool_response(None)
        
        assert not response["is_error"]
        assert len(response["content"]) == 1
        assert response["content"][0]["type"] == "text"
        assert response["content"][0]["text"] == "null"


class TestCreateErrorResponse:
    """Tests for create_error_response function."""

    def test_with_string_error(self):
        """Test with string error."""
        response = create_error_response("Test error")
        
        assert response["is_error"]
        assert len(response["content"]) == 1
        assert response["content"][0]["type"] == "text"
        assert response["content"][0]["text"] == "Test error"

    def test_with_exception(self):
        """Test with exception object."""
        try:
            raise ValueError("Test exception")
        except ValueError as e:
            response = create_error_response(e)
        
        assert response["is_error"]
        assert len(response["content"]) == 1
        assert response["content"][0]["type"] == "text"
        assert "Test exception" in response["content"][0]["text"]

    def test_with_dict_error(self):
        """Test with dictionary error."""
        error_data = {"code": 404, "message": "Not found"}
        response = create_error_response(error_data)
        
        assert response["is_error"]
        assert len(response["content"]) == 1
        assert response["content"][0]["type"] == "text"
        # Should be JSON-formatted
        assert "code" in response["content"][0]["text"]
        assert "404" in response["content"][0]["text"]
        assert "message" in response["content"][0]["text"]
        assert "Not found" in response["content"][0]["text"]
