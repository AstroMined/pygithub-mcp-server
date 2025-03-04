"""Unit tests for parameter formatting utilities.

These tests verify that parameter formatting functions correctly handle
various input types and edge cases.
"""

import pytest
from datetime import datetime

from pygithub_mcp_server.converters.parameters import (
    format_query_params,
    build_issue_kwargs,
    build_list_issues_kwargs,
    build_update_issue_kwargs,
    convert_labels_parameter
)


class TestFormatQueryParams:
    """Tests for format_query_params function."""
    
    def test_empty_params(self):
        """Test with no parameters."""
        result = format_query_params()
        assert result == {}
    
    def test_none_values(self):
        """Test with None values."""
        result = format_query_params(param1=None, param2="value")
        assert "param1" not in result
        assert result["param2"] == "value"
    
    def test_boolean_values(self):
        """Test with boolean values."""
        result = format_query_params(param1=True, param2=False)
        assert result["param1"] == "true"
        assert result["param2"] == "false"
    
    def test_list_values(self):
        """Test with list values."""
        result = format_query_params(param1=["a", "b", "c"])
        assert result["param1"] == "a,b,c"
    
    def test_tuple_values(self):
        """Test with tuple values."""
        result = format_query_params(param1=("a", "b", "c"))
        assert result["param1"] == "a,b,c"
    
    def test_datetime_values(self):
        """Test with datetime values."""
        dt = datetime(2025, 3, 1, 12, 0, 0)
        result = format_query_params(param1=dt)
        assert result["param1"] == dt.isoformat()
    
    def test_mixed_values(self):
        """Test with mixed value types."""
        dt = datetime(2025, 3, 1, 12, 0, 0)
        result = format_query_params(
            bool_param=True,
            list_param=["a", "b"],
            datetime_param=dt,
            string_param="value",
            none_param=None
        )
        
        assert result["bool_param"] == "true"
        assert result["list_param"] == "a,b"
        assert result["datetime_param"] == dt.isoformat()
        assert result["string_param"] == "value"
        assert "none_param" not in result
    
    def test_numeric_values(self):
        """Test with numeric values."""
        result = format_query_params(int_param=42, float_param=3.14)
        assert result["int_param"] == "42"
        assert result["float_param"] == "3.14"


class TestBuildIssueKwargs:
    """Tests for build_issue_kwargs function."""
    
    def test_empty_params(self):
        """Test with empty parameters."""
        result = build_issue_kwargs({})
        assert result == {}
    
    def test_required_params_only(self):
        """Test with only required parameters."""
        result = build_issue_kwargs({"title": "Test Issue"})
        assert result == {"title": "Test Issue"}
    
    def test_all_params(self):
        """Test with all parameters."""
        params = {
            "title": "Test Issue",
            "body": "Test Body",
            "assignees": ["user1", "user2"],
            "labels": ["bug", "enhancement"],
            "milestone": 1
        }
        result = build_issue_kwargs(params)
        assert result == params
    
    def test_none_values(self):
        """Test with None values."""
        params = {
            "title": "Test Issue",
            "body": None,
            "milestone": None
        }
        result = build_issue_kwargs(params)
        assert "title" in result
        assert "body" not in result  # None body should be skipped
        assert "milestone" not in result  # None milestone should be skipped
    
    def test_empty_lists(self):
        """Test with empty lists."""
        params = {
            "title": "Test Issue",
            "assignees": [],
            "labels": []
        }
        result = build_issue_kwargs(params)
        assert "title" in result
        assert "assignees" not in result  # Empty assignees should be skipped
        assert "labels" not in result  # Empty labels should be skipped


class TestBuildListIssuesKwargs:
    """Tests for build_list_issues_kwargs function."""
    
    def test_empty_params(self):
        """Test with empty parameters."""
        result = build_list_issues_kwargs({})
        assert result == {}
    
    def test_all_params(self):
        """Test with all parameters."""
        now = datetime.now()
        params = {
            "state": "open",
            "labels": ["bug", "enhancement"],
            "sort": "created",
            "direction": "desc",
            "since": now,
            "page": 2,
            "per_page": 30
        }
        result = build_list_issues_kwargs(params)
        assert result == params
    
    def test_none_values(self):
        """Test with None values."""
        params = {
            "state": None,
            "labels": None,
            "sort": "created"
        }
        result = build_list_issues_kwargs(params)
        assert "state" not in result
        assert "labels" not in result
        assert result["sort"] == "created"
    
    def test_partial_params(self):
        """Test with partial parameters."""
        params = {
            "state": "closed",
            "direction": "asc"
        }
        result = build_list_issues_kwargs(params)
        assert result["state"] == "closed"
        assert result["direction"] == "asc"
        assert "sort" not in result
        assert "labels" not in result
        assert "since" not in result


class TestBuildUpdateIssueKwargs:
    """Tests for build_update_issue_kwargs function."""
    
    def test_empty_params(self):
        """Test with empty parameters."""
        result = build_update_issue_kwargs({})
        assert result == {}
    
    def test_all_params(self):
        """Test with all parameters."""
        params = {
            "title": "Updated Title",
            "body": "Updated Body",
            "state": "closed",
            "labels": ["bug", "wontfix"],
            "assignees": ["user1"],
            "milestone": 2
        }
        result = build_update_issue_kwargs(params)
        assert result == params
    
    def test_none_values(self):
        """Test with None values."""
        params = {
            "title": "Updated Title",
            "body": None,
            "state": None
        }
        result = build_update_issue_kwargs(params)
        assert result["title"] == "Updated Title"
        assert "body" not in result
        assert "state" not in result
    
    def test_partial_params(self):
        """Test with partial parameters."""
        params = {
            "title": "Updated Title",
            "state": "closed"
        }
        result = build_update_issue_kwargs(params)
        assert result["title"] == "Updated Title"
        assert result["state"] == "closed"
        assert "body" not in result
        assert "labels" not in result


class TestConvertLabelsParameter:
    """Tests for convert_labels_parameter function."""
    
    def test_none_value(self):
        """Test with None value."""
        result = convert_labels_parameter(None)
        assert result is None
    
    def test_valid_labels(self):
        """Test with valid labels list."""
        labels = ["bug", "enhancement", "documentation"]
        result = convert_labels_parameter(labels)
        assert result == labels
    
    def test_empty_list(self):
        """Test with empty list."""
        result = convert_labels_parameter([])
        assert result == []
    
    def test_non_list_value(self):
        """Test with non-list value."""
        with pytest.raises(ValueError, match="Labels must be a list of strings"):
            convert_labels_parameter("not_a_list")
    
    def test_mixed_type_list(self):
        """Test with list containing non-string values."""
        with pytest.raises(ValueError, match="Labels must be a list of strings"):
            convert_labels_parameter(["bug", 123, "enhancement"])
