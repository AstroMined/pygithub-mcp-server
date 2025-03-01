"""Unit tests for issue converters.

This module tests the conversion functions for GitHub issues.
These tests use realistic data structures instead of mocks.
"""

import pytest
from datetime import datetime, timezone
from typing import Dict, Any, List

from pygithub_mcp_server.converters.issues.issues import (
    convert_issue,
    convert_issue_list,
    convert_label,
    convert_milestone,
)


# Realistic data fixtures
class RealisticLabel:
    """A realistic representation of a PyGithub Label object."""
    
    def __init__(self, name: str, color: str, description: str = None, id: int = 1):
        self.name = name
        self.color = color
        self.description = description
        self.id = id


class RealisticMilestone:
    """A realistic representation of a PyGithub Milestone object."""
    
    def __init__(
        self,
        number: int,
        title: str,
        state: str = "open",
        description: str = None,
        id: int = 1,
        created_at: datetime = None,
        updated_at: datetime = None,
        due_on: datetime = None,
    ):
        self.number = number
        self.title = title
        self.state = state
        self.description = description
        self.id = id
        self.created_at = created_at or datetime(2025, 2, 1, 10, 0, 0, tzinfo=timezone.utc)
        self.updated_at = updated_at or datetime(2025, 2, 1, 11, 0, 0, tzinfo=timezone.utc)
        self.due_on = due_on


class RealisticUser:
    """A realistic representation of a PyGithub NamedUser object."""
    
    def __init__(
        self,
        login: str,
        id: int = 1,
        type: str = "User",
        site_admin: bool = False,
    ):
        self.login = login
        self.id = id
        self.type = type
        self.site_admin = site_admin


class RealisticRepository:
    """A realistic representation of a PyGithub Repository object."""
    
    def __init__(self, name: str, owner_login: str):
        self.name = name
        self.full_name = f"{owner_login}/{name}"
        self.owner = RealisticUser(login=owner_login)


class RealisticIssue:
    """A realistic representation of a PyGithub Issue object."""
    
    def __init__(
        self,
        number: int,
        title: str,
        state: str = "open",
        body: str = None,
        id: int = 1,
        state_reason: str = None,
        locked: bool = False,
        active_lock_reason: str = None,
        comments: int = 0,
        created_at: datetime = None,
        updated_at: datetime = None,
        closed_at: datetime = None,
        author_association: str = "CONTRIBUTOR",
        user: RealisticUser = None,
        assignee: RealisticUser = None,
        assignees: List[RealisticUser] = None,
        milestone: RealisticMilestone = None,
        labels: List[RealisticLabel] = None,
        url: str = "https://api.github.com/repos/owner/repo/issues/1",
        html_url: str = "https://github.com/owner/repo/issues/1",
        repository: RealisticRepository = None,
    ):
        self.number = number
        self.title = title
        self.state = state
        self.body = body
        self.id = id
        self.state_reason = state_reason
        self.locked = locked
        self.active_lock_reason = active_lock_reason
        self.comments = comments
        self.created_at = created_at or datetime(2025, 3, 1, 10, 0, 0, tzinfo=timezone.utc)
        self.updated_at = updated_at or datetime(2025, 3, 1, 11, 0, 0, tzinfo=timezone.utc)
        self.closed_at = closed_at
        self.author_association = author_association
        self.user = user or RealisticUser(login="testuser")
        self.assignee = assignee
        self.assignees = assignees or []
        self.milestone = milestone
        self.labels = labels or []
        self.url = url
        self.html_url = html_url
        self.repository = repository or RealisticRepository(name="repo", owner_login="owner")


class TestConvertLabel:
    """Tests for convert_label function."""
    
    def test_convert_label_full(self):
        """Test conversion of a label with all attributes."""
        # Create a realistic label
        label = RealisticLabel(
            name="bug",
            color="ff0000",
            description="Bug report",
            id=123
        )
        
        # Convert the label
        result = convert_label(label)
        
        # Verify
        assert result["name"] == "bug"
        assert result["color"] == "ff0000"
        assert result["description"] == "Bug report"
        assert result["id"] == 123
    
    def test_convert_label_minimal(self):
        """Test conversion of a label with minimal attributes."""
        # Create a realistic label with minimal attributes
        label = RealisticLabel(
            name="bug",
            color="ff0000"
        )
        
        # Convert the label
        result = convert_label(label)
        
        # Verify
        assert result["name"] == "bug"
        assert result["color"] == "ff0000"
        assert result["description"] is None
        assert result["id"] == 1


class TestConvertMilestone:
    """Tests for convert_milestone function."""
    
    def test_convert_milestone_full(self):
        """Test conversion of a milestone with all attributes."""
        # Create a realistic milestone
        created_at = datetime(2025, 2, 1, 10, 0, 0, tzinfo=timezone.utc)
        updated_at = datetime(2025, 2, 1, 11, 0, 0, tzinfo=timezone.utc)
        due_on = datetime(2025, 4, 1, 0, 0, 0, tzinfo=timezone.utc)
        
        milestone = RealisticMilestone(
            number=1,
            title="v1.0",
            description="First release",
            state="open",
            id=42,
            created_at=created_at,
            updated_at=updated_at,
            due_on=due_on
        )
        
        # Convert the milestone
        result = convert_milestone(milestone)
        
        # Verify
        assert result["number"] == 1
        assert result["title"] == "v1.0"
        assert result["description"] == "First release"
        assert result["state"] == "open"
        assert result["id"] == 42
        assert result["created_at"] == "2025-02-01T10:00:00+00:00"
        assert result["updated_at"] == "2025-02-01T11:00:00+00:00"
        assert result["due_on"] == "2025-04-01T00:00:00+00:00"
    
    def test_convert_milestone_minimal(self):
        """Test conversion of a milestone with minimal attributes."""
        # Create a realistic milestone with minimal attributes
        milestone = RealisticMilestone(
            number=1,
            title="v1.0"
        )
        
        # Convert the milestone
        result = convert_milestone(milestone)
        
        # Verify
        assert result["number"] == 1
        assert result["title"] == "v1.0"
        assert result["description"] is None
        assert result["state"] == "open"
        assert result["id"] == 1
        assert "created_at" in result
        assert "updated_at" in result
        assert "due_on" in result
    
    def test_convert_milestone_none(self):
        """Test conversion of a None milestone."""
        # Convert None
        result = convert_milestone(None)
        
        # Verify
        assert result is None


class TestConvertIssue:
    """Tests for convert_issue function."""
    
    def test_convert_issue_full(self):
        """Test conversion of a complete issue object."""
        # Create realistic labels
        label1 = RealisticLabel(
            name="bug",
            color="ff0000",
            description="Bug report",
            id=101
        )
        
        label2 = RealisticLabel(
            name="enhancement",
            color="00ff00",
            description="Feature request",
            id=102
        )
        
        # Create realistic milestone
        milestone = RealisticMilestone(
            number=1,
            title="v1.0",
            description="First release",
            state="open",
            id=42,
            created_at=datetime(2025, 2, 1, 10, 0, 0, tzinfo=timezone.utc),
            updated_at=datetime(2025, 2, 1, 11, 0, 0, tzinfo=timezone.utc),
            due_on=datetime(2025, 4, 1, 0, 0, 0, tzinfo=timezone.utc)
        )
        
        # Create realistic users
        user = RealisticUser(login="testuser", id=1001)
        assignee1 = RealisticUser(login="user1", id=1002)
        assignee2 = RealisticUser(login="user2", id=1003)
        
        # Create a realistic issue with all attributes
        issue = RealisticIssue(
            number=42,
            title="Test Issue",
            body="This is a test issue",
            state="open",
            id=2001,
            locked=False,
            comments=5,
            created_at=datetime(2025, 3, 1, 10, 0, 0, tzinfo=timezone.utc),
            updated_at=datetime(2025, 3, 1, 11, 0, 0, tzinfo=timezone.utc),
            closed_at=None,
            user=user,
            assignee=assignee1,
            assignees=[assignee1, assignee2],
            milestone=milestone,
            labels=[label1, label2],
            repository=RealisticRepository(name="testrepo", owner_login="testorg")
        )
        
        # Convert the issue
        result = convert_issue(issue)
        
        # Verify basic properties
        assert result["issue_number"] == 42
        assert result["title"] == "Test Issue"
        assert result["body"] == "This is a test issue"
        assert result["state"] == "open"
        assert result["id"] == 2001
        assert result["comments"] == 5
        assert result["created_at"] == "2025-03-01T10:00:00+00:00"
        assert result["updated_at"] == "2025-03-01T11:00:00+00:00"
        assert result["closed_at"] is None
        
        # Verify labels
        assert len(result["labels"]) == 2
        assert result["labels"][0]["name"] == "bug"
        assert result["labels"][0]["color"] == "ff0000"
        assert result["labels"][0]["description"] == "Bug report"
        assert result["labels"][1]["name"] == "enhancement"
        assert result["labels"][1]["color"] == "00ff00"
        assert result["labels"][1]["description"] == "Feature request"
        
        # Verify assignees
        assert len(result["assignees"]) == 2
        assert result["assignees"][0]["login"] == "user1"
        assert result["assignees"][1]["login"] == "user2"
        
        # Verify milestone
        assert result["milestone"]["number"] == 1
        assert result["milestone"]["title"] == "v1.0"
        assert result["milestone"]["description"] == "First release"
        assert result["milestone"]["state"] == "open"
        
        # Verify repository
        assert result["repository"]["full_name"] == "testorg/testrepo"
        assert result["repository"]["name"] == "testrepo"
        assert result["repository"]["owner"] == "testorg"
    
    def test_convert_issue_minimal(self):
        """Test conversion of a minimal issue object."""
        # Create a realistic issue with minimal attributes
        issue = RealisticIssue(
            number=42,
            title="Test Issue"
        )
        
        # Convert the issue
        result = convert_issue(issue)
        
        # Verify basic properties
        assert result["issue_number"] == 42
        assert result["title"] == "Test Issue"
        assert result["body"] is None
        assert result["state"] == "open"
        
        # Verify empty collections
        assert len(result["labels"]) == 0
        assert len(result["assignees"]) == 0
        assert result["milestone"] is None
    
    def test_convert_issue_closed(self):
        """Test conversion of a closed issue."""
        # Create a realistic closed issue
        closed_at = datetime(2025, 3, 1, 12, 0, 0, tzinfo=timezone.utc)
        issue = RealisticIssue(
            number=42,
            title="Test Issue",
            body="This is a test issue",
            state="closed",
            closed_at=closed_at
        )
        
        # Convert the issue
        result = convert_issue(issue)
        
        # Verify closed state and closed_at
        assert result["state"] == "closed"
        assert result["closed_at"] == "2025-03-01T12:00:00+00:00"


class TestConvertIssueList:
    """Tests for convert_issue_list function."""
    
    def test_convert_empty_list(self):
        """Test conversion of an empty issue list."""
        result = convert_issue_list([])
        assert len(result) == 0
    
    def test_convert_issue_list(self):
        """Test conversion of a list of issues."""
        # Create realistic issues
        issue1 = RealisticIssue(
            number=1,
            title="Issue 1",
            body="Body 1",
            state="open",
            id=1001
        )
        
        issue2 = RealisticIssue(
            number=2,
            title="Issue 2",
            body="Body 2",
            state="closed",
            id=1002,
            closed_at=datetime(2025, 3, 2, 12, 0, 0, tzinfo=timezone.utc)
        )
        
        # Convert the list
        result = convert_issue_list([issue1, issue2])
        
        # Verify
        assert len(result) == 2
        assert result[0]["issue_number"] == 1
        assert result[0]["title"] == "Issue 1"
        assert result[0]["state"] == "open"
        assert result[1]["issue_number"] == 2
        assert result[1]["title"] == "Issue 2"
        assert result[1]["state"] == "closed"
