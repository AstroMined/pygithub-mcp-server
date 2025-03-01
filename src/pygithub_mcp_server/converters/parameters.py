"""Parameter formatting utilities.

This module provides functions for formatting parameters for GitHub API requests.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union


def format_query_params(**kwargs: Any) -> Dict[str, str]:
    """Format query parameters for GitHub API requests.

    Args:
        **kwargs: Query parameters to format

    Returns:
        Formatted query parameters
    """
    params: Dict[str, str] = {}
    for key, value in kwargs.items():
        if value is not None:
            if isinstance(value, bool):
                params[key] = str(value).lower()
            elif isinstance(value, (list, tuple)):
                params[key] = ",".join(str(v) for v in value)
            elif isinstance(value, datetime):
                params[key] = value.isoformat()
            else:
                params[key] = str(value)
    return params


def build_issue_kwargs(params: Dict[str, Any]) -> Dict[str, Any]:
    """Build kwargs for issue creation.

    Args:
        params: Parameters for issue creation

    Returns:
        Kwargs for PyGithub issue creation
    """
    kwargs: Dict[str, Any] = {}
    
    # Required parameters
    if "title" in params:
        kwargs["title"] = params["title"]
    
    # Optional parameters
    if params.get("body") is not None:
        kwargs["body"] = params["body"]
    
    if params.get("assignees"):
        kwargs["assignees"] = params["assignees"]
    
    if params.get("labels"):
        kwargs["labels"] = params["labels"]
    
    if params.get("milestone") is not None:
        kwargs["milestone"] = params["milestone"]
    
    return kwargs


def build_list_issues_kwargs(params: Dict[str, Any]) -> Dict[str, Any]:
    """Build kwargs for listing issues.

    Args:
        params: Parameters for listing issues

    Returns:
        Kwargs for PyGithub list_issues
    """
    kwargs: Dict[str, Any] = {}
    
    # Optional parameters
    if params.get("state") is not None:
        kwargs["state"] = params["state"]
    
    if params.get("labels") is not None:
        kwargs["labels"] = params["labels"]
    
    if params.get("sort") is not None:
        kwargs["sort"] = params["sort"]
    
    if params.get("direction") is not None:
        kwargs["direction"] = params["direction"]
    
    if params.get("since") is not None:
        kwargs["since"] = params["since"]
    
    if params.get("page") is not None:
        kwargs["page"] = params["page"]
    
    if params.get("per_page") is not None:
        kwargs["per_page"] = params["per_page"]
    
    return kwargs


def build_update_issue_kwargs(params: Dict[str, Any]) -> Dict[str, Any]:
    """Build kwargs for updating an issue.

    Args:
        params: Parameters for updating an issue

    Returns:
        Kwargs for PyGithub issue.edit
    """
    kwargs: Dict[str, Any] = {}
    
    # Optional parameters
    if params.get("title") is not None:
        kwargs["title"] = params["title"]
    
    if params.get("body") is not None:
        kwargs["body"] = params["body"]
    
    if params.get("state") is not None:
        kwargs["state"] = params["state"]
    
    if params.get("labels") is not None:
        kwargs["labels"] = params["labels"]
    
    if params.get("assignees") is not None:
        kwargs["assignees"] = params["assignees"]
    
    if params.get("milestone") is not None:
        kwargs["milestone"] = params["milestone"]
    
    return kwargs
