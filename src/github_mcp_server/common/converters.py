"""Conversion utilities for PyGithub objects.

This module provides functions for converting PyGithub objects to our schema
representations, ensuring consistent data structures across the application.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from github.Issue import Issue
from github.IssueComment import IssueComment
from github.Label import Label
from github.Milestone import Milestone
from github.NamedUser import NamedUser


def convert_user(user: Optional[NamedUser]) -> Optional[Dict[str, Any]]:
    """Convert a PyGithub NamedUser to our schema.

    Args:
        user: PyGithub NamedUser object

    Returns:
        User data in our schema format
    """
    if user is None:
        return None

    return {
        "login": user.login,
        "id": user.id,
        "type": user.type,
        "site_admin": user.site_admin,
    }


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
        "created_at": milestone.created_at.isoformat() if milestone.created_at else None,
        "updated_at": milestone.updated_at.isoformat() if milestone.updated_at else None,
        "due_on": milestone.due_on.isoformat() if milestone.due_on else None,
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
        "number": issue.number,
        "title": issue.title,
        "body": issue.body,
        "state": issue.state,
        "state_reason": issue.state_reason,
        "locked": issue.locked,
        "active_lock_reason": issue.active_lock_reason,
        "comments": issue.comments,
        "created_at": issue.created_at.isoformat() if issue.created_at else None,
        "updated_at": issue.updated_at.isoformat() if issue.updated_at else None,
        "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
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


def convert_issue_comment(comment: IssueComment) -> Dict[str, Any]:
    """Convert a PyGithub IssueComment to our schema.

    Args:
        comment: PyGithub IssueComment object

    Returns:
        Comment data in our schema format
    """
    return {
        "id": comment.id,
        "body": comment.body,
        "user": convert_user(comment.user),
        "created_at": comment.created_at.isoformat() if comment.created_at else None,
        "updated_at": comment.updated_at.isoformat() if comment.updated_at else None,
        "url": comment.url,
        "html_url": comment.html_url,
    }


def convert_datetime(dt: Optional[datetime]) -> Optional[str]:
    """Convert datetime to ISO format string.

    Args:
        dt: Datetime object

    Returns:
        ISO format string or None
    """
    return dt.isoformat() if dt else None
