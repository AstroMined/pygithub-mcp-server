"""Unit tests for user converters.

This module tests the conversion functions for GitHub users.
These tests use realistic data structures instead of mocks.
"""

import pytest
from typing import Dict, Any, Optional

from pygithub_mcp_server.converters.users.users import convert_user


# Realistic data fixtures
class RealisticUser:
    """A realistic representation of a PyGithub NamedUser object."""
    
    def __init__(
        self,
        login: str,
        id: int = 1,
        name: Optional[str] = None,
        email: Optional[str] = None,
        bio: Optional[str] = None,
        avatar_url: str = "https://github.com/images/error/octocat_happy.gif",
        html_url: str = "https://github.com/octocat",
        type: str = "User",
        site_admin: bool = False,
    ):
        self.login = login
        self.id = id
        self.name = name
        self.email = email
        self.bio = bio
        self.avatar_url = avatar_url
        self.html_url = html_url
        self.type = type
        self.site_admin = site_admin


class TestConvertUser:
    """Tests for convert_user function."""
    
    def test_convert_user_full(self):
        """Test conversion of a user with all attributes."""
        # Create a realistic user with all attributes
        user = RealisticUser(
            login="testuser",
            id=1001,
            name="Test User",
            email="test@example.com",
            bio="This is a test user",
            avatar_url="https://example.com/avatar.png",
            html_url="https://github.com/testuser",
            type="User",
            site_admin=False
        )
        
        # Convert the user
        result = convert_user(user)
        
        # Verify
        assert result["login"] == "testuser"
        assert result["id"] == 1001
        assert result["type"] == "User"
        assert result["site_admin"] is False
    
    def test_convert_user_minimal(self):
        """Test conversion of a user with minimal attributes."""
        # Create a realistic user with minimal attributes
        user = RealisticUser(
            login="testuser"
        )
        
        # Convert the user
        result = convert_user(user)
        
        # Verify
        assert result["login"] == "testuser"
        assert result["id"] == 1
        assert result["type"] == "User"
        assert result["site_admin"] is False
    
    def test_convert_organization(self):
        """Test conversion of an organization user."""
        # Create a realistic organization
        org = RealisticUser(
            login="testorg",
            id=2001,
            name="Test Organization",
            email="org@example.com",
            bio="This is a test organization",
            avatar_url="https://example.com/org-avatar.png",
            html_url="https://github.com/testorg",
            type="Organization",
            site_admin=False
        )
        
        # Convert the organization
        result = convert_user(org)
        
        # Verify
        assert result["login"] == "testorg"
        assert result["id"] == 2001
        assert result["type"] == "Organization"
        assert result["site_admin"] is False
    
    def test_convert_site_admin(self):
        """Test conversion of a site admin user."""
        # Create a realistic site admin user
        admin = RealisticUser(
            login="admin",
            id=3001,
            name="Admin User",
            email="admin@example.com",
            bio="Site administrator",
            avatar_url="https://example.com/admin-avatar.png",
            html_url="https://github.com/admin",
            type="User",
            site_admin=True
        )
        
        # Convert the admin user
        result = convert_user(admin)
        
        # Verify
        assert result["login"] == "admin"
        assert result["id"] == 3001
        assert result["type"] == "User"
        assert result["site_admin"] is True
    
    def test_convert_user_none(self):
        """Test conversion of a None user."""
        # Convert None
        result = convert_user(None)
        
        # Verify
        assert result is None
