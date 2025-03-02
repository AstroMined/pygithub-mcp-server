"""Tests for error handling utilities.

This module tests the error handling utilities used to map PyGithub exceptions
to our custom exceptions and format error messages.
"""

import pytest
from datetime import datetime
import json

from github import GithubException, RateLimitExceededException
from github.Rate import Rate
from github.RateLimit import RateLimit

from pygithub_mcp_server.errors.handlers import (
    handle_github_exception,
    format_validation_error
)
from pygithub_mcp_server.errors.exceptions import (
    GitHubAuthenticationError,
    GitHubError,
    GitHubPermissionError,
    GitHubRateLimitError,
    GitHubResourceNotFoundError,
    GitHubValidationError,
)


class TestHandleGithubException:
    """Tests for handle_github_exception function."""
    
    def test_handle_rate_limit_exceeded(self):
        """Test handling RateLimitExceededException with rate attribute."""
        # Create a rate limit exception with real structure
        reset_time = int(datetime(2023, 6, 1, 12, 0, 0).timestamp())
        
        # Create the exception with headers
        exception = RateLimitExceededException(
            403, 
            {"message": "API rate limit exceeded"},
            {"X-RateLimit-Reset": str(reset_time)}
        )
        
        # Create mock rate object and attach to exception
        class TestRate:
            def __init__(self):
                self.limit = 5000
                self.remaining = 0
                self.reset = datetime(2023, 6, 1, 12, 0, 0)
        
        exception.rate = TestRate()
        
        # Test the handler
        result = handle_github_exception(exception)
        
        assert isinstance(result, GitHubRateLimitError)
        assert "API rate limit exceeded" in str(result)
        assert "(0/5000 calls remaining)" in str(result)
        assert "2023-06-01" in str(result)
        # Check against the datetime object now that handler converts timestamp to datetime
        assert isinstance(result.reset_at, datetime)
        assert result.reset_at == datetime.fromtimestamp(int(reset_time))
    
    def test_handle_rate_limit_exceeded_without_rate(self):
        """Test handling RateLimitExceededException without rate attribute."""
        # Create a rate limit exception without rate attribute
        exception = RateLimitExceededException(
            403, 
            {"message": "API rate limit exceeded"},
            {"X-RateLimit-Reset": "1622548800"}  # Jun 1, 2021
        )
        
        # Test the handler
        result = handle_github_exception(exception)
        
        assert isinstance(result, GitHubRateLimitError)
        assert "API rate limit exceeded" in str(result)
        assert "(0/None calls remaining)" in str(result)
    
    def test_handle_authentication_error(self):
        """Test handling 401 authentication error."""
        exception = GithubException(
            401, 
            {"message": "Bad credentials"},
            {"X-GitHub-Request-Id": "ABCD1234"}
        )
        
        result = handle_github_exception(exception)
        
        assert isinstance(result, GitHubAuthenticationError)
        assert "Authentication failed" in str(result)
        assert "verify your GitHub token" in str(result)
    
    def test_handle_permission_error(self):
        """Test handling 403 permission error."""
        exception = GithubException(
            403, 
            {"message": "Resource not accessible by integration"},
            {"X-GitHub-Request-Id": "ABCD1234"}
        )
        
        result = handle_github_exception(exception)
        
        assert isinstance(result, GitHubPermissionError)
        assert "Permission denied" in str(result)
        assert "Resource not accessible by integration" in str(result)
    
    def test_handle_403_rate_limit(self):
        """Test handling 403 error with rate limit message."""
        reset_time = "1717200000"  # Some future timestamp
        exception = GithubException(
            403, 
            {"message": "API rate limit exceeded"},
            {"X-RateLimit-Reset": reset_time}
        )
        
        result = handle_github_exception(exception)
        
        assert isinstance(result, GitHubRateLimitError)
        assert "API rate limit exceeded" in str(result)
        assert "Reset at" in str(result)
        # Check that reset_at is now converted to a datetime object
        assert isinstance(result.reset_at, datetime)
        assert result.reset_at == datetime.fromtimestamp(int(reset_time))
    
    def test_handle_not_found_with_hint(self):
        """Test handling 404 not found with resource hint."""
        exception = GithubException(
            404, 
            {"message": "Not Found"},
            {"X-GitHub-Request-Id": "ABCD1234"}
        )
        
        result = handle_github_exception(exception, resource_hint="repository")
        
        assert isinstance(result, GitHubResourceNotFoundError)
        assert "Repository not found" in str(result)
    
    def test_handle_not_found_auto_detection(self):
        """Test handling 404 with automatic resource detection from message."""
        exception = GithubException(
            404, 
            {"message": "Issue not found"},
            {"X-GitHub-Request-Id": "ABCD1234"}
        )
        
        result = handle_github_exception(exception)
        
        assert isinstance(result, GitHubResourceNotFoundError)
        assert "Issue not found" in str(result)
    
    def test_handle_not_found_with_resource_in_data(self):
        """Test handling 404 with resource in response data."""
        exception = GithubException(
            404, 
            {"message": "Not Found", "resource": "pull_request"},
            {"X-GitHub-Request-Id": "ABCD1234"}
        )
        
        result = handle_github_exception(exception)
        
        assert isinstance(result, GitHubResourceNotFoundError)
        assert "Pull Request not found" in str(result)  # Now properly formatted with spaces and correctly capitalized
    
    def test_handle_validation_error(self):
        """Test handling 422 validation error."""
        error_data = {
            "message": "Validation Failed",
            "errors": [
                {"resource": "Issue", "field": "title", "code": "missing_field"}
            ]
        }
        exception = GithubException(
            422, 
            error_data,
            {"X-GitHub-Request-Id": "ABCD1234"}
        )
        
        result = handle_github_exception(exception)
        
        assert isinstance(result, GitHubValidationError)
        assert "Validation Failed" in str(result)
    
    def test_handle_unknown_error(self):
        """Test handling unknown error status."""
        exception = GithubException(
            500, 
            {"message": "Internal server error"},
            {"X-GitHub-Request-Id": "ABCD1234"}
        )
        
        result = handle_github_exception(exception)
        
        assert isinstance(result, GitHubError)
        assert "GitHub API Error (500)" in str(result)
        assert "Internal server error" in str(result)
    
    def test_handle_string_data(self):
        """Test handling error with string data instead of dict."""
        exception = GithubException(
            400, 
            json.dumps({"message": "Bad request"}),
            {"X-GitHub-Request-Id": "ABCD1234"}
        )
        
        result = handle_github_exception(exception)
        
        assert isinstance(result, GitHubError)
        assert "Bad request" in str(result)
    
    def test_handle_plain_string_data(self):
        """Test handling error with plain string data."""
        exception = GithubException(
            400, 
            "Something went wrong",
            {"X-GitHub-Request-Id": "ABCD1234"}
        )
        
        result = handle_github_exception(exception)
        
        assert isinstance(result, GitHubError)
        assert "Something went wrong" in str(result)


class TestFormatValidationError:
    """Tests for format_validation_error function."""
    
    def test_format_validation_error_with_field_errors(self):
        """Test formatting validation error with field errors."""
        error_msg = "Validation Failed"
        data = {
            "message": "Validation Failed",
            "errors": [
                {"resource": "Issue", "field": "title", "code": "missing_field", "message": "is required"},
                {"resource": "Issue", "field": "body", "code": "invalid", "message": "is too long"}
            ]
        }
        
        result = format_validation_error(error_msg, data)
        
        assert "Validation failed:" in result
        assert "- title: is required (missing_field)" in result
        assert "- body: is too long (invalid)" in result
    
    def test_format_validation_error_without_field_errors(self):
        """Test formatting validation error without field errors."""
        error_msg = "Validation Failed"
        data = {
            "message": "Validation Failed",
            "errors": [
                {"resource": "Issue", "code": "invalid"}
            ]
        }
        
        result = format_validation_error(error_msg, data)
        
        assert result == error_msg
    
    def test_format_validation_error_without_errors(self):
        """Test formatting validation error without errors array."""
        error_msg = "Validation Failed"
        data = {"message": "Validation Failed"}
        
        result = format_validation_error(error_msg, data)
        
        assert result == error_msg
    
    def test_format_validation_error_with_none_data(self):
        """Test formatting validation error with None data."""
        error_msg = "Validation Failed"
        
        result = format_validation_error(error_msg, None)
        
        assert result == error_msg
