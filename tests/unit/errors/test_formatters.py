"""Unit tests for error formatting utilities.

This module tests the error formatting functions in the errors/formatters.py module.
"""

import pytest
from datetime import datetime

from pygithub_mcp_server.errors.formatters import (
    format_github_error,
    is_github_error,
)
from pygithub_mcp_server.errors.exceptions import (
    GitHubError,
    GitHubValidationError,
    GitHubResourceNotFoundError,
    GitHubAuthenticationError,
    GitHubPermissionError,
    GitHubRateLimitError,
    GitHubConflictError,
)


class TestFormatGitHubError:
    """Tests for format_github_error function."""
    
    def test_base_github_error(self):
        """Test formatting of base GitHubError."""
        error = GitHubError("Test error message")
        formatted = format_github_error(error)
        
        assert "GitHub API Error" in formatted
        assert "Test error message" in formatted
    
    def test_validation_error(self):
        """Test formatting of GitHubValidationError."""
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
    
    def test_resource_not_found_error(self):
        """Test formatting of GitHubResourceNotFoundError."""
        error = GitHubResourceNotFoundError("Repository not found")
        formatted = format_github_error(error)
        
        assert "Not Found" in formatted
        assert "Repository not found" in formatted
    
    def test_authentication_error(self):
        """Test formatting of GitHubAuthenticationError."""
        error = GitHubAuthenticationError("Invalid token")
        formatted = format_github_error(error)
        
        assert "Authentication Failed" in formatted
        assert "Invalid token" in formatted
    
    def test_permission_error(self):
        """Test formatting of GitHubPermissionError."""
        error = GitHubPermissionError("No access to repository")
        formatted = format_github_error(error)
        
        assert "Permission Denied" in formatted
        assert "No access to repository" in formatted
    
    def test_rate_limit_error_with_reset_time(self):
        """Test formatting of GitHubRateLimitError with reset time."""
        reset_time = datetime.fromisoformat("2025-03-01T10:00:00+00:00")
        error = GitHubRateLimitError("Rate limit exceeded", reset_time)
        formatted = format_github_error(error)
        
        assert "Rate Limit Exceeded" in formatted
        assert "Rate limit exceeded" in formatted
        assert reset_time.isoformat() in formatted
    
    def test_rate_limit_error_without_reset_time(self):
        """Test formatting of GitHubRateLimitError without reset time."""
        error = GitHubRateLimitError("Rate limit exceeded", None)
        formatted = format_github_error(error)
        
        assert "Rate Limit Exceeded" in formatted
        assert "Rate limit exceeded" in formatted
        assert "unknown" in formatted
    
    def test_conflict_error(self):
        """Test formatting of GitHubConflictError."""
        error = GitHubConflictError("Resource already exists")
        formatted = format_github_error(error)
        
        assert "Conflict" in formatted
        assert "Resource already exists" in formatted


class TestIsGitHubError:
    """Tests for is_github_error function."""
    
    def test_with_github_errors(self):
        """Test with various GitHub error types."""
        assert is_github_error(GitHubError("test"))
        assert is_github_error(GitHubValidationError("test"))
        assert is_github_error(GitHubResourceNotFoundError("test"))
        assert is_github_error(GitHubAuthenticationError("test"))
        assert is_github_error(GitHubPermissionError("test"))
        assert is_github_error(GitHubRateLimitError("test", None))
        assert is_github_error(GitHubConflictError("test"))
    
    def test_with_non_github_errors(self):
        """Test with non-GitHub error types."""
        assert not is_github_error(ValueError("test"))
        assert not is_github_error(Exception("test"))
        assert not is_github_error(RuntimeError("test"))
        assert not is_github_error(KeyError("test"))
    
    def test_with_non_errors(self):
        """Test with non-error values."""
        assert not is_github_error(None)
        assert not is_github_error("string error")
        assert not is_github_error(123)
        assert not is_github_error({"error": "message"})
