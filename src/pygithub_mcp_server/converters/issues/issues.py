"""Issue converters.

This module provides functions for converting PyGithub issue, label, and milestone
objects to our schema representations.
"""

from typing import Any, Dict, List, Optional

from github.Issue import Issue
from github.Label import Label
from github.Milestone import Milestone

from ..common import convert_datetime
from ..users import convert_user


def convert_label(label: Label) -> Dict[str, Any]:
    """Convert a PyGithub Label to our schema.

    Args:
        label: PyGithub Label object

    Returns:
        Label data in our schema format
    """
    return {
        "id": label.id,
        "name": label.name,
        "description": label.description,
        "color": label.color,
    }


def convert_milestone(milestone: Optional[Milestone]) -> Optional[Dict[str, Any]]:
    """Convert a PyGithub Milestone to our schema.

    Args:
        milestone: PyGithub Milestone object

    Returns:
        Milestone data in our schema format
    """
    if milestone is None:
        return None

    return {
        "id": milestone.id,
        "number": milestone.number,
        "title": milestone.title,
        "description": milestone.description,
        "state": milestone.state,
        "created_at": convert_datetime(milestone.created_at),
        "updated_at": convert_datetime(milestone.updated_at),
        "due_on": convert_datetime(milestone.due_on),
    }


def convert_issue(issue: Issue) -> Dict[str, Any]:
    """Convert a PyGithub Issue to our schema.

    Args:
        issue: PyGithub Issue object

    Returns:
        Issue data in our schema format
    """
    return {
        "id": issue.id,
        "issue_number": issue.number,
        "title": issue.title,
        "body": issue.body,
        "state": issue.state,
        "state_reason": issue.state_reason,
        "locked": issue.locked,
        "active_lock_reason": issue.active_lock_reason,
        "comments": issue.comments,
        "created_at": convert_datetime(issue.created_at),
        "updated_at": convert_datetime(issue.updated_at),
        "closed_at": convert_datetime(issue.closed_at),
        "author_association": issue.author_association,
        "user": convert_user(issue.user),
        "assignee": convert_user(issue.assignee),
        "assignees": [convert_user(u) for u in issue.assignees],
        "milestone": convert_milestone(issue.milestone),
        "labels": [convert_label(l) for l in issue.labels],
        "url": issue.url,
        "html_url": issue.html_url,
        "repository": {
            "full_name": issue.repository.full_name,
            "name": issue.repository.name,
            "owner": issue.repository.owner.login,
        },
    }


def convert_issue_list(issues: List[Issue]) -> List[Dict[str, Any]]:
    """Convert a list of PyGithub Issues to our schema.

    Args:
        issues: List of PyGithub Issue objects

    Returns:
        List of issue data in our schema format
    """
    return [convert_issue(issue) for issue in issues]
