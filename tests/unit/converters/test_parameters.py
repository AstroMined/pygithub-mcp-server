"""Tests for parameter conversion functions.

This module tests the parameter conversion functions used to convert between
our schema models and PyGithub parameters.
"""

import pytest
from datetime import datetime, timezone

from pygithub_mcp_server.converters.parameters import (
    build_issue_kwargs,
    build_list_issues_kwargs,
    build_update_issue_kwargs,
)


class TestBuildIssueKwargs:
    """Tests for build_issue_kwargs function."""

    def test_with_all_parameters(self):
        """Test with all parameters provided."""
        params = {
            "title": "Test Issue",
            "body": "This is a test issue",
            "assignees": ["octocat"],
            "labels": ["bug", "help wanted"],
            "milestone": 1
        }
        
        kwargs = build_issue_kwargs(params)
        
        assert kwargs["title"] == "Test Issue"
        assert kwargs["body"] == "This is a test issue"
        assert kwargs["assignees"] == ["octocat"]
        assert kwargs["labels"] == ["bug", "help wanted"]
        assert kwargs["milestone"] == 1

    def test_with_minimal_parameters(self):
        """Test with only required parameters."""
        params = {
            "title": "Test Issue"
        }
        
        kwargs = build_issue_kwargs(params)
        
        assert kwargs["title"] == "Test Issue"
        assert "body" not in kwargs
        assert "assignees" not in kwargs
        assert "labels" not in kwargs
        assert "milestone" not in kwargs

    def test_with_none_values(self):
        """Test with None values for optional parameters."""
        params = {
            "title": "Test Issue",
            "body": None,
            "assignees": None,
            "labels": None,
            "milestone": None
        }
        
        kwargs = build_issue_kwargs(params)
        
        assert kwargs["title"] == "Test Issue"
        assert "body" not in kwargs
        assert "assignees" not in kwargs
        assert "labels" not in kwargs
        assert "milestone" not in kwargs


class TestBuildListIssuesKwargs:
    """Tests for build_list_issues_kwargs function."""

    def test_with_all_parameters(self):
        """Test with all parameters provided."""
        params = {
            "state": "open",
            "labels": ["bug"],
            "sort": "created",
            "direction": "desc",
            "since": datetime(2020, 1, 1, tzinfo=timezone.utc),
            "page": 1,
            "per_page": 30
        }
        
        kwargs = build_list_issues_kwargs(params)
        
        assert kwargs["state"] == "open"
        assert kwargs["labels"] == ["bug"]
        assert kwargs["sort"] == "created"
        assert kwargs["direction"] == "desc"
        assert kwargs["since"] == datetime(2020, 1, 1, tzinfo=timezone.utc)
        assert kwargs["page"] == 1
        assert kwargs["per_page"] == 30

    def test_with_minimal_parameters(self):
        """Test with no optional parameters."""
        params = {}
        
        kwargs = build_list_issues_kwargs(params)
        
        assert kwargs == {}

    def test_with_none_values(self):
        """Test with None values for optional parameters."""
        params = {
            "state": None,
            "labels": None,
            "sort": None,
            "direction": None,
            "since": None,
            "page": None,
            "per_page": None
        }
        
        kwargs = build_list_issues_kwargs(params)
        
        assert kwargs == {}


class TestBuildUpdateIssueKwargs:
    """Tests for build_update_issue_kwargs function."""

    def test_with_all_parameters(self):
        """Test with all parameters provided."""
        params = {
            "title": "Updated Issue",
            "body": "This is an updated issue",
            "state": "closed",
            "labels": ["bug", "fixed"],
            "assignees": ["octocat"],
            "milestone": 2
        }
        
        kwargs = build_update_issue_kwargs(params)
        
        assert kwargs["title"] == "Updated Issue"
        assert kwargs["body"] == "This is an updated issue"
        assert kwargs["state"] == "closed"
        assert kwargs["labels"] == ["bug", "fixed"]
        assert kwargs["assignees"] == ["octocat"]
        assert kwargs["milestone"] == 2

    def test_with_minimal_parameters(self):
        """Test with no optional parameters."""
        params = {}
        
        kwargs = build_update_issue_kwargs(params)
        
        assert kwargs == {}

    def test_with_none_values(self):
        """Test with None values for optional parameters."""
        params = {
            "title": None,
            "body": None,
            "state": None,
            "labels": None,
            "assignees": None,
            "milestone": None
        }
        
        kwargs = build_update_issue_kwargs(params)
        
        assert kwargs == {}

    def test_with_partial_parameters(self):
        """Test with some parameters provided."""
        params = {
            "title": "Updated Issue",
            "state": "closed"
        }
        
        kwargs = build_update_issue_kwargs(params)
        
        assert kwargs["title"] == "Updated Issue"
        assert kwargs["state"] == "closed"
        assert "body" not in kwargs
        assert "labels" not in kwargs
        assert "assignees" not in kwargs
        assert "milestone" not in kwargs
