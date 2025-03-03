"""Configuration module for the PyGithub MCP Server.

This package provides configuration management for the server, including loading
configurations from files and environment variables.
"""

from .settings import load_config

__all__ = ['load_config']
