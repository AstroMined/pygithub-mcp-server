"""Repository operations.

This module provides operations for GitHub repositories, including
creating, forking, searching, and managing repositories.
"""

import logging
from typing import Any, Dict, List, Optional

from github import GithubException
from github.ContentFile import ContentFile
from github.GitRef import GitRef
from github.Repository import Repository

from pygithub_mcp_server.client.client import GitHubClient
from pygithub_mcp_server.converters.common.pagination import get_paginated_items
from pygithub_mcp_server.converters.repositories.repositories import convert_repository
from pygithub_mcp_server.converters.repositories.contents import convert_file_content
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
from pygithub_mcp_server.schemas.base import FileContent
from pygithub_mcp_server.errors.exceptions import GitHubError

logger = logging.getLogger(__name__)


def get_repository(owner: str, repo: str) -> Dict[str, Any]:
    """Get a repository by owner and name.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name

    Returns:
        Repository data in our schema

    Raises:
        GitHubError: If repository access fails
    """
    logger.debug(f"Getting repository: {owner}/{repo}")
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{owner}/{repo}")
        return convert_repository(repository)
    except GithubException as e:
        logger.error(f"GitHub exception when getting repo {owner}/{repo}: {str(e)}")
        raise client._handle_github_exception(e, resource_hint="repository")


def create_repository(params: CreateRepositoryParams) -> Dict[str, Any]:
    """Create a new repository.

    Args:
        params: Parameters for creating a repository

    Returns:
        Repository data in our schema

    Raises:
        GitHubError: If repository creation fails
    """
    logger.debug(f"Creating repository: {params.name}")
    try:
        client = GitHubClient.get_instance()
        github = client.github
        
        # Build kwargs from Pydantic model
        kwargs = {
            "name": params.name,
        }
        
        # Add optional parameters only if provided
        if params.description:
            kwargs["description"] = params.description
        if params.private is not None:
            kwargs["private"] = params.private
        if params.auto_init is not None:
            kwargs["auto_init"] = params.auto_init
        
        # Create repository
        repository = github.get_user().create_repo(**kwargs)
        logger.debug(f"Repository created successfully: {repository.full_name}")
        return convert_repository(repository)
    except GithubException as e:
        logger.error(f"GitHub exception when creating repository: {str(e)}")
        raise client._handle_github_exception(e, resource_hint="repository")


def fork_repository(params: ForkRepositoryParams) -> Dict[str, Any]:
    """Fork a repository.

    Args:
        params: Parameters for forking a repository

    Returns:
        Forked repository data in our schema

    Raises:
        GitHubError: If repository forking fails
    """
    logger.debug(f"Forking repository: {params.owner}/{params.repo}")
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{params.owner}/{params.repo}")
        
        # Build kwargs from Pydantic model
        kwargs = {}
        if params.organization:
            kwargs["organization"] = params.organization
        
        # Fork repository
        forked_repo = repository.create_fork(**kwargs)
        logger.debug(f"Repository forked successfully: {forked_repo.full_name}")
        return convert_repository(forked_repo)
    except GithubException as e:
        logger.error(f"GitHub exception when forking repository: {str(e)}")
        raise client._handle_github_exception(e, resource_hint="repository")


def search_repositories(params: SearchRepositoriesParams) -> List[Dict[str, Any]]:
    """Search for repositories.

    Args:
        params: Parameters for searching repositories

    Returns:
        List of matching repositories in our schema

    Raises:
        GitHubError: If repository search fails
    """
    logger.debug(f"Searching repositories with query: {params.query}")
    try:
        client = GitHubClient.get_instance()
        github = client.github
        
        # Search repositories
        paginated_repos = github.search_repositories(query=params.query)
        
        # Handle pagination
        repos = get_paginated_items(paginated_repos, params.page, params.per_page)
        
        # Convert repositories to our schema
        return [convert_repository(repo) for repo in repos]
    except GithubException as e:
        logger.error(f"GitHub exception when searching repositories: {str(e)}")
        raise client._handle_github_exception(e, resource_hint="repository")


def get_file_contents(params: GetFileContentsParams) -> Dict[str, Any]:
    """Get contents of a file in a repository.

    Args:
        params: Parameters for getting file contents

    Returns:
        File content data in our schema

    Raises:
        GitHubError: If file access fails
    """
    logger.debug(f"Getting file contents: {params.owner}/{params.repo}/{params.path}")
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{params.owner}/{params.repo}")
        
        # Build kwargs from Pydantic model
        kwargs = {"path": params.path}
        if params.branch:
            kwargs["ref"] = params.branch
        
        # Get file contents
        content_file = repository.get_contents(**kwargs)
        
        # Handle case where get_contents returns a list (for directories)
        if isinstance(content_file, list):
            return {
                "is_directory": True,
                "path": params.path,
                "contents": [convert_file_content(item) for item in content_file]
            }
        
        # Handle case where get_contents returns a single file
        return convert_file_content(content_file)
    except GithubException as e:
        logger.error(f"GitHub exception when getting file contents: {str(e)}")
        raise client._handle_github_exception(e, resource_hint="content_file")


def create_or_update_file(params: CreateOrUpdateFileParams) -> Dict[str, Any]:
    """Create or update a file in a repository.

    Args:
        params: Parameters for creating or updating a file

    Returns:
        Result data including commit info

    Raises:
        GitHubError: If file creation/update fails
    """
    logger.debug(f"Creating/updating file: {params.owner}/{params.repo}/{params.path}")
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{params.owner}/{params.repo}")
        
        # Build kwargs from Pydantic model
        kwargs = {
            "path": params.path,
            "message": params.message,
            "content": params.content,
            "branch": params.branch
        }
        
        # Add SHA if updating an existing file
        if params.sha:
            kwargs["sha"] = params.sha
        
        # Create or update file
        result = repository.create_file(**kwargs)
        
        logger.debug(f"File created/updated successfully: {params.path}")
        
        # Log detailed information about the response structure for debugging
        logger.debug(f"Commit result type: {type(result['commit']).__name__}")
        if hasattr(result['commit'], 'commit'):
            logger.debug(f"Has nested commit: {result['commit'].commit is not None}")
        
        # Extract commit information safely with fallbacks
        commit_sha = None
        commit_message = None
        commit_url = None
        
        try:
            # Get commit SHA
            if hasattr(result["commit"], "sha"):
                commit_sha = result["commit"].sha
            
            # Get commit message with multiple fallbacks
            if hasattr(result["commit"], "commit") and result["commit"].commit is not None:
                if hasattr(result["commit"].commit, "message"):
                    commit_message = result["commit"].commit.message
            if commit_message is None and hasattr(result["commit"], "message"):
                commit_message = result["commit"].message
            if commit_message is None:
                commit_message = params.message  # Fall back to the provided commit message
            
            # Get commit URL
            if hasattr(result["commit"], "html_url"):
                commit_url = result["commit"].html_url
        except (AttributeError, KeyError) as e:
            logger.warning(f"Error extracting commit details: {e}")
            # Continue execution even if we can't get all commit details
        
        # Extract content information safely
        content_sha = None
        content_size = None
        content_url = None
        
        try:
            if hasattr(result["content"], "sha"):
                content_sha = result["content"].sha
            if hasattr(result["content"], "size"):
                content_size = result["content"].size
            if hasattr(result["content"], "html_url"):
                content_url = result["content"].html_url
        except (AttributeError, KeyError) as e:
            logger.warning(f"Error extracting content details: {e}")
            # Continue execution even if we can't get all content details
        
        return {
            "commit": {
                "sha": commit_sha,
                "message": commit_message,
                "html_url": commit_url
            },
            "content": {
                "path": params.path,
                "sha": content_sha,
                "size": content_size,
                "html_url": content_url
            }
        }
    except GithubException as e:
        logger.error(f"GitHub exception when creating/updating file: {str(e)}")
        raise client._handle_github_exception(e, resource_hint="content_file")


def push_files(params: PushFilesParams) -> Dict[str, Any]:
    """Push multiple files to a repository in a single commit.
    
    This is a convenience wrapper around multiple create_file operations.
    Note: This does not support directories or binary files yet.

    Args:
        params: Parameters for pushing multiple files

    Returns:
        Result including commit info

    Raises:
        GitHubError: If file push fails
    """
    logger.debug(f"Pushing {len(params.files)} files to {params.owner}/{params.repo}")
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{params.owner}/{params.repo}")
        
        # Get current file SHAs if they exist
        file_shas = {}
        for file_content in params.files:
            try:
                existing_file = repository.get_contents(
                    path=file_content.path, 
                    ref=params.branch
                )
                if not isinstance(existing_file, list):
                    file_shas[file_content.path] = existing_file.sha
            except GithubException:
                # File doesn't exist yet, no SHA needed
                pass
        
        # Create a commit for each file
        results = []
        for file_content in params.files:
            kwargs = {
                "path": file_content.path,
                "message": params.message,
                "content": file_content.content,
                "branch": params.branch
            }
            
            # Add SHA if updating an existing file
            if file_content.path in file_shas:
                kwargs["sha"] = file_shas[file_content.path]
            
            result = repository.create_file(**kwargs)
            
            # Extract content SHA safely
            content_sha = None
            try:
                if hasattr(result["content"], "sha"):
                    content_sha = result["content"].sha
                elif isinstance(result["content"], dict) and "sha" in result["content"]:
                    content_sha = result["content"]["sha"]
            except (AttributeError, KeyError, TypeError) as e:
                logger.warning(f"Error extracting content SHA for {file_content.path}: {e}")
                # If we can't get the SHA, we'll proceed without it
            
            results.append({
                "path": file_content.path,
                "sha": content_sha
            })
        
        logger.debug(f"Files pushed successfully to {params.owner}/{params.repo}")
        return {
            "message": params.message,
            "branch": params.branch,
            "files": results
        }
    except GithubException as e:
        logger.error(f"GitHub exception when pushing files: {str(e)}")
        raise client._handle_github_exception(e, resource_hint="content_file")


def create_branch(params: CreateBranchParams) -> Dict[str, Any]:
    """Create a new branch in a repository.

    Args:
        params: Parameters for creating a branch

    Returns:
        Branch data in our schema

    Raises:
        GitHubError: If branch creation fails
    """
    logger.debug(f"Creating branch {params.branch} in {params.owner}/{params.repo}")
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{params.owner}/{params.repo}")
        
        # Get source branch to use as base
        if params.from_branch:
            # Use specified source branch
            source_branch = params.from_branch
        else:
            # Use repository default branch
            source_branch = repository.default_branch
        
        # Get the SHA of the latest commit on the source branch
        source_ref = repository.get_git_ref(f"heads/{source_branch}")
        sha = source_ref.object.sha
        
        # Create the new branch
        new_branch = repository.create_git_ref(f"refs/heads/{params.branch}", sha)
        
        logger.debug(f"Branch created successfully: {params.branch}")
        return {
            "name": params.branch,
            "sha": new_branch.object.sha,
            "url": new_branch.url
        }
    except GithubException as e:
        logger.error(f"GitHub exception when creating branch: {str(e)}")
        raise client._handle_github_exception(e, resource_hint="git_ref")


def list_commits(params: ListCommitsParams) -> List[Dict[str, Any]]:
    """List commits in a repository.

    Args:
        params: Parameters for listing commits

    Returns:
        List of commits in our schema

    Raises:
        GitHubError: If commit listing fails
    """
    logger.debug(f"Listing commits for {params.owner}/{params.repo}")
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{params.owner}/{params.repo}")
        
        # Build kwargs from Pydantic model
        kwargs = {}
        if params.sha:
            kwargs["sha"] = params.sha
        
        # Get commits
        paginated_commits = repository.get_commits(**kwargs)
        
        # Handle pagination
        commits = get_paginated_items(paginated_commits, params.page, params.per_page)
        
        # Convert commits to our schema
        return [{
            "sha": commit.sha,
            "message": commit.commit.message,
            "author": {
                "name": commit.commit.author.name,
                "email": commit.commit.author.email,
                "date": commit.commit.author.date.isoformat()
            },
            "html_url": commit.html_url
        } for commit in commits]
    except GithubException as e:
        logger.error(f"GitHub exception when listing commits: {str(e)}")
        raise client._handle_github_exception(e, resource_hint="commit")
