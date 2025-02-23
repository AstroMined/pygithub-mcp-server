"""Tests for utility functions."""

import os
from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from requests import Response

from pygithub_mcp_server.common.errors import (
    GitHubAuthenticationError,
    GitHubConflictError,
    GitHubError,
    GitHubPermissionError,
    GitHubRateLimitError,
    GitHubResourceNotFoundError,
    GitHubValidationError,
)
from pygithub_mcp_server.common.utils import (
    API_BASE_URL,
    DEFAULT_HEADERS,
    build_url,
    create_tool_response,
    format_query_params,
    get_github_token,
    get_session,
    parse_rate_limit_headers,
    process_error_response,
    process_response,
)

# Session/Authentication Tests

def test_get_github_token_success():
    """Test successful token retrieval."""
    with patch.dict(os.environ, {"GITHUB_PERSONAL_ACCESS_TOKEN": "test-token"}):
        assert get_github_token() == "test-token"

def test_get_github_token_missing():
    """Test error when token is missing."""
    with patch.dict(os.environ, clear=True):
        with pytest.raises(GitHubError, match="GITHUB_PERSONAL_ACCESS_TOKEN.*not set"):
            get_github_token()

def test_get_session():
    """Test session creation with proper headers."""
    with patch.dict(os.environ, {"GITHUB_PERSONAL_ACCESS_TOKEN": "test-token"}):
        session = get_session()
        assert session.headers["Accept"] == DEFAULT_HEADERS["Accept"]
        assert session.headers["X-GitHub-Api-Version"] == DEFAULT_HEADERS["X-GitHub-Api-Version"]
        assert session.headers["Authorization"] == "Bearer test-token"

# URL/Request Handling Tests

@pytest.mark.parametrize("endpoint,expected", [
    ("repos/owner/repo", f"{API_BASE_URL}/repos/owner/repo"),
    ("/repos/owner/repo", f"{API_BASE_URL}/repos/owner/repo"),
    ("issues", f"{API_BASE_URL}/issues"),
])
def test_build_url(endpoint: str, expected: str):
    """Test URL building with various endpoints."""
    assert build_url(endpoint) == expected

# Response Processing Tests

def test_parse_rate_limit_headers():
    """Test parsing rate limit headers."""
    response = Mock(spec=Response)
    now = datetime.now()
    timestamp = int(now.timestamp())
    response.headers = {
        "X-RateLimit-Remaining": "42",
        "X-RateLimit-Reset": str(timestamp)
    }
    
    remaining, reset_time = parse_rate_limit_headers(response)
    assert remaining == 42
    assert reset_time.timestamp() == timestamp

def test_parse_rate_limit_headers_missing():
    """Test parsing rate limit headers with missing values."""
    response = Mock(spec=Response)
    response.headers = {}
    
    remaining, reset_time = parse_rate_limit_headers(response)
    assert remaining == 0
    assert isinstance(reset_time, datetime)

@pytest.mark.parametrize("status_code,error_class,error_data,expected_message", [
    (401, GitHubAuthenticationError, {"message": "Bad credentials"}, "Bad credentials"),
    (403, GitHubPermissionError, {"message": "Permission denied"}, "Permission denied"),
    (404, GitHubResourceNotFoundError, {"message": "Not found"}, "Not found"),
    (409, GitHubConflictError, {"message": "Conflict"}, "Conflict"),
    (422, GitHubValidationError, {"message": "Validation failed"}, "Validation failed"),
    (500, GitHubError, {"message": "Server error"}, r"API error \(500\): Server error"),
])
def test_process_error_response(status_code, error_class, error_data, expected_message):
    """Test error response processing for different status codes."""
    response = Mock(spec=Response)
    response.status_code = status_code
    response.json.return_value = error_data
    response.headers = {}  # Add empty headers for rate limit checks
    
    with pytest.raises(error_class, match=expected_message):
        process_error_response(response)

def test_process_error_response_rate_limit():
    """Test rate limit error processing."""
    response = Mock(spec=Response)
    response.status_code = 403
    response.json.return_value = {"message": "API rate limit exceeded"}
    response.headers = {
        "X-RateLimit-Remaining": "0",
        "X-RateLimit-Reset": str(int(datetime.now().timestamp()))
    }
    
    with pytest.raises(GitHubRateLimitError):
        process_error_response(response)

def test_process_response_success():
    """Test successful response processing."""
    response = Mock(spec=Response)
    response.ok = True
    response.status_code = 200
    expected_data = {"key": "value"}
    response.json.return_value = expected_data
    
    assert process_response(response) == expected_data

def test_process_response_no_content():
    """Test processing response with no content."""
    response = Mock(spec=Response)
    response.ok = True
    response.status_code = 204
    
    assert process_response(response) is None

def test_process_response_invalid_json():
    """Test processing response with invalid JSON."""
    response = Mock(spec=Response)
    response.ok = True
    response.status_code = 200
    response.json.side_effect = ValueError("Invalid JSON")
    
    with pytest.raises(GitHubError, match="Invalid JSON response"):
        process_response(response)

# Tool Response Formatting Tests

@pytest.mark.parametrize("input_data,expected_text", [
    ("test message", "test message"),
    ({"key": "value"}, "{'key': 'value'}"),
    (123, "123"),
    (None, "None"),
])
def test_create_tool_response(input_data, expected_text):
    """Test tool response creation with different input types."""
    response = create_tool_response(input_data)
    assert response["content"][0]["type"] == "text"
    assert response["content"][0]["text"] == expected_text
    assert not response["is_error"]

def test_create_tool_response_error():
    """Test tool response creation for errors."""
    response = create_tool_response("error message", is_error=True)
    assert response["content"][0]["type"] == "text"
    assert response["content"][0]["text"] == "error message"
    assert response["is_error"]

# Parameter Formatting Tests

@pytest.mark.parametrize("params,expected", [
    (
        {"state": "open", "labels": ["bug", "help wanted"], "draft": True},
        {"state": "open", "labels": "bug,help wanted", "draft": "true"}
    ),
    (
        {"milestone": None, "assignee": "username"},
        {"assignee": "username"}
    ),
    (
        {"created": datetime(2025, 1, 1, 12, 0)},
        {"created": "2025-01-01T12:00:00"}
    ),
])
def test_format_query_params(params, expected):
    """Test query parameter formatting with different input types."""
    assert format_query_params(**params) == expected
