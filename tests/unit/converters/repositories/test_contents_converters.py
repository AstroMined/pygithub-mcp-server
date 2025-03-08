"""Unit tests for repository content converters.

These tests verify that content converters correctly transform content data to our schema.
"""

import pytest
from dataclasses import dataclass, field
from typing import Optional

from pygithub_mcp_server.converters.repositories.contents import convert_file_content


@dataclass
class ContentFile:
    """Test content file data class."""
    name: str
    path: str
    sha: str
    size: int
    type: str
    url: str
    html_url: str
    download_url: Optional[str] = None
    encoding: Optional[str] = None
    content: Optional[str] = None


class TestContentConverters:
    """Tests for content converters."""
    
    def test_convert_file_content(self):
        """Test conversion of a ContentFile to our schema."""
        # Create test data using simple data class instead of mock
        content = ContentFile(
            name="test-file.txt",
            path="path/to/test-file.txt",
            sha="abc123def456",
            size=1024,
            type="file",
            encoding="base64",
            content="SGVsbG8gV29ybGQ=",  # base64 for "Hello World"
            url="https://api.github.com/repos/owner/repo/contents/path/to/test-file.txt",
            html_url="https://github.com/owner/repo/blob/main/path/to/test-file.txt",
            download_url="https://raw.githubusercontent.com/owner/repo/main/path/to/test-file.txt"
        )
        
        # Convert the content file
        result = convert_file_content(content)
        
        # Verify the conversion
        assert result["name"] == "test-file.txt"
        assert result["path"] == "path/to/test-file.txt"
        assert result["sha"] == "abc123def456"
        assert result["size"] == 1024
        assert result["type"] == "file"
        assert result["encoding"] == "base64"
        assert result["content"] == "SGVsbG8gV29ybGQ="
        assert result["url"] == "https://api.github.com/repos/owner/repo/contents/path/to/test-file.txt"
        assert result["html_url"] == "https://github.com/owner/repo/blob/main/path/to/test-file.txt"
        assert result["download_url"] == "https://raw.githubusercontent.com/owner/repo/main/path/to/test-file.txt"
    
    def test_convert_directory_content(self):
        """Test conversion of a directory ContentFile (which lacks content/encoding)."""
        # Create test data for a directory using data class
        content = ContentFile(
            name="test-dir",
            path="path/to/test-dir",
            sha="abc123def456",
            size=0,
            type="dir",
            url="https://api.github.com/repos/owner/repo/contents/path/to/test-dir",
            html_url="https://github.com/owner/repo/tree/main/path/to/test-dir",
            download_url=None  # Directories don't have download URLs
            # No encoding or content for directories
        )
        
        # Convert the directory content
        result = convert_file_content(content)
        
        # Verify the conversion
        assert result["name"] == "test-dir"
        assert result["path"] == "path/to/test-dir"
        assert result["sha"] == "abc123def456"
        assert result["size"] == 0
        assert result["type"] == "dir"
        assert result["encoding"] is None
        assert result["content"] is None
        assert result["url"] == "https://api.github.com/repos/owner/repo/contents/path/to/test-dir"
        assert result["html_url"] == "https://github.com/owner/repo/tree/main/path/to/test-dir"
        assert result["download_url"] is None
