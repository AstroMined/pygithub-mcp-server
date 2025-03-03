"""Unit tests for configuration settings module.

These tests use real environment variables and real files to test the
configuration loading functionality with no mocks.
"""

import os
import json
import tempfile
import shutil
from pathlib import Path

import pytest
from pygithub_mcp_server.config.settings import load_config, DEFAULT_CONFIG


@pytest.fixture
def clean_config_env():
    """Fixture to clean environment variables that affect configuration.
    
    This fixture removes environment variables that would affect the
    configuration loading, then restores them after the test.
    """
    # Store original values
    orig_env = {}
    env_vars = [
        "PYGITHUB_MCP_CONFIG",
        "PYGITHUB_ENABLE_ISSUES",
        "PYGITHUB_ENABLE_REPOSITORIES", 
        "PYGITHUB_ENABLE_PULL_REQUESTS",
        "PYGITHUB_ENABLE_DISCUSSIONS",
        "PYGITHUB_ENABLE_SEARCH",
        "PYGITHUB_ENABLE_USERS",
        "PYGITHUB_ENABLE_ORGANIZATIONS",
        "PYGITHUB_ENABLE_TEAMS",
        "PYGITHUB_ENABLE_WEBHOOKS",
        "PYGITHUB_ENABLE_GISTS",
    ]
    
    for var in env_vars:
        if var in os.environ:
            orig_env[var] = os.environ[var]
            del os.environ[var]
    
    yield
    
    # Restore original values
    for var in env_vars:
        if var in os.environ:
            del os.environ[var]
    
    for var, value in orig_env.items():
        os.environ[var] = value


@pytest.fixture
def temp_config_file():
    """Fixture that creates a temporary config file.
    
    This fixture creates a temporary file that can be used as a config file
    and cleans it up after the test.
    
    Returns:
        Path to temporary file
    """
    # Create temporary file
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    
    yield path
    
    # Clean up
    if os.path.exists(path):
        os.unlink(path)


class TestConfigSettings:
    """Tests for the configuration settings module."""
    
    def test_default_configuration(self, clean_config_env):
        """Test default configuration is loaded correctly when no overrides exist."""
        # Load config with clean environment
        config = load_config()
        
        # Verify default configuration is returned
        assert config is not None
        assert "tool_groups" in config
        assert config["tool_groups"]["issues"]["enabled"] is True
        assert config["tool_groups"]["repositories"]["enabled"] is False
        assert config["tool_groups"]["pull_requests"]["enabled"] is False
    
    def test_environment_variable_override(self, clean_config_env):
        """Test environment variables override default configuration."""
        # Set environment variables to override defaults
        os.environ["PYGITHUB_ENABLE_REPOSITORIES"] = "true"
        os.environ["PYGITHUB_ENABLE_ISSUES"] = "false"
        os.environ["PYGITHUB_ENABLE_PULL_REQUESTS"] = "1"
        
        # Load config with environment overrides
        config = load_config()
        
        # Verify environment variables override defaults
        assert config["tool_groups"]["repositories"]["enabled"] is True
        assert config["tool_groups"]["issues"]["enabled"] is False
        assert config["tool_groups"]["pull_requests"]["enabled"] is True
    
    def test_config_file_override(self, clean_config_env, temp_config_file):
        """Test configuration file overrides default configuration."""
        # Create config data
        config_data = {
            "tool_groups": {
                "issues": {"enabled": False},
                "repositories": {"enabled": True},
                "discussions": {"enabled": True}
            },
            "logging": {
                "level": "DEBUG"
            }
        }
        
        # Write config to file
        with open(temp_config_file, "w") as f:
            json.dump(config_data, f)
        
        # Set environment variable to point to config file
        os.environ["PYGITHUB_MCP_CONFIG"] = temp_config_file
        
        # Load config with file override
        config = load_config()
        
        # Verify file configuration overrides defaults
        assert config["tool_groups"]["issues"]["enabled"] is False
        assert config["tool_groups"]["repositories"]["enabled"] is True
        assert config["tool_groups"]["discussions"]["enabled"] is True
        assert config.get("logging", {}).get("level") == "DEBUG"
    
    def test_environment_overrides_file(self, clean_config_env, temp_config_file):
        """Test environment variables override file configuration."""
        # Create config data
        config_data = {
            "tool_groups": {
                "issues": {"enabled": False},
                "repositories": {"enabled": False}
            }
        }
        
        # Write config to file
        with open(temp_config_file, "w") as f:
            json.dump(config_data, f)
        
        # Set environment variables
        os.environ["PYGITHUB_MCP_CONFIG"] = temp_config_file
        os.environ["PYGITHUB_ENABLE_REPOSITORIES"] = "true"
        
        # Load config with file and environment overrides
        config = load_config()
        
        # Verify environment variables override file configuration
        assert config["tool_groups"]["issues"]["enabled"] is False  # From file
        assert config["tool_groups"]["repositories"]["enabled"] is True  # From env var
    
    def test_invalid_config_file(self, clean_config_env, temp_config_file):
        """Test handling of invalid configuration file."""
        # Write invalid JSON to file
        with open(temp_config_file, "w") as f:
            f.write("not valid json")
        
        # Set environment variable to point to invalid config file
        os.environ["PYGITHUB_MCP_CONFIG"] = temp_config_file
        
        # Load config with invalid file
        config = load_config()
        
        # Verify defaults are used
        assert config["tool_groups"]["issues"]["enabled"] is True
        assert config["tool_groups"]["repositories"]["enabled"] is False
    
    def test_nonexistent_config_file(self, clean_config_env):
        """Test handling of nonexistent configuration file."""
        # Set environment variable to point to nonexistent file
        os.environ["PYGITHUB_MCP_CONFIG"] = "/nonexistent/file.json"
        
        # Load config with nonexistent file
        config = load_config()
        
        # Verify defaults are used
        assert config["tool_groups"]["issues"]["enabled"] is True
        assert config["tool_groups"]["repositories"]["enabled"] is False
