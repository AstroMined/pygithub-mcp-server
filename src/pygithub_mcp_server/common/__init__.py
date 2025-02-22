"""Common utilities and types for GitHub MCP Server.

This package provides shared functionality used across the GitHub MCP Server,
including error handling, type definitions, and utility functions.
"""

from .errors import (
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
from .types import (
    RepositoryRef,
    ListIssuesParams,
    CreateIssueParams,
    UpdateIssueParams,
    IssueCommentParams,
    ResponseContent,
    TextContent,
    ErrorContent,
    ToolResponse,
)
from .utils import (
    get_session,
    build_url,
    get_github_token,
    process_response,
    create_tool_response,
    format_query_params,
)
from .version import VERSION, get_version, get_version_tuple

__all__ = [
    # Errors
    "GitHubError",
    "GitHubValidationError",
    "GitHubResourceNotFoundError",
    "GitHubAuthenticationError",
    "GitHubPermissionError",
    "GitHubRateLimitError",
    "GitHubConflictError",
    "format_github_error",
    "is_github_error",
    # Types
    "RepositoryRef",
    "ListIssuesParams",
    "CreateIssueParams",
    "UpdateIssueParams",
    "IssueCommentParams",
    "ResponseContent",
    "TextContent",
    "ErrorContent",
    "ToolResponse",
    # Utils
    "get_session",
    "build_url",
    "get_github_token",
    "process_response",
    "create_tool_response",
    "format_query_params",
    # Version
    "VERSION",
    "get_version",
    "get_version_tuple",
]
