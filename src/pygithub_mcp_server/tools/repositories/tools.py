"""Repository tools.

This module implements MCP tools for GitHub repository operations.
"""

import json
import logging
import traceback
from typing import Dict

from pydantic import ValidationError

from pygithub_mcp_server.errors import GitHubError, format_github_error
from pygithub_mcp_server.operations import repositories
from pygithub_mcp_server.schemas.repositories import (
    CreateBranchParams,
    CreateOrUpdateFileParams,
    CreateRepositoryParams,
    ForkRepositoryParams,
    GetFileContentsParams,
    ListCommitsParams,
    PushFilesParams,
    SearchRepositoriesParams
)
from pygithub_mcp_server.schemas.base import RepositoryRef
from pygithub_mcp_server.tools import tool

# Set up logger
logger = logging.getLogger(__name__)


@tool()
def get_repository(params: Dict) -> Dict:
    """Get details about a GitHub repository.

    Args:
        params: Dictionary with repository parameters
            - owner: Repository owner (username or organization)
            - repo: Repository name

    Returns:
        MCP response with repository details
    """
    try:
        logger.debug(f"get_repository called with params: {params}")
        # Convert dict to Pydantic model
        repo_params = RepositoryRef(**params)
        
        # Call operation
        result = repositories.get_repository(repo_params.owner, repo_params.repo)
        
        logger.debug(f"Got result: {result}")
        return {
            "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
        }
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return {
            "content": [{"type": "error", "text": f"Validation error: {str(e)}"}],
            "is_error": True
        }
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


@tool()
def create_repository(params: Dict) -> Dict:
    """Create a new GitHub repository.

    Args:
        params: Dictionary with repository creation parameters
            - name: Repository name
            - description: Repository description (optional)
            - private: Whether the repository should be private (optional)
            - auto_init: Initialize repository with README (optional)

    Returns:
        MCP response with created repository details
    """
    try:
        logger.debug(f"create_repository called with params: {params}")
        # Convert dict to Pydantic model
        repo_params = CreateRepositoryParams(**params)
        
        # Call operation
        result = repositories.create_repository(repo_params)
        
        logger.debug(f"Got result: {result}")
        return {
            "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
        }
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return {
            "content": [{"type": "error", "text": f"Validation error: {str(e)}"}],
            "is_error": True
        }
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


@tool()
def fork_repository(params: Dict) -> Dict:
    """Fork an existing GitHub repository.

    Args:
        params: Dictionary with fork parameters
            - owner: Repository owner (username or organization)
            - repo: Repository name
            - organization: Organization to fork to (optional)

    Returns:
        MCP response with forked repository details
    """
    try:
        logger.debug(f"fork_repository called with params: {params}")
        # Convert dict to Pydantic model
        fork_params = ForkRepositoryParams(**params)
        
        # Call operation
        result = repositories.fork_repository(fork_params)
        
        logger.debug(f"Got result: {result}")
        return {
            "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
        }
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return {
            "content": [{"type": "error", "text": f"Validation error: {str(e)}"}],
            "is_error": True
        }
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


@tool()
def search_repositories(params: Dict) -> Dict:
    """Search for GitHub repositories.

    Args:
        params: Dictionary with search parameters
            - query: Search query
            - page: Page number for pagination (optional)
            - per_page: Results per page (optional)

    Returns:
        MCP response with matching repositories
    """
    try:
        logger.debug(f"search_repositories called with params: {params}")
        # Convert dict to Pydantic model
        search_params = SearchRepositoriesParams(**params)
        
        # Call operation
        result = repositories.search_repositories(search_params)
        
        logger.debug(f"Got {len(result)} results")
        return {
            "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
        }
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return {
            "content": [{"type": "error", "text": f"Validation error: {str(e)}"}],
            "is_error": True
        }
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


@tool()
def get_file_contents(params: Dict) -> Dict:
    """Get contents of a file in a GitHub repository.

    Args:
        params: Dictionary with file parameters
            - owner: Repository owner (username or organization)
            - repo: Repository name
            - path: Path to file/directory
            - branch: Branch to get contents from (optional)

    Returns:
        MCP response with file content data
    """
    try:
        logger.debug(f"get_file_contents called with params: {params}")
        # Convert dict to Pydantic model
        content_params = GetFileContentsParams(**params)
        
        # Call operation
        result = repositories.get_file_contents(content_params)
        
        logger.debug(f"Got result for path: {content_params.path}")
        return {
            "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
        }
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return {
            "content": [{"type": "error", "text": f"Validation error: {str(e)}"}],
            "is_error": True
        }
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


@tool()
def create_or_update_file(params: Dict) -> Dict:
    """Create or update a file in a GitHub repository.

    Args:
        params: Dictionary with file parameters
            - owner: Repository owner (username or organization)
            - repo: Repository name
            - path: Path where to create/update the file
            - content: Content of the file
            - message: Commit message
            - branch: Branch to create/update the file in
            - sha: SHA of file being replaced (for updates, optional)

    Returns:
        MCP response with file creation/update result
    """
    try:
        logger.debug(f"create_or_update_file called with params: {params}")
        # Convert dict to Pydantic model
        file_params = CreateOrUpdateFileParams(**params)
        
        # Call operation
        result = repositories.create_or_update_file(file_params)
        
        logger.debug(f"File created/updated: {file_params.path}")
        return {
            "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
        }
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return {
            "content": [{"type": "error", "text": f"Validation error: {str(e)}"}],
            "is_error": True
        }
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


@tool()
def push_files(params: Dict) -> Dict:
    """Push multiple files to a GitHub repository in a single commit.

    Args:
        params: Dictionary with file parameters
            - owner: Repository owner (username or organization)
            - repo: Repository name
            - branch: Branch to push to
            - files: List of files to push, each with path and content
            - message: Commit message

    Returns:
        MCP response with file push result
    """
    try:
        logger.debug(f"push_files called with params: {params}")
        # Convert dict to Pydantic model
        push_params = PushFilesParams(**params)
        
        # Call operation
        result = repositories.push_files(push_params)
        
        logger.debug(f"Pushed {len(push_params.files)} files")
        return {
            "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
        }
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return {
            "content": [{"type": "error", "text": f"Validation error: {str(e)}"}],
            "is_error": True
        }
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


@tool()
def create_branch(params: Dict) -> Dict:
    """Create a new branch in a GitHub repository.

    Args:
        params: Dictionary with branch parameters
            - owner: Repository owner (username or organization)
            - repo: Repository name
            - branch: Name for new branch
            - from_branch: Source branch (optional, defaults to repo default)

    Returns:
        MCP response with branch creation result
    """
    try:
        logger.debug(f"create_branch called with params: {params}")
        # Convert dict to Pydantic model
        branch_params = CreateBranchParams(**params)
        
        # Call operation
        result = repositories.create_branch(branch_params)
        
        logger.debug(f"Branch created: {branch_params.branch}")
        return {
            "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
        }
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return {
            "content": [{"type": "error", "text": f"Validation error: {str(e)}"}],
            "is_error": True
        }
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


@tool()
def list_commits(params: Dict) -> Dict:
    """List commits in a GitHub repository.

    Args:
        params: Dictionary with commit parameters
            - owner: Repository owner (username or organization)
            - repo: Repository name
            - page: Page number (optional)
            - per_page: Results per page (optional)
            - sha: Branch name or commit SHA (optional)

    Returns:
        MCP response with list of commits
    """
    try:
        logger.debug(f"list_commits called with params: {params}")
        # Convert dict to Pydantic model
        commits_params = ListCommitsParams(**params)
        
        # Call operation
        result = repositories.list_commits(commits_params)
        
        logger.debug(f"Got {len(result)} commits")
        return {
            "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
        }
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return {
            "content": [{"type": "error", "text": f"Validation error: {str(e)}"}],
            "is_error": True
        }
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
