"""Schema models for GitHub MCP Server.

This module re-exports all schema models from their domain-specific modules
for backward compatibility.
"""

# Re-export all schemas for backward compatibility
from .base import RepositoryRef, FileContent
from .repositories import (
    CreateOrUpdateFileParams,
    PushFilesParams,
    SearchRepositoriesParams,
    CreateRepositoryParams,
    GetFileContentsParams,
    ForkRepositoryParams,
    CreateBranchParams,
)
from .issues import (
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
)
from .pull_requests import (
    CreatePullRequestParams,
)
from .search import (
    SearchParams,
    SearchCodeParams,
    SearchIssuesParams,
    SearchUsersParams,
)
from .responses import (
    ToolResponse,
    TextContent,
    ErrorContent,
    ResponseContent,
)

# For backward compatibility, also import ListCommitsParams
from .repositories import ListCommitsParams

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
