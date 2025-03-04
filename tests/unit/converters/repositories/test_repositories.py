"""Unit tests for repository converters.

These tests verify that converters correctly transform repository data to our schema.
"""

import pytest
from dataclasses import dataclass

from pygithub_mcp_server.converters.repositories.repositories import convert_repository


@dataclass
class RepositoryOwner:
    """Test repository owner data class."""
    login: str


@dataclass
class Repository:
    """Test repository data class."""
    id: int
    name: str
    full_name: str
    owner: RepositoryOwner
    private: bool
    html_url: str
    description: str = None


class TestRepositoryConverters:
    """Tests for repository converters."""
    
    def test_convert_repository(self):
        """Test conversion of a Repository to our schema."""
        # Create test data using simple data classes instead of mocks
        repo = Repository(
            id=12345,
            name="test-repo",
            full_name="test-owner/test-repo",
            owner=RepositoryOwner(login="test-owner"),
            private=False,
            html_url="https://github.com/test-owner/test-repo",
            description="Test repository description"
        )
        
        # Convert the repository
        result = convert_repository(repo)
        
        # Verify the conversion
        assert result["id"] == 12345
        assert result["name"] == "test-repo"
        assert result["full_name"] == "test-owner/test-repo"
        assert result["owner"] == "test-owner"
        assert result["private"] is False
        assert result["html_url"] == "https://github.com/test-owner/test-repo"
        assert result["description"] == "Test repository description"
    
    def test_convert_repository_with_none_values(self):
        """Test conversion with None values."""
        # Create test data with None description
        repo = Repository(
            id=12345,
            name="test-repo",
            full_name="test-owner/test-repo",
            owner=RepositoryOwner(login="test-owner"),
            private=False,
            html_url="https://github.com/test-owner/test-repo",
            description=None
        )
        
        # Convert the repository
        result = convert_repository(repo)
        
        # Verify the conversion
        assert result["id"] == 12345
        assert result["name"] == "test-repo"
        assert result["full_name"] == "test-owner/test-repo"
        assert result["owner"] == "test-owner"
        assert result["private"] is False
        assert result["html_url"] == "https://github.com/test-owner/test-repo"
        assert result["description"] is None
