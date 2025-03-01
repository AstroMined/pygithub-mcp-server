"""Tests for environment utility functions.

This module tests the environment utility functions used to get environment
variables and configuration values.
"""

import os
import pytest
from unittest.mock import patch

from pygithub_mcp_server.errors import GitHubError
from pygithub_mcp_server.utils.environment import (
    get_github_token,
    get_env_var,
    get_bool_env_var,
)


class TestGetGithubToken:
    """Tests for get_github_token function."""

    @patch.dict(os.environ, {"GITHUB_PERSONAL_ACCESS_TOKEN": "test-token"})
    def test_with_token_in_env(self):
        """Test when token is in environment."""
        token = get_github_token()
        assert token == "test-token"

    @patch.dict(os.environ, {}, clear=True)
    def test_without_token_in_env(self):
        """Test when token is not in environment."""
        with pytest.raises(GitHubError) as exc_info:
            get_github_token()
        assert "GITHUB_PERSONAL_ACCESS_TOKEN" in str(exc_info.value)


class TestGetEnvVar:
    """Tests for get_env_var function."""

    @patch.dict(os.environ, {"TEST_VAR": "test-value"})
    def test_with_var_in_env(self):
        """Test when variable is in environment."""
        value = get_env_var("TEST_VAR")
        assert value == "test-value"

    @patch.dict(os.environ, {}, clear=True)
    def test_without_var_in_env_no_default(self):
        """Test when variable is not in environment and no default."""
        with pytest.raises(ValueError) as exc_info:
            get_env_var("TEST_VAR")
        assert "TEST_VAR" in str(exc_info.value)

    @patch.dict(os.environ, {}, clear=True)
    def test_without_var_in_env_with_default(self):
        """Test when variable is not in environment but default is provided."""
        value = get_env_var("TEST_VAR", default="default-value")
        assert value == "default-value"


class TestGetBoolEnvVar:
    """Tests for get_bool_env_var function."""

    @pytest.mark.parametrize("env_value,expected", [
        ("true", True),
        ("True", True),
        ("TRUE", True),
        ("1", True),
        ("yes", True),
        ("Yes", True),
        ("YES", True),
        ("false", False),
        ("False", False),
        ("FALSE", False),
        ("0", False),
        ("no", False),
        ("No", False),
        ("NO", False),
    ])
    def test_with_valid_bool_values(self, env_value, expected):
        """Test with valid boolean values."""
        with patch.dict(os.environ, {"TEST_BOOL": env_value}):
            value = get_bool_env_var("TEST_BOOL")
            assert value is expected

    @patch.dict(os.environ, {"TEST_BOOL": "invalid"})
    def test_with_invalid_bool_value(self):
        """Test with invalid boolean value."""
        with pytest.raises(ValueError) as exc_info:
            get_bool_env_var("TEST_BOOL")
        assert "TEST_BOOL" in str(exc_info.value)
        assert "invalid" in str(exc_info.value)

    @patch.dict(os.environ, {}, clear=True)
    def test_without_var_in_env_no_default(self):
        """Test when variable is not in environment and no default."""
        with pytest.raises(ValueError) as exc_info:
            get_bool_env_var("TEST_BOOL")
        assert "TEST_BOOL" in str(exc_info.value)

    @patch.dict(os.environ, {}, clear=True)
    def test_without_var_in_env_with_default(self):
        """Test when variable is not in environment but default is provided."""
        value = get_bool_env_var("TEST_BOOL", default=True)
        assert value is True
