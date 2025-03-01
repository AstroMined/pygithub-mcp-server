"""Issue comment converters.

This module provides functions for converting PyGithub issue comment objects to our
schema representations.
"""

from typing import Any, Dict

from github.IssueComment import IssueComment

from ..common import convert_datetime
from ..users import convert_user


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
        "created_at": convert_datetime(comment.created_at),
        "updated_at": convert_datetime(comment.updated_at),
        "url": comment.url,
        "html_url": comment.html_url,
    }
