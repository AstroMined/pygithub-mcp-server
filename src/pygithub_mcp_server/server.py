"""PyGithub MCP Server implementation.

This module provides a FastMCP server that exposes GitHub API operations.
"""

import json
import logging
import os
import sys
import traceback
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from pygithub_mcp_server.common.types import ListIssuesParams
from pygithub_mcp_server.common.version import VERSION
from pygithub_mcp_server.common.errors import GitHubError, format_github_error
from pygithub_mcp_server.operations import issues

# Set up logging
log_dir = Path(__file__).parent.parent.parent / 'logs'
if not log_dir.exists():
    os.makedirs(log_dir)

log_file = log_dir / 'pygithub_mcp_server.log'
logger = logging.getLogger()  # Get root logger
logger.setLevel(logging.DEBUG)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stderr)
    ],
    force=True
)
logger = logging.getLogger(__name__)
logger.debug("Logging initialized")

# Create FastMCP server instance
mcp = FastMCP(
    "pygithub-mcp-server",
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
    try:
        logger.debug(f"list_issues called with params: {params}")
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
        logger.debug(f"Got result: {result}")
        response = {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
        logger.debug(f"Returning response: {response}")
        return response
    except GitHubError as e:
        logger.error(f"GitHub error: {e}")
        return {
            "content": [{"type": "error", "text": format_github_error(e)}],
            "is_error": True
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(traceback.format_exc())
        error_msg = str(e) if str(e) else "An unexpected error occurred"
        return {
            "content": [{"type": "error", "text": f"Internal server error: {error_msg}"}],
            "is_error": True
        }

if __name__ == "__main__":
    mcp.run()
