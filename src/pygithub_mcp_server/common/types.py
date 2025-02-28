"""Type definitions and schema models for GitHub MCP Server.

DEPRECATED: This module is deprecated. Import schemas from pygithub_mcp_server.schemas instead.

This module re-exports all schema models from their domain-specific modules
for backward compatibility.
"""

import warnings

# Show deprecation warning
warnings.warn(
    "The pygithub_mcp_server.common.types module is deprecated. "
    "Import schemas from pygithub_mcp_server.schemas instead.",
    DeprecationWarning,
    stacklevel=2
)

# Re-export all schemas from the new location
from pygithub_mcp_server.schemas import (
    # Base
    RepositoryRef,
    FileContent,
    
    # Repositories
    CreateOrUpdateFileParams,
    PushFilesParams,
    SearchRepositoriesParams,
    CreateRepositoryParams,
    GetFileContentsParams,
    ForkRepositoryParams,
    CreateBranchParams,
    ListCommitsParams,
    
    # Issues
    CreateIssueParams,
    UpdateIssueParams,
    GetIssueParams,
    ListIssuesParams,
    IssueCommentParams,
    ListIssueCommentsParams,
    UpdateIssueCommentParams,
    DeleteIssueCommentParams,
    AddIssueLabelsParams,
    RemoveIssueLabelParams,
    
    # Pull Requests
    CreatePullRequestParams,
    
    # Search
    SearchParams,
    SearchCodeParams,
    SearchIssuesParams,
    SearchUsersParams,
    
    # Responses
    ToolResponse,
    TextContent,
    ErrorContent,
    ResponseContent,
)

__all__ = [
    # Base
    "RepositoryRef",
    "FileContent",
    
    # Repositories
    "CreateOrUpdateFileParams",
    "PushFilesParams",
    "SearchRepositoriesParams",
    "CreateRepositoryParams",
    "GetFileContentsParams",
    "ForkRepositoryParams",
    "CreateBranchParams",
    "ListCommitsParams",
    
    # Issues
    "CreateIssueParams",
    "UpdateIssueParams",
    "GetIssueParams",
    "ListIssuesParams",
    "IssueCommentParams",
    "ListIssueCommentsParams",
    "UpdateIssueCommentParams",
    "DeleteIssueCommentParams",
    "AddIssueLabelsParams",
    "RemoveIssueLabelParams",
    
    # Pull Requests
    "CreatePullRequestParams",
    
    # Search
    "SearchParams",
    "SearchCodeParams",
    "SearchIssuesParams",
    "SearchUsersParams",
    
    # Responses
    "ToolResponse",
    "TextContent",
    "ErrorContent",
    "ResponseContent",
]
