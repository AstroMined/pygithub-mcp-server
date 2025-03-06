"""GitHub issue operations.

This module provides functions for working with issues in GitHub repositories,
including creation, updates, comments, and listing.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from github import GithubException
from github.PaginatedList import PaginatedList

from ..converters.issues.issues import convert_issue, convert_label
from ..converters.issues.comments import convert_issue_comment
from ..converters.common.datetime import with_utc_datetimes, ensure_utc_datetime
from ..converters.common.pagination import get_paginated_items
from ..errors import GitHubError
from ..client import GitHubClient
from ..schemas.issues import (
    ListIssuesParams,
    GetIssueParams,
    CreateIssueParams,
    UpdateIssueParams,
    IssueCommentParams,
    ListIssueCommentsParams,
    UpdateIssueCommentParams,
    DeleteIssueCommentParams,
    AddIssueLabelsParams,
    RemoveIssueLabelParams,
)

# Get logger
logger = logging.getLogger(__name__)


def create_issue(params: CreateIssueParams) -> Dict[str, Any]:
    """Create a new issue in a repository.

    Args:
        params: Validated parameters for creating an issue

    Returns:
        Created issue details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{params.owner}/{params.repo}")

        # Build kwargs for create_issue using fields from the Pydantic model
        kwargs = {"title": params.title}  # title is required

        # Add optional parameters only if provided
        if params.body is not None:
            kwargs["body"] = params.body
        if params.assignees:  # Only add if non-empty list
            kwargs["assignees"] = params.assignees
        if params.labels:  # Only add if non-empty list
            kwargs["labels"] = params.labels
        if params.milestone is not None:
            try:
                kwargs["milestone"] = repository.get_milestone(params.milestone)
            except Exception as e:
                logger.error(f"Failed to get milestone {params.milestone}: {e}")
                raise GitHubError(f"Invalid milestone number: {params.milestone}")

        # Create issue using PyGithub
        issue = repository.create_issue(**kwargs)

        # Convert to our schema
        return convert_issue(issue)

    except GithubException as e:
        raise GitHubClient.get_instance()._handle_github_exception(e)


def get_issue(params: GetIssueParams) -> Dict[str, Any]:
    """Get details about a specific issue.

    Args:
        params: Validated parameters for getting an issue

    Returns:
        Issue details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{params.owner}/{params.repo}")
        issue = repository.get_issue(params.issue_number)
        return convert_issue(issue)
    except GithubException as e:
        raise GitHubClient.get_instance()._handle_github_exception(e)


def update_issue(params: UpdateIssueParams) -> Dict[str, Any]:
    """Update an existing issue.

    Args:
        params: Validated parameters for updating an issue

    Returns:
        Updated issue details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    try:
        logger.debug(f"update_issue called with params: {params}")
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{params.owner}/{params.repo}")
        issue = repository.get_issue(params.issue_number)
        logger.debug(f"Got issue with title: {issue.title}")

        # Build kwargs with only provided values
        kwargs = {}
        
        if params.title is not None:
            kwargs["title"] = params.title
            logger.debug(f"Adding title={params.title} to kwargs")
        if params.body is not None:
            kwargs["body"] = params.body
        if params.state is not None:
            kwargs["state"] = params.state
        if params.labels is not None:
            kwargs["labels"] = params.labels
        if params.assignees is not None:
            kwargs["assignees"] = params.assignees
        if params.milestone is not None:
            try:
                kwargs["milestone"] = repository.get_milestone(params.milestone)
            except Exception as e:
                logger.error(f"Failed to get milestone {params.milestone}: {e}")
                raise GitHubError(f"Invalid milestone number: {params.milestone}")

        logger.debug(f"kwargs for edit: {kwargs}")

        # If no changes provided, return current issue state
        if not kwargs:
            return convert_issue(issue)

        # Update issue using PyGithub with only provided values
        # PyGithub's edit() method returns None, not the updated issue
        issue.edit(**kwargs)
        
        # Get fresh issue data to ensure we have the latest state
        updated_issue = repository.get_issue(params.issue_number)
        logger.debug(f"After edit, updated_issue.title: {updated_issue.title}")

        # Create a custom converter for this specific case to handle empty strings properly
        def custom_convert_issue(issue):
            result = convert_issue(issue)
            # Ensure empty strings remain empty strings and don't become None
            if params.body == "":
                result["body"] = ""
            return result
        
        # Return the updated issue with special handling for empty strings
        result = custom_convert_issue(updated_issue)
        logger.debug(f"Converted result: {result}")
        return result

    except GithubException as e:
        raise GitHubClient.get_instance()._handle_github_exception(e)


def list_issues(params: ListIssuesParams) -> List[Dict[str, Any]]:
    """List issues in a repository.

    Args:
        params: Validated parameters for listing issues

    Returns:
        List of issues from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    try:
        # No need for parameter validation as Pydantic already validated the input
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{params.owner}/{params.repo}")

        # Default to 'open' if state is None
        state = params.state or 'open'

        # Build kwargs for get_issues using fields from the Pydantic model
        kwargs = {"state": state}
        
        # Add optional parameters only if provided
        if params.sort:
            kwargs["sort"] = params.sort
        if params.direction:
            kwargs["direction"] = params.direction
        if params.since:
            kwargs["since"] = params.since
            logger.debug(f"Using UTC since parameter: {params.since.isoformat()}")
        if params.labels is not None:
            # Convert to PyGithub-compatible format
            from ..converters.parameters import convert_labels_parameter
            kwargs["labels"] = convert_labels_parameter(params.labels)
            logger.debug(f"Using labels filter: {kwargs['labels']}")
            
        # Get paginated issues
        logger.debug(f"Getting issues for {params.owner}/{params.repo} with kwargs: {kwargs}")
        try:
            paginated_issues = repository.get_issues(**kwargs)
            logger.debug(f"Got PaginatedList of issues: {paginated_issues}")
        except AssertionError as e:
            logger.error(f"PyGithub assertion error: {e}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error args: {e.args}")
            raise GitHubError("Invalid parameter values for get_issues")
        except GithubException as e:
            # Let the GitHub client handle the exception properly
            raise GitHubClient.get_instance()._handle_github_exception(e)
        except Exception as e:
            logger.error(f"Error getting issues: {e}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error args: {e.args}")
            raise GitHubError(f"Failed to get issues: {str(e)}")

        try:
            # Use our pagination utility to safely handle paginated lists
            issues = get_paginated_items(paginated_issues, params.page, params.per_page)
            
            logger.debug(f"Retrieved {len(issues)} issues")

            # Convert each issue to our schema
            converted_issues = [convert_issue(issue) for issue in issues]
            logger.debug(f"Converted {len(converted_issues)} issues to schema")
            return converted_issues

        except Exception as e:
            logger.error(f"Error handling pagination: {str(e)}")
            raise GitHubError(f"Error retrieving issues: {str(e)}")

    except GithubException as e:
        # Convert PyGithub exception to our error type
        error = GitHubClient.get_instance()._handle_github_exception(e)
        raise error


def add_issue_comment(params: IssueCommentParams) -> Dict[str, Any]:
    """Add a comment to an issue.

    Args:
        params: Validated parameters for adding a comment

    Returns:
        Created comment details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{params.owner}/{params.repo}")
        issue = repository.get_issue(params.issue_number)
        comment = issue.create_comment(params.body)
        return convert_issue_comment(comment)
    except GithubException as e:
        raise GitHubClient.get_instance()._handle_github_exception(e)


def list_issue_comments(params: ListIssueCommentsParams) -> List[Dict[str, Any]]:
    """List comments on an issue.

    Args:
        params: Validated parameters for listing comments

    Returns:
        List of comments from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{params.owner}/{params.repo}")
        issue = repository.get_issue(params.issue_number)

        # Build kwargs for get_comments
        kwargs = {}
        if params.since is not None:
            logger.debug(f"Using UTC since parameter: {params.since.isoformat()}")
            kwargs["since"] = params.since

        # Get paginated comments with only provided parameters
        paginated_comments = issue.get_comments(**kwargs)
        
        # Use our pagination utility for consistent pagination handling
        comments = get_paginated_items(paginated_comments, params.page, params.per_page)

        logger.debug(f"Retrieved {len(comments)} comments")

        # Convert each comment to our schema
        converted_comments = [convert_issue_comment(comment) for comment in comments]
        return converted_comments

    except GithubException as e:
        raise GitHubClient.get_instance()._handle_github_exception(e)


def update_issue_comment(params: UpdateIssueCommentParams) -> Dict[str, Any]:
    """Update an issue comment.

    Args:
        params: Validated parameters for updating a comment

    Returns:
        Updated comment details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{params.owner}/{params.repo}")
        issue = repository.get_issue(params.issue_number)
        comment = issue.get_comment(params.comment_id)
        comment.edit(params.body)
        return convert_issue_comment(comment)
    except GithubException as e:
        raise GitHubClient.get_instance()._handle_github_exception(e)


def delete_issue_comment(params: DeleteIssueCommentParams) -> None:
    """Delete an issue comment.

    Args:
        params: Validated parameters for deleting a comment

    Raises:
        GitHubError: If the API request fails
    """
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{params.owner}/{params.repo}")
        issue = repository.get_issue(params.issue_number)
        comment = issue.get_comment(params.comment_id)
        comment.delete()
    except GithubException as e:
        raise GitHubClient.get_instance()._handle_github_exception(e)


def add_issue_labels(params: AddIssueLabelsParams) -> List[Dict[str, Any]]:
    """Add labels to an issue.

    Args:
        params: Validated parameters for adding labels to an issue

    Returns:
        Updated list of labels from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{params.owner}/{params.repo}")
        issue = repository.get_issue(params.issue_number)

        # Add labels to the issue
        issue.add_to_labels(*params.labels)

        # Get fresh issue data to get updated labels
        updated_issue = repository.get_issue(params.issue_number)
        return [convert_label(label) for label in updated_issue.labels]

    except GithubException as e:
        raise GitHubClient.get_instance()._handle_github_exception(e)


def remove_issue_label(params: RemoveIssueLabelParams) -> None:
    """Remove a label from an issue.

    Args:
        params: Validated parameters for removing a label from an issue

    Raises:
        GitHubError: If the API request fails or label doesn't exist
    """
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{params.owner}/{params.repo}")
        issue = repository.get_issue(params.issue_number)
        try:
            issue.remove_from_labels(params.label)
        except GithubException as label_e:
            # Handle specific case for non-existent labels
            if label_e.status == 404 and "Label does not exist" in str(label_e):
                logger.warning(f"Label '{params.label}' does not exist on issue #{params.issue_number}")
                # Not raising an error since removing a non-existent label is not a failure
                return
            # Re-raise if it's a different error
            raise label_e
    except GithubException as e:
        raise client._handle_github_exception(e)
