"""Tests for the PyGithub MCP Server implementation."""

import json
import pytest
from pygithub_mcp_server.common.errors import GitHubError
from pygithub_mcp_server.common.version import VERSION


class TestServerInitialization:
    """Test FastMCP server initialization and configuration."""
    
    def test_server_creation(self, mock_fastmcp):
        """Test FastMCP server is created with correct parameters."""
        # Verify FastMCP was created with correct name and version
        mock_fastmcp.assert_called_once_with(
            "pygithub-mcp-server",
            version=VERSION,
            description="GitHub API operations via MCP"
        )

    def test_tool_registration(self, mock_fastmcp):
        """Test all tools are registered."""
        # Get all tool decorators that were called
        tool_calls = [
            name for name, args, kwargs in mock_fastmcp.tool.mock_calls
            if name == "()"
        ]
        
        # We should have one call for each tool
        expected_tools = [
            "create_issue",
            "list_issues",
            "get_issue",
            "update_issue",
            "add_issue_comment",
            "list_issue_comments",
            "update_issue_comment",
            "delete_issue_comment",
            "add_issue_labels",
            "remove_issue_label"
        ]
        
        assert len(tool_calls) == len(expected_tools), \
            f"Expected {len(expected_tools)} tools to be registered, got {len(tool_calls)}"


class TestToolResponses:
    """Test tool response formatting and error handling."""
    
    def test_successful_response_format(self, mock_tool_response):
        """Test successful response formatting."""
        test_data = {"key": "value"}
        response = mock_tool_response(test_data)
        
        assert not response.get("is_error")
        assert len(response["content"]) == 1
        assert response["content"][0]["type"] == "text"
        assert json.loads(response["content"][0]["text"]) == test_data

    def test_error_response_format(self, mock_tool_response):
        """Test error response formatting."""
        test_error = "Test error message"
        response = mock_tool_response(test_error, is_error=True)
        
        assert response["is_error"]
        assert len(response["content"]) == 1
        assert response["content"][0]["type"] == "text"
        assert json.loads(response["content"][0]["text"]) == test_error


class TestCreateIssueTool:
    """Test the create_issue tool implementation."""
    
    def test_create_issue_success(self, mock_fastmcp, mock_issue, mock_tool_response):
        """Test successful issue creation."""
        from pygithub_mcp_server.server import create_issue
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "title": "Test Issue",
            "body": "Test body",
            "assignees": ["testuser"],
            "labels": ["bug"],
            "milestone": 1
        }
        
        # Call the tool function
        result = create_issue(params)
        
        # Verify response format
        assert not result.get("is_error")
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"
        
        # Verify response content
        response_data = json.loads(result["content"][0]["text"])
        assert response_data["number"] == mock_issue.number
        assert response_data["title"] == mock_issue.title

    def test_create_issue_github_error(self, mock_fastmcp, mock_github_exception):
        """Test GitHub error handling in create_issue."""
        from pygithub_mcp_server.server import create_issue
        
        # Create test error
        test_error = mock_github_exception(
            404,
            {"message": "Repository not found"}
        )
        
        # Configure mock to raise error
        mock_fastmcp.create_issue.side_effect = GitHubError(str(test_error))
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "title": "Test Issue"
        }
        
        # Call the tool function
        result = create_issue(params)
        
        # Verify error response
        assert result["is_error"]
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "error"
        assert "Repository not found" in result["content"][0]["text"]


class TestListIssuesTool:
    """Test the list_issues tool implementation."""
    
    def test_list_issues_success(self, mock_fastmcp, mock_issue, mock_tool_response):
        """Test successful issues listing."""
        from pygithub_mcp_server.server import list_issues
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "state": "open",
            "labels": ["bug"],
            "sort": "created",
            "direction": "desc",
            "page": 1,
            "per_page": 30
        }
        
        # Call the tool function
        result = list_issues(params)
        
        # Verify response format
        assert not result.get("is_error")
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"
        
        # Verify response content
        response_data = json.loads(result["content"][0]["text"])
        assert isinstance(response_data, list)

    def test_list_issues_github_error(self, mock_fastmcp, mock_github_exception):
        """Test GitHub error handling in list_issues."""
        from pygithub_mcp_server.server import list_issues
        
        # Create test error
        test_error = mock_github_exception(
            403,
            {"message": "Rate limit exceeded"}
        )
        
        # Configure mock to raise error
        mock_fastmcp.list_issues.side_effect = GitHubError(str(test_error))
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo"
        }
        
        # Call the tool function
        result = list_issues(params)
        
        # Verify error response
        assert result["is_error"]
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "error"
        assert "Rate limit exceeded" in result["content"][0]["text"]

    def test_list_issues_unexpected_error(self, mock_fastmcp):
        """Test unexpected error handling in list_issues."""
        from pygithub_mcp_server.server import list_issues
        
        # Configure mock to raise unexpected error
        mock_fastmcp.list_issues.side_effect = Exception("Unexpected error")
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo"
        }
        
        # Call the tool function
        result = list_issues(params)
        
        # Verify error response
        assert result["is_error"]
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "error"
        assert "Internal server error" in result["content"][0]["text"]
        assert "Unexpected error" in result["content"][0]["text"]


class TestGetIssueTool:
    """Test the get_issue tool implementation."""
    
    def test_get_issue_success(self, mock_fastmcp, mock_issue, mock_tool_response):
        """Test successful issue retrieval."""
        from pygithub_mcp_server.server import get_issue
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "issue_number": 42
        }
        
        # Call the tool function
        result = get_issue(params)
        
        # Verify response format
        assert not result.get("is_error")
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"
        
        # Verify response content
        response_data = json.loads(result["content"][0]["text"])
        assert response_data["number"] == mock_issue.number
        assert response_data["title"] == mock_issue.title
        assert response_data["state"] == mock_issue.state

    def test_get_issue_not_found(self, mock_fastmcp, mock_github_exception):
        """Test error handling when issue doesn't exist."""
        from pygithub_mcp_server.server import get_issue
        
        # Create test error
        test_error = mock_github_exception(
            404,
            {"message": "Issue not found"}
        )
        
        # Configure mock to raise error
        mock_fastmcp.get_issue.side_effect = GitHubError(str(test_error))
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "issue_number": 999
        }
        
        # Call the tool function
        result = get_issue(params)
        
        # Verify error response
        assert result["is_error"]
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "error"
        assert "Issue not found" in result["content"][0]["text"]


class TestUpdateIssueTool:
    """Test the update_issue tool implementation."""
    
    def test_update_issue_success(self, mock_fastmcp, mock_issue, mock_tool_response):
        """Test successful issue update."""
        from pygithub_mcp_server.server import update_issue
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "issue_number": 42,
            "title": "Updated Title",
            "body": "Updated body",
            "state": "closed",
            "labels": ["bug", "priority"],
            "assignees": ["testuser"],
            "milestone": 2
        }
        
        # Call the tool function
        result = update_issue(params)
        
        # Verify response format
        assert not result.get("is_error")
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"
        
        # Verify response content
        response_data = json.loads(result["content"][0]["text"])
        assert response_data["number"] == mock_issue.number
        assert response_data["state"] == mock_issue.state

    def test_update_issue_permission_error(self, mock_fastmcp, mock_github_exception):
        """Test error handling when user lacks permission."""
        from pygithub_mcp_server.server import update_issue
        
        # Create test error
        test_error = mock_github_exception(
            403,
            {"message": "Resource not accessible by integration"}
        )
        
        # Configure mock to raise error
        mock_fastmcp.update_issue.side_effect = GitHubError(str(test_error))
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "issue_number": 42,
            "state": "closed"
        }
        
        # Call the tool function
        result = update_issue(params)
        
        # Verify error response
        assert result["is_error"]
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "error"
        assert "Resource not accessible" in result["content"][0]["text"]

    def test_update_issue_no_changes(self, mock_fastmcp, mock_issue, mock_tool_response):
        """Test update with no actual changes."""
        from pygithub_mcp_server.server import update_issue
        
        # Test parameters with current values
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "issue_number": 42,
            "state": mock_issue.state,  # Same as current state
            "title": mock_issue.title   # Same as current title
        }
        
        # Call the tool function
        result = update_issue(params)
        
        # Verify response format
        assert not result.get("is_error")
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"
        
        # Verify response content shows no changes
        response_data = json.loads(result["content"][0]["text"])
        assert response_data["number"] == mock_issue.number
        assert response_data["state"] == mock_issue.state
        assert response_data["title"] == mock_issue.title


class TestIssueCommentTools:
    """Test the issue comment related tools."""
    
    def test_add_comment_success(self, mock_fastmcp, mock_comment, mock_tool_response):
        """Test successful comment creation."""
        from pygithub_mcp_server.server import add_issue_comment
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "issue_number": 42,
            "body": "Test comment body"
        }
        
        # Call the tool function
        result = add_issue_comment(params)
        
        # Verify response format
        assert not result.get("is_error")
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"
        
        # Verify response content
        response_data = json.loads(result["content"][0]["text"])
        assert response_data["id"] == mock_comment.id
        assert response_data["body"] == mock_comment.body

    def test_list_comments_success(self, mock_fastmcp, mock_comment, mock_tool_response):
        """Test successful comments listing."""
        from pygithub_mcp_server.server import list_issue_comments
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "issue_number": 42,
            "since": "2025-01-01T00:00:00Z",
            "page": 1,
            "per_page": 30
        }
        
        # Call the tool function
        result = list_issue_comments(params)
        
        # Verify response format
        assert not result.get("is_error")
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"
        
        # Verify response content
        response_data = json.loads(result["content"][0]["text"])
        assert isinstance(response_data, list)

    def test_update_comment_success(self, mock_fastmcp, mock_comment, mock_tool_response):
        """Test successful comment update."""
        from pygithub_mcp_server.server import update_issue_comment
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "issue_number": 42,
            "comment_id": 22222,
            "body": "Updated comment body"
        }
        
        # Call the tool function
        result = update_issue_comment(params)
        
        # Verify response format
        assert not result.get("is_error")
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"
        
        # Verify response content
        response_data = json.loads(result["content"][0]["text"])
        assert response_data["id"] == mock_comment.id
        assert response_data["body"] == mock_comment.body

    def test_delete_comment_success(self, mock_fastmcp, mock_tool_response):
        """Test successful comment deletion."""
        from pygithub_mcp_server.server import delete_issue_comment
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "issue_number": 42,
            "comment_id": 22222
        }
        
        # Call the tool function
        result = delete_issue_comment(params)
        
        # Verify response format
        assert not result.get("is_error")
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"
        assert "Comment deleted successfully" in result["content"][0]["text"]

    def test_comment_not_found_error(self, mock_fastmcp, mock_github_exception):
        """Test error handling when comment doesn't exist."""
        from pygithub_mcp_server.server import update_issue_comment
        
        # Create test error
        test_error = mock_github_exception(
            404,
            {"message": "Comment not found"}
        )
        
        # Configure mock to raise error
        mock_fastmcp.update_issue_comment.side_effect = GitHubError(str(test_error))
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "issue_number": 42,
            "comment_id": 99999,
            "body": "Updated body"
        }
        
        # Call the tool function
        result = update_issue_comment(params)
        
        # Verify error response
        assert result["is_error"]
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "error"
        assert "Comment not found" in result["content"][0]["text"]

    def test_comment_rate_limit_error(self, mock_fastmcp, mock_github_exception):
        """Test rate limit error handling for comments."""
        from pygithub_mcp_server.server import add_issue_comment
        
        # Create test error with rate limit headers
        test_error = mock_github_exception(
            403,
            {"message": "API rate limit exceeded"},
            {
                "X-RateLimit-Limit": "5000",
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": "1614556800"
            }
        )
        
        # Configure mock to raise error
        mock_fastmcp.add_issue_comment.side_effect = GitHubError(str(test_error))
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "issue_number": 42,
            "body": "Test comment"
        }
        
        # Call the tool function
        result = add_issue_comment(params)
        
        # Verify error response
        assert result["is_error"]
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "error"
        assert "API rate limit exceeded" in result["content"][0]["text"]
        assert "X-RateLimit-Reset" in str(test_error)


class TestIssueLabelTools:
    """Test the issue label related tools."""
    
    def test_add_labels_success(self, mock_fastmcp, mock_issue, mock_label, mock_tool_response):
        """Test successful label addition."""
        from pygithub_mcp_server.server import add_issue_labels
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "issue_number": 42,
            "labels": ["bug", "priority"]
        }
        
        # Call the tool function
        result = add_issue_labels(params)
        
        # Verify response format
        assert not result.get("is_error")
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"
        
        # Verify response content
        response_data = json.loads(result["content"][0]["text"])
        assert isinstance(response_data, list)
        assert any(label["name"] == mock_label.name for label in response_data)

    def test_remove_label_success(self, mock_fastmcp, mock_tool_response):
        """Test successful label removal."""
        from pygithub_mcp_server.server import remove_issue_label
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "issue_number": 42,
            "label": "bug"
        }
        
        # Call the tool function
        result = remove_issue_label(params)
        
        # Verify response format
        assert not result.get("is_error")
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"
        assert "Label removed successfully" in result["content"][0]["text"]

    def test_add_labels_invalid_label(self, mock_fastmcp, mock_github_exception):
        """Test error handling when adding invalid labels."""
        from pygithub_mcp_server.server import add_issue_labels
        
        # Create test error
        test_error = mock_github_exception(
            422,
            {"message": "Invalid label name"}
        )
        
        # Configure mock to raise error
        mock_fastmcp.add_issue_labels.side_effect = GitHubError(str(test_error))
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "issue_number": 42,
            "labels": ["nonexistent-label"]
        }
        
        # Call the tool function
        result = add_issue_labels(params)
        
        # Verify error response
        assert result["is_error"]
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "error"
        assert "Invalid label name" in result["content"][0]["text"]

    def test_remove_nonexistent_label(self, mock_fastmcp, mock_github_exception):
        """Test error handling when removing a nonexistent label."""
        from pygithub_mcp_server.server import remove_issue_label
        
        # Create test error
        test_error = mock_github_exception(
            404,
            {"message": "Label does not exist on this issue"}
        )
        
        # Configure mock to raise error
        mock_fastmcp.remove_issue_label.side_effect = GitHubError(str(test_error))
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "issue_number": 42,
            "label": "nonexistent"
        }
        
        # Call the tool function
        result = remove_issue_label(params)
        
        # Verify error response
        assert result["is_error"]
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "error"
        assert "Label does not exist" in result["content"][0]["text"]

    def test_label_operations_permission_error(self, mock_fastmcp, mock_github_exception):
        """Test permission error handling for label operations."""
        from pygithub_mcp_server.server import add_issue_labels
        
        # Create test error
        test_error = mock_github_exception(
            403,
            {"message": "Must have write access to repository"}
        )
        
        # Configure mock to raise error
        mock_fastmcp.add_issue_labels.side_effect = GitHubError(str(test_error))
        
        # Test parameters
        params = {
            "owner": "test-owner",
            "repo": "test-repo",
            "issue_number": 42,
            "labels": ["bug"]
        }
        
        # Call the tool function
        result = add_issue_labels(params)
        
        # Verify error response
        assert result["is_error"]
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "error"
        assert "Must have write access" in result["content"][0]["text"]
