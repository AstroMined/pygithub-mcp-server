"""GitHub issue operations.

This module provides functions for working with issues in GitHub repositories,
including creation, updates, comments, and listing.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from github import GithubException

from ..common.converters import convert_issue, convert_issue_comment, convert_label
from ..common.errors import GitHubError
from ..common.github import GitHubClient


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

        # Get milestone object if number provided
        milestone_obj = None
        if milestone is not None:
            milestone_obj = repository.get_milestone(milestone)

        # Create issue using PyGithub
        issue = repository.create_issue(
            title=title,
            body=body,
            assignees=assignees,
            labels=labels,
            milestone=milestone_obj,
        )

        # Convert to our schema
        return convert_issue(issue)

    except GithubException as e:
        # GitHubClient's get_repo will handle the exception
        raise


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
        # GitHubClient's get_repo will handle the exception
        raise


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

        # Get milestone object if number provided
        milestone_obj = None
        if milestone is not None:
            milestone_obj = repository.get_milestone(milestone)

        # Update issue using PyGithub
        # Note: PyGithub's edit() method handles None values appropriately
        issue.edit(
            title=title,
            body=body,
            state=state,
            labels=labels,
            assignees=assignees,
            milestone=milestone_obj,  # None will clear the milestone
        )

        # Get fresh issue data after update
        updated_issue = repository.get_issue(issue_number)
        return convert_issue(updated_issue)

    except GithubException as e:
        # GitHubClient's get_repo will handle the exception
        raise


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
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{owner}/{repo}")

        # Convert labels list to comma-separated string if provided
        label_str = ",".join(labels) if labels else None

        # Get paginated issues
        issues = repository.get_issues(
            state=state,
            labels=label_str,
            sort=sort,
            direction=direction,
            since=since,
        )

        # Handle pagination
        if page is not None:
            issues = issues.get_page(page - 1)  # PyGithub uses 0-based indexing
        elif per_page is not None:
            issues = list(issues[:per_page])
        else:
            issues = list(issues)

        # Convert each issue to our schema
        return [convert_issue(issue) for issue in issues]

    except GithubException as e:
        # GitHubClient's get_repo will handle the exception
        raise


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
        # GitHubClient's get_repo will handle the exception
        raise


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

        # Get paginated comments
        comments = issue.get_comments(since=since)

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
        # GitHubClient's get_repo will handle the exception
        raise


def update_issue_comment(
    owner: str, repo: str, comment_id: int, body: str
) -> Dict[str, Any]:
    """Update an issue comment.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
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
        comment = repository.get_issue_comment(comment_id)
        comment.edit(body)
        return convert_issue_comment(comment)
    except GithubException as e:
        # GitHubClient's get_repo will handle the exception
        raise


def delete_issue_comment(owner: str, repo: str, comment_id: int) -> None:
    """Delete an issue comment.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        comment_id: Comment ID to delete

    Raises:
        GitHubError: If the API request fails
    """
    try:
        client = GitHubClient.get_instance()
        repository = client.get_repo(f"{owner}/{repo}")
        comment = repository.get_issue_comment(comment_id)
        comment.delete()
    except GithubException as e:
        # GitHubClient's get_repo will handle the exception
        raise


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
        # GitHubClient's get_repo will handle the exception
        raise


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
        # GitHubClient's get_repo will handle the exception
        raise
