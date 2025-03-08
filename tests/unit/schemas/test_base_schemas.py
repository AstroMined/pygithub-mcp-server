"""Tests for base schema models.

This module tests the base schema models used across multiple domains.
"""

import pytest
from pydantic import ValidationError

from pygithub_mcp_server.schemas.base import RepositoryRef, FileContent


class TestRepositoryRef:
    """Tests for the RepositoryRef schema."""

    def test_valid_data(self, valid_repository_ref_data):
        """Test that valid data passes validation."""
        repo_ref = RepositoryRef(**valid_repository_ref_data)
        assert repo_ref.owner == valid_repository_ref_data["owner"]
        assert repo_ref.repo == valid_repository_ref_data["repo"]

    def test_minimal_valid_data(self):
        """Test with minimal valid data."""
        repo_ref = RepositoryRef(owner="octocat", repo="hello-world")
        assert repo_ref.owner == "octocat"
        assert repo_ref.repo == "hello-world"

    def test_missing_required_fields(self):
        """Test that missing required fields raise validation errors."""
        # Missing owner
        with pytest.raises(ValidationError) as exc_info:
            RepositoryRef(repo="hello-world")
        assert "owner" in str(exc_info.value).lower()
        
        # Missing repo
        with pytest.raises(ValidationError) as exc_info:
            RepositoryRef(owner="octocat")
        assert "repo" in str(exc_info.value).lower()

    def test_invalid_field_types(self):
        """Test that invalid field types raise validation errors."""
        # Invalid owner type
        with pytest.raises(ValidationError) as exc_info:
            RepositoryRef(owner=123, repo="hello-world")
        assert "owner" in str(exc_info.value).lower()
        
        # Invalid repo type
        with pytest.raises(ValidationError) as exc_info:
            RepositoryRef(owner="octocat", repo=123)
        assert "repo" in str(exc_info.value).lower()

    def test_empty_strings(self):
        """Test that empty strings raise validation errors."""
        # Empty owner
        with pytest.raises(ValidationError) as exc_info:
            RepositoryRef(owner="", repo="hello-world")
        assert "owner cannot be empty" in str(exc_info.value).lower()
        
        # Empty repo
        with pytest.raises(ValidationError) as exc_info:
            RepositoryRef(owner="octocat", repo="")
        assert "repo cannot be empty" in str(exc_info.value).lower()
        
        # Whitespace-only owner
        with pytest.raises(ValidationError) as exc_info:
            RepositoryRef(owner="   ", repo="hello-world")
        assert "owner cannot be empty" in str(exc_info.value).lower()
        
        # Whitespace-only repo
        with pytest.raises(ValidationError) as exc_info:
            RepositoryRef(owner="octocat", repo="  ")
        assert "repo cannot be empty" in str(exc_info.value).lower()

    def test_none_values(self):
        """Test that None values raise validation errors."""
        # None owner
        with pytest.raises(ValidationError) as exc_info:
            RepositoryRef(owner=None, repo="hello-world")
        assert "owner" in str(exc_info.value).lower()
        
        # None repo
        with pytest.raises(ValidationError) as exc_info:
            RepositoryRef(owner="octocat", repo=None)
        assert "repo" in str(exc_info.value).lower()

    def test_extra_fields(self):
        """Test that extra fields are ignored."""
        repo_ref = RepositoryRef(
            owner="octocat",
            repo="hello-world",
            extra_field="ignored"
        )
        assert repo_ref.owner == "octocat"
        assert repo_ref.repo == "hello-world"
        assert not hasattr(repo_ref, "extra_field")


class TestFileContent:
    """Tests for the FileContent schema."""

    def test_valid_data(self, valid_file_content_data):
        """Test that valid data passes validation."""
        file_content = FileContent(**valid_file_content_data)
        assert file_content.path == valid_file_content_data["path"]
        assert file_content.content == valid_file_content_data["content"]

    def test_minimal_valid_data(self):
        """Test with minimal valid data."""
        file_content = FileContent(path="README.md", content="# Hello World")
        assert file_content.path == "README.md"
        assert file_content.content == "# Hello World"

    def test_missing_required_fields(self):
        """Test that missing required fields raise validation errors."""
        # Missing path
        with pytest.raises(ValidationError) as exc_info:
            FileContent(content="# Hello World")
        assert "path" in str(exc_info.value).lower()
        
        # Missing content
        with pytest.raises(ValidationError) as exc_info:
            FileContent(path="README.md")
        assert "content" in str(exc_info.value).lower()

    def test_invalid_field_types(self):
        """Test that invalid field types raise validation errors."""
        # Invalid path type
        with pytest.raises(ValidationError) as exc_info:
            FileContent(path=123, content="# Hello World")
        assert "path" in str(exc_info.value).lower()
        
        # Invalid content type
        with pytest.raises(ValidationError) as exc_info:
            FileContent(path="README.md", content=123)
        assert "content" in str(exc_info.value).lower()

    def test_empty_strings(self):
        """Test behavior with empty strings."""
        # Empty path - should raise error
        with pytest.raises(ValidationError) as exc_info:
            FileContent(path="", content="# Hello World")
        assert "path cannot be empty" in str(exc_info.value).lower()
        
        # Whitespace-only path - should raise error
        with pytest.raises(ValidationError) as exc_info:
            FileContent(path="   ", content="# Hello World")
        assert "path cannot be empty" in str(exc_info.value).lower()
        
        # Empty content - should be valid (empty files are allowed)
        file_content = FileContent(path="README.md", content="")
        assert file_content.path == "README.md"
        assert file_content.content == ""

    def test_none_values(self):
        """Test that None values raise validation errors."""
        # None path
        with pytest.raises(ValidationError) as exc_info:
            FileContent(path=None, content="# Hello World")
        assert "path" in str(exc_info.value).lower()
        
        # None content
        with pytest.raises(ValidationError) as exc_info:
            FileContent(path="README.md", content=None)
        assert "content" in str(exc_info.value).lower()

    def test_extra_fields(self):
        """Test that extra fields are ignored."""
        file_content = FileContent(
            path="README.md",
            content="# Hello World",
            extra_field="ignored"
        )
        assert file_content.path == "README.md"
        assert file_content.content == "# Hello World"
        assert not hasattr(file_content, "extra_field")

    def test_binary_content(self):
        """Test with binary content encoded as base64 string."""
        # Base64 encoded content should be valid
        file_content = FileContent(
            path="image.png",
            content="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
        )
        assert file_content.path == "image.png"
        assert file_content.content.startswith("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ")
