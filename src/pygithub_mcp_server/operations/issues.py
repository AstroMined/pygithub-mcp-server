"""GitHub issue operations.

This module provides functions for working with issues in GitHub repositories,
including creation, updates, comments, and listing.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from github import GithubException
from github.PaginatedList import PaginatedList

from ..common.converters import convert_issue, convert_issue_comment, convert_label
from ..common.errors import GitHubError
from ..common.github import GitHubClient

# Get logger
logger = logging.getLogger(__name__)


def create_issue(
    owner: str,
    repo: str,
    title: str,
    body: Optional[str] = None,
    assignees: Optional[List[str]] = None,
    labels: Optional[List[str]] = None,
    milestone: Optional[int] = None,
) -> Dict[str, Any]:
    """Create a new issue in a repository.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        title: Issue title
        body: Issue description
        assignees: List of usernames to assign
        labels: List of labels to add
        milestone: Milestone number to assign

    Returns:
        Created issue details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{owner}/{repo}")

        # Build kwargs for create_issue
        kwargs = {"title": title}  # title is required

        # Add optional parameters only if provided
        if body is not None:
            kwargs["body"] = body
        if assignees:  # Only add if non-empty list
            kwargs["assignees"] = assignees
        if labels:  # Only add if non-empty list
            kwargs["labels"] = labels
        if milestone is not None:
            try:
                kwargs["milestone"] = repository.get_milestone(milestone)
            except Exception as e:
                logger.error(f"Failed to get milestone {milestone}: {e}")
                raise GitHubError(f"Invalid milestone number: {milestone}")

        # Create issue using PyGithub
        issue = repository.create_issue(**kwargs)

        # Convert to our schema
        return convert_issue(issue)

    except GithubException as e:
        raise GitHubClient.get_instance()._handle_github_exception(e)


def get_issue(owner: str, repo: str, issue_number: int) -> Dict[str, Any]:
    """Get details about a specific issue.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        issue_number: Issue number

    Returns:
        Issue details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{owner}/{repo}")
        issue = repository.get_issue(issue_number)
        return convert_issue(issue)
    except GithubException as e:
        raise GitHubClient.get_instance()._handle_github_exception(e)


def update_issue(
    owner: str,
    repo: str,
    issue_number: int,
    title: Optional[str] = None,
    body: Optional[str] = None,
    state: Optional[str] = None,
    labels: Optional[List[str]] = None,
    assignees: Optional[List[str]] = None,
    milestone: Optional[Union[int, None]] = None,
) -> Dict[str, Any]:
    """Update an existing issue.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        issue_number: Issue number to update
        title: New title
        body: New description
        state: New state (open or closed)
        labels: New labels
        assignees: New assignees
        milestone: New milestone number (None to clear)

    Returns:
        Updated issue details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{owner}/{repo}")
        issue = repository.get_issue(issue_number)

        # Build kwargs with only provided values
        kwargs = {}
        
        if title is not None:
            kwargs["title"] = title
        if body is not None:
            kwargs["body"] = body
        if state is not None:
            kwargs["state"] = state
        if labels is not None:
            kwargs["labels"] = labels
        if assignees is not None:
            kwargs["assignees"] = assignees
        if milestone is not None:
            try:
                kwargs["milestone"] = repository.get_milestone(milestone)
            except Exception as e:
                logger.error(f"Failed to get milestone {milestone}: {e}")
                raise GitHubError(f"Invalid milestone number: {milestone}")

        # If no changes provided, return current issue state
        if not kwargs:
            return convert_issue(issue)

        # Update issue using PyGithub with only provided values
        issue.edit(**kwargs)

        # Get fresh issue data after update only if changes were made
        updated_issue = repository.get_issue(issue_number)
        return convert_issue(updated_issue)

    except GithubException as e:
        raise GitHubClient.get_instance()._handle_github_exception(e)


def list_issues(
    owner: str,
    repo: str,
    state: Optional[str] = None,
    labels: Optional[List[str]] = None,
    sort: Optional[str] = None,
    direction: Optional[str] = None,
    since: Optional[datetime] = None,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """List issues in a repository.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        state: Issue state (open, closed, all)
        labels: Filter by labels
        sort: Sort field (created, updated, comments)
        direction: Sort direction (asc, desc)
        since: Filter by date
        page: Page number for pagination
        per_page: Number of results per page (max 100)

    Returns:
        List of issues from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    try:
        # Validate parameters
        valid_states = {'open', 'closed', 'all'}
        # Default to 'open' if state is None
        if state is None:
            state = 'open'
        elif state not in valid_states:
            raise GitHubError(f"Invalid state: {state}. Must be one of: {valid_states}")

        valid_sorts = {'created', 'updated', 'comments'}
        if sort is not None and sort not in valid_sorts:
            raise GitHubError(f"Invalid sort: {sort}. Must be one of: {valid_sorts}")

        valid_directions = {'asc', 'desc'}
        if direction is not None and direction not in valid_directions:
            raise GitHubError(f"Invalid direction: {direction}. Must be one of: {valid_directions}")

        # Validate page and per_page
        if page is not None:
            if not isinstance(page, int) or page < 1:
                raise GitHubError("Invalid page number. Must be a positive integer.")

        if per_page is not None:
            if not isinstance(per_page, int) or per_page < 1:
                raise GitHubError("Invalid per_page value. Must be a positive integer.")
            if per_page > 100:
                raise GitHubError("per_page cannot exceed 100")

        # Handle labels parameter
        if labels is not None:
            if not isinstance(labels, list):
                raise GitHubError("Labels must be a list")
            if not all(isinstance(label, str) for label in labels):
                raise GitHubError("Labels must be a list of strings")

        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{owner}/{repo}")

        # Get paginated issues
        logger.debug(f"Getting issues for {owner}/{repo} with state={state}, labels={labels}, sort={sort}, direction={direction}")
        try:
            # Start with just the required state parameter
            paginated_issues = repository.get_issues(state=state)
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
            # Handle pagination
            if page is not None:
                logger.debug(f"Getting page {page}")
                issues = paginated_issues.get_page(page - 1)  # PyGithub uses 0-based indexing
            elif per_page is not None:
                logger.debug(f"Getting first {per_page} issues")
                issues = list(paginated_issues[:per_page])
            else:
                logger.debug("Getting all issues")
                issues = list(paginated_issues)
            
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


def add_issue_comment(
    owner: str, repo: str, issue_number: int, body: str
) -> Dict[str, Any]:
    """Add a comment to an issue.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        issue_number: Issue number to comment on
        body: Comment text

    Returns:
        Created comment details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{owner}/{repo}")
        issue = repository.get_issue(issue_number)
        comment = issue.create_comment(body)
        return convert_issue_comment(comment)
    except GithubException as e:
        raise GitHubClient.get_instance()._handle_github_exception(e)


def list_issue_comments(
    owner: str,
    repo: str,
    issue_number: int,
    since: Optional[datetime] = None,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """List comments on an issue.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        issue_number: Issue number
        since: Filter by date
        page: Page number for pagination
        per_page: Number of results per page (max 100)

    Returns:
        List of comments from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{owner}/{repo}")
        issue = repository.get_issue(issue_number)

        # Build kwargs for get_comments
        kwargs = {}
        if since is not None:
            kwargs["since"] = since

        # Get paginated comments with only provided parameters
        comments = issue.get_comments(**kwargs)

        # Handle pagination
        if page is not None:
            comments = comments.get_page(page - 1)  # PyGithub uses 0-based indexing
        elif per_page is not None:
            comments = list(comments[:per_page])
        else:
            comments = list(comments)

        # Convert each comment to our schema
        return [convert_issue_comment(comment) for comment in comments]

    except GithubException as e:
        raise GitHubClient.get_instance()._handle_github_exception(e)


def update_issue_comment(
    owner: str, repo: str, issue_number: int, comment_id: int, body: str
) -> Dict[str, Any]:
    """Update an issue comment.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        issue_number: Issue number containing the comment
        comment_id: Comment ID to update
        body: New comment text

    Returns:
        Updated comment details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{owner}/{repo}")
        issue = repository.get_issue(issue_number)
        comment = issue.get_comment(comment_id)
        comment.edit(body)
        return convert_issue_comment(comment)
    except GithubException as e:
        raise GitHubClient.get_instance()._handle_github_exception(e)


def delete_issue_comment(owner: str, repo: str, issue_number: int, comment_id: int) -> None:
    """Delete an issue comment.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        issue_number: Issue number containing the comment
        comment_id: Comment ID to delete

    Raises:
        GitHubError: If the API request fails
    """
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{owner}/{repo}")
        issue = repository.get_issue(issue_number)
        comment = issue.get_comment(comment_id)
        comment.delete()
    except GithubException as e:
        raise GitHubClient.get_instance()._handle_github_exception(e)


def add_issue_labels(
    owner: str, repo: str, issue_number: int, labels: List[str]
) -> List[Dict[str, Any]]:
    """Add labels to an issue.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        issue_number: Issue number
        labels: Labels to add

    Returns:
        Updated list of labels from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{owner}/{repo}")
        issue = repository.get_issue(issue_number)

        # Add labels to the issue
        issue.add_to_labels(*labels)

        # Get fresh issue data to get updated labels
        updated_issue = repository.get_issue(issue_number)
        return [convert_label(label) for label in updated_issue.labels]

    except GithubException as e:
        raise GitHubClient.get_instance()._handle_github_exception(e)


def remove_issue_label(
    owner: str, repo: str, issue_number: int, label: str
) -> None:
    """Remove a label from an issue.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        issue_number: Issue number
        label: Label to remove

    Raises:
        GitHubError: If the API request fails
    """
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{owner}/{repo}")
        issue = repository.get_issue(issue_number)
        issue.remove_from_labels(label)
    except GithubException as e:
        raise GitHubClient.get_instance()._handle_github_exception(e)
