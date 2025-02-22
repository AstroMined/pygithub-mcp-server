"""Tests for GitHub error handling.

This module tests the error handling functionality in the common/errors.py module,
including error formatting and specific error types.
"""

import pytest
from datetime import datetime
from pygithub_mcp_server.common.errors import (
    GitHubError,
    GitHubValidationError,
    GitHubResourceNotFoundError,
    GitHubAuthenticationError,
    GitHubPermissionError,
    GitHubRateLimitError,
    GitHubConflictError,
    format_github_error,
    is_github_error,
)


def test_base_github_error():
    """Test base GitHubError class."""
    error = GitHubError("test message")
    assert str(error) == "test message"
    assert error.response is None

    # Test with response data
    response_data = {"message": "API error"}
    error_with_data = GitHubError("test message", response_data)
    assert error_with_data.response == response_data


def test_validation_error():
    """Test GitHubValidationError formatting."""
    response_data = {
        "message": "Validation Failed",
        "errors": [
            {
                "resource": "Issue",
                "field": "title",
                "code": "missing_field"
            }
        ]
    }
    error = GitHubValidationError("Invalid title", response_data)
    formatted = format_github_error(error)
    assert "Validation Error" in formatted
    assert "Invalid title" in formatted
    assert str(response_data) in formatted


def test_resource_not_found_error():
    """Test GitHubResourceNotFoundError formatting."""
    error = GitHubResourceNotFoundError("Issue not found")
    formatted = format_github_error(error)
    assert "Not Found" in formatted
    assert "Issue not found" in formatted


def test_authentication_error():
    """Test GitHubAuthenticationError formatting."""
    error = GitHubAuthenticationError("Invalid token")
    formatted = format_github_error(error)
    assert "Authentication Failed" in formatted
    assert "Invalid token" in formatted


def test_permission_error():
    """Test GitHubPermissionError formatting."""
    error = GitHubPermissionError("No access")
    formatted = format_github_error(error)
    assert "Permission Denied" in formatted
    assert "No access" in formatted


def test_rate_limit_error():
    """Test GitHubRateLimitError formatting."""
    reset_time = datetime.fromisoformat("2025-02-22T21:00:00+00:00")
    error = GitHubRateLimitError("Rate limit exceeded", reset_time)
    formatted = format_github_error(error)
    assert "Rate Limit Exceeded" in formatted
    assert "Rate limit exceeded" in formatted
    assert reset_time.isoformat() in formatted


def test_conflict_error():
    """Test GitHubConflictError formatting."""
    error = GitHubConflictError("Resource conflict")
    formatted = format_github_error(error)
    assert "Conflict" in formatted
    assert "Resource conflict" in formatted


def test_is_github_error():
    """Test is_github_error function."""
    # Test with GitHub errors
    assert is_github_error(GitHubError("test"))
    assert is_github_error(GitHubValidationError("test"))
    assert is_github_error(GitHubResourceNotFoundError("test"))
    
    # Test with non-GitHub errors
    assert not is_github_error(ValueError("test"))
    assert not is_github_error(Exception("test"))
    assert not is_github_error(None)


def test_error_with_complex_response():
    """Test error handling with complex response data."""
    response_data = {
        "message": "Validation Failed",
        "errors": [
            {
                "resource": "Issue",
                "field": "title",
                "code": "missing_field"
            },
            {
                "resource": "Issue",
                "field": "labels",
                "code": "invalid",
                "message": "Label does not exist"
            }
        ],
        "documentation_url": "https://docs.github.com/rest"
    }
    error = GitHubValidationError("Multiple validation errors", response_data)
    formatted = format_github_error(error)
    
    # Check all components are present
    assert "Validation Error" in formatted
    assert "Multiple validation errors" in formatted
    assert str(response_data) in formatted


def test_rate_limit_error_without_reset():
    """Test rate limit error without reset time."""
    error = GitHubRateLimitError("Rate limit exceeded", None)
    formatted = format_github_error(error)
    assert "Rate Limit Exceeded" in formatted
    assert "Rate limit exceeded" in formatted
    assert "Resets at: None" in formatted


def test_error_inheritance():
    """Test error class inheritance."""
    # All custom errors should inherit from GitHubError
    assert issubclass(GitHubValidationError, GitHubError)
    assert issubclass(GitHubResourceNotFoundError, GitHubError)
    assert issubclass(GitHubAuthenticationError, GitHubError)
    assert issubclass(GitHubPermissionError, GitHubError)
    assert issubclass(GitHubRateLimitError, GitHubError)
    assert issubclass(GitHubConflictError, GitHubError)
