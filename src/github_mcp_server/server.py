"""GitHub MCP Server implementation.

This module provides a FastMCP server that exposes GitHub API operations.
"""

import json
from mcp.server.fastmcp import FastMCP
from github_mcp_server.common.types import ListIssuesParams
from github_mcp_server.common.version import VERSION
from github_mcp_server.operations import issues

# Create FastMCP server instance
mcp = FastMCP(
    "github-mcp-server",
    version=VERSION,
    description="GitHub API operations via MCP"
)

@mcp.tool()
def list_issues(params: ListIssuesParams) -> dict:
    """List issues from a GitHub repository.
    
    Args:
        params: Parameters for listing issues including:
            - owner: Repository owner (user or organization)
            - repo: Repository name
            - state: Issue state (open, closed, all)
            - labels: Filter by labels
            - sort: Sort field (created, updated, comments)
            - direction: Sort direction (asc, desc)
            - since: Filter by date
            - page: Page number for pagination
            - per_page: Number of results per page (max 100)
    
    Returns:
        List of issues from GitHub API
    """
    result = issues.list_issues(
        params.owner,
        params.repo,
        state=params.state,
        labels=params.labels,
        sort=params.sort,
        direction=params.direction,
        since=params.since,
        page=params.page,
        per_page=params.per_page
    )
    return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}

if __name__ == "__main__":
    mcp.run()
