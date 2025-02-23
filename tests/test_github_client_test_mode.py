"""Tests for GitHub client test mode functionality.

This module tests the GitHubClient's test mode features including
environment detection, mock client integration, and safety checks.
"""

import os
import pytest
from unittest.mock import Mock

from github import Github
from pygithub_mcp_server.common.github import GitHubClient
from pygithub_mcp_server.common.errors import GitHubError


def test_test_mode_detection(enable_test_mode):
    """Test that test mode is properly detected."""
    client = GitHubClient.get_instance()
    assert client.test_mode is True


def test_test_mode_prevents_real_auth():
    """Test that test mode prevents real authentication attempts."""
    os.environ["GITHUB_TEST_MODE"] = "true"
    os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"] = "real-token"
    
    client = GitHubClient.get_instance()
    assert client._github is None
    assert client.test_mode is True

    os.environ.pop("GITHUB_TEST_MODE")
    os.environ.pop("GITHUB_PERSONAL_ACCESS_TOKEN")


def test_test_client_requires_test_mode():
    """Test that set_test_client requires test mode."""
    client = GitHubClient.get_instance()
    mock_client = Mock(spec=Github)
    
    with pytest.raises(GitHubError) as exc:
        client.set_test_client(mock_client)
    assert "Cannot set test client when not in test mode" in str(exc.value)


def test_test_client_integration(test_client, mock_repo):
    """Test that test client is properly integrated."""
    repo = test_client.get_repo("owner/repo")
    assert repo is mock_repo
    assert test_client.test_mode is True


def test_test_mode_with_missing_mock(enable_test_mode):
    """Test error when accessing GitHub instance without setting mock."""
    client = GitHubClient.get_instance()
    
    with pytest.raises(GitHubError) as exc:
        _ = client.github
    assert "GitHub client not mocked" in str(exc.value)


def test_test_environment_detection(monkeypatch):
    """Test various test environment detection scenarios."""
    def check_is_test_env():
        client = GitHubClient.get_instance()
        return client._is_test_environment()

    # Test pytest detection
    assert check_is_test_env() is True  # We're running under pytest

    # Test CI environment
    monkeypatch.setenv("CI", "true")
    assert check_is_test_env() is True
    monkeypatch.delenv("CI", raising=False)

    # Test explicit test environment
    monkeypatch.setenv("TEST_ENVIRONMENT", "true")
    assert check_is_test_env() is True
    monkeypatch.delenv("TEST_ENVIRONMENT", raising=False)


def test_prevent_real_auth_in_test_env(monkeypatch):
    """Test prevention of real auth in test environment."""
    monkeypatch.setenv("TEST_ENVIRONMENT", "true")
    monkeypatch.setenv("GITHUB_PERSONAL_ACCESS_TOKEN", "real-token")
    
    with pytest.raises(GitHubError) as exc:
        GitHubClient.get_instance()
    assert "Attempting to use real GitHub token in test environment" in str(exc.value)

    monkeypatch.delenv("TEST_ENVIRONMENT", raising=False)
    monkeypatch.delenv("GITHUB_PERSONAL_ACCESS_TOKEN", raising=False)
