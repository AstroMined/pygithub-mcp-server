#!/usr/bin/env python3
"""
Test Generator for PyGithub MCP Server

This script generates standardized test files for new PyGithub MCP Server tools,
following the project's testing patterns. It creates both unit and integration
tests that use dataclasses instead of mocks, aligned with ADR-002 principles.

Usage:
    python scripts/generate_tool_tests.py --module repositories --tool-name get_repository

Options:
    --module MODULE      Tool module name (e.g., issues, repositories)
    --tool-name NAME     Tool name in CamelCase (e.g., GetRepository)
    --output-dir DIR     Output directory for test files (default: tests/)
    --schema-module MOD  Schema module name (default: same as tool module)
    --schema-name NAME   Schema class name (default: derived from tool name + 'Params')
    --overwrite          Overwrite existing test files (default: ask)
"""

import os
import re
import sys
import inspect
import argparse
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, List


TEMPLATES = {
    "unit_test": """
import pytest
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from pygithub_mcp_server.tools.{module} import {tool_name}
from pygithub_mcp_server.errors import GitHubError
from pygithub_mcp_server.schemas.{schema_module} import {schema_name}

# Dataclasses representing PyGithub objects
@dataclass
class RepositoryOwner:
    login: str
    id: int = 12345
    html_url: str = "https://github.com/test-owner"
    
@dataclass
class Repository:
    id: int
    name: str
    full_name: str
    owner: RepositoryOwner
    private: bool = False
    html_url: str = "https://github.com/test-owner/test-repo"
    description: Optional[str] = None

{additional_dataclasses}

class Test{tool_name}:
    """Test suite for {tool_name} tool."""
    
    def test_{tool_func}_success(self):
        """Test successful {tool_name} execution using dataclasses."""
        # Create test data using dataclasses
        owner = RepositoryOwner(login="test-owner")
        repo = Repository(
            id=98765,
            name="test-repo",
            full_name="test-owner/test-repo",
            owner=owner
        )
        
        # Test parameters
        params = {{"params": {params}}}
        
        # Patch PyGithub interactions to return our dataclass objects
        with pytest.MonkeyPatch.context() as monkeypatch:
            # Configure to return our test objects
            monkeypatch.setattr(
                "pygithub_mcp_server.client.GitHubClient.get_instance().get_repo",
                lambda _: repo
            )
            
            # Execute the tool
            result = {tool_func}(params)
            
            # Verify success result
            assert not result.get("is_error", False)
            assert isinstance(result["content"], list)
            assert result["content"][0]["type"] == "text"
            
            # Additional assertions specific to this tool
            # TODO: Add assertions based on expected return values
    
    def test_{tool_func}_validation_error(self):
        """Test {tool_name} with validation errors."""
        # Test with invalid parameters
        with pytest.raises(ValueError):
            # This should fail during Pydantic validation
            {schema_name}(**{invalid_params})
        
        # Test the tool itself with invalid parameters
        params = {{"params": {invalid_params}}}
        
        # Execute the tool
        result = {tool_func}(params)
        
        # Verify error result
        assert result.get("is_error", True)
        assert "validation" in result["content"][0]["text"].lower()
    
    def test_{tool_func}_github_error(self):
        """Test {tool_name} with GitHub API errors."""
        # Test parameters
        params = {{"params": {params}}}
        
        # Simulate GitHub API error without mocks
        with pytest.MonkeyPatch.context() as monkeypatch:
            # Configure to raise a GitHub exception
            def raise_github_exception(*args, **kwargs):
                from github import GithubException
                raise GithubException(404, {{"message": "Not Found"}})
                
            monkeypatch.setattr(
                "pygithub_mcp_server.client.GitHubClient.get_instance().get_repo",
                raise_github_exception
            )
            
            # Execute the tool
            result = {tool_func}(params)
            
            # Verify error result
            assert result.get("is_error", True)
            assert "not found" in result["content"][0]["text"].lower()
""",

    "integration_test": """
import pytest
import uuid
from pygithub_mcp_server.tools.{module} import {tool_name}
from pygithub_mcp_server.errors import GitHubError
from pygithub_mcp_server.schemas.{schema_module} import {schema_name}

@pytest.mark.integration
class TestIntegration{tool_name}:
    """Integration tests for {tool_name} tool."""
    
    def test_{tool_func}_integration(self, test_owner, test_repo, test_cleanup):
        """Test {tool_name} with real PyGithub client."""
        # Create a unique identifier for this test
        test_id = str(uuid.uuid4())[:8]
        
        # Test parameters with real repo
        params = {{"params": {integration_params}}}
        
        # Execute the tool with real parameters
        result = {tool_func}(params)
        
        # Verify the tool executed successfully with real data
        assert not result.get("is_error", False)
        assert isinstance(result["content"], list)
        assert "text" in result["content"][0]
        
        # Additional assertions based on the specific tool
        # TODO: Add assertions specific to this tool
    
    def test_{tool_func}_not_found(self):
        """Test {tool_name} with non-existent resources."""
        # Create parameters with non-existent resources
        params = {{"params": {{
            "owner": "non-existent-user-12345",
            "repo": "non-existent-repo-12345"
        }}}}
        
        # Execute the tool
        result = {tool_func}(params)
        
        # Verify error response
        assert result.get("is_error", True)
        assert "not found" in result["content"][0]["text"].lower()
"""
}


# Tool type-specific parameters
TOOL_PARAMS = {
    "repositories": {
        "GetRepository": {
            "params": {"owner": "test-owner", "repo": "test-repo"},
            "invalid_params": {"owner": "", "repo": ""},
            "integration_params": {"owner": "test_owner", "repo": "test_repo"}
        },
        "CreateRepository": {
            "params": {"name": "test-repo", "description": "Test repository", "private": True},
            "invalid_params": {"name": "", "description": 123},
            "integration_params": {"name": "test-repo-{test_id}", "description": "Test repository", "private": True}
        },
        "ForkRepository": {
            "params": {"owner": "test-owner", "repo": "test-repo"},
            "invalid_params": {"owner": "", "repo": ""},
            "integration_params": {"owner": "test_owner", "repo": "test_repo"}
        },
        "SearchRepositories": {
            "params": {"query": "test repo language:python"},
            "invalid_params": {"query": ""},
            "integration_params": {"query": "test repo language:python"}
        },
        "GetFileContents": {
            "params": {"owner": "test-owner", "repo": "test-repo", "path": "README.md"},
            "invalid_params": {"owner": "test-owner", "repo": "test-repo", "path": ""},
            "integration_params": {"owner": "test_owner", "repo": "test_repo", "path": "README.md"}
        },
        "CreateOrUpdateFile": {
            "params": {"owner": "test-owner", "repo": "test-repo", "path": "test.txt", "content": "Test content", "message": "Test commit"},
            "invalid_params": {"owner": "", "repo": "", "path": "", "content": "", "message": ""},
            "integration_params": {"owner": "test_owner", "repo": "test_repo", "path": "test-{test_id}.txt", "content": "Test content", "message": "Test commit"}
        },
        "PushFiles": {
            "params": {"owner": "test-owner", "repo": "test-repo", "branch": "main", "message": "Test commit", "files": [{"path": "test.txt", "content": "Test content"}]},
            "invalid_params": {"owner": "", "repo": "", "branch": "", "message": "", "files": []},
            "integration_params": {"owner": "test_owner", "repo": "test_repo", "branch": "main", "message": "Test commit", "files": [{"path": "test-{test_id}.txt", "content": "Test content"}]}
        },
        "CreateBranch": {
            "params": {"owner": "test-owner", "repo": "test-repo", "branch": "test-branch", "from_branch": "main"},
            "invalid_params": {"owner": "", "repo": "", "branch": ""},
            "integration_params": {"owner": "test_owner", "repo": "test_repo", "branch": "test-branch-{test_id}", "from_branch": "main"}
        },
        "ListCommits": {
            "params": {"owner": "test-owner", "repo": "test-repo"},
            "invalid_params": {"owner": "", "repo": ""},
            "integration_params": {"owner": "test_owner", "repo": "test_repo"}
        }
    },
    "issues": {
        "CreateIssue": {
            "params": {"owner": "test-owner", "repo": "test-repo", "title": "Test Issue"},
            "invalid_params": {"owner": "", "repo": "", "title": ""},
            "integration_params": {"owner": "test_owner", "repo": "test_repo", "title": "Test Issue {test_id}"},
            "additional_dataclasses": """
@dataclass
class Issue:
    number: int = 1
    title: str = "Test Issue"
    body: str = "Test body"
    state: str = "open"
    user: RepositoryOwner = field(default_factory=lambda: RepositoryOwner(login="test-owner"))
    html_url: str = "https://github.com/test-owner/test-repo/issues/1"
"""
        },
        "GetIssue": {
            "params": {"owner": "test-owner", "repo": "test-repo", "issue_number": 1},
            "invalid_params": {"owner": "", "repo": "", "issue_number": -1},
            "integration_params": {"owner": "test_owner", "repo": "test_repo", "issue_number": 1},
            "additional_dataclasses": """
@dataclass
class Issue:
    number: int = 1
    title: str = "Test Issue"
    body: str = "Test body"
    state: str = "open"
    user: RepositoryOwner = field(default_factory=lambda: RepositoryOwner(login="test-owner"))
    html_url: str = "https://github.com/test-owner/test-repo/issues/1"
"""
        },
        "UpdateIssue": {
            "params": {"owner": "test-owner", "repo": "test-repo", "issue_number": 1, "title": "Updated Title"},
            "invalid_params": {"owner": "", "repo": "", "issue_number": -1, "state": "invalid"},
            "integration_params": {"owner": "test_owner", "repo": "test_repo", "issue_number": 1, "title": "Updated Title {test_id}"},
            "additional_dataclasses": """
@dataclass
class Issue:
    number: int = 1
    title: str = "Test Issue"
    body: str = "Test body"
    state: str = "open"
    user: RepositoryOwner = field(default_factory=lambda: RepositoryOwner(login="test-owner"))
    html_url: str = "https://github.com/test-owner/test-repo/issues/1"
    
    def edit(self, **kwargs):
        # Update fields based on kwargs
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
"""
        },
        "ListIssues": {
            "params": {"owner": "test-owner", "repo": "test-repo", "state": "open"},
            "invalid_params": {"owner": "", "repo": "", "state": "invalid"},
            "integration_params": {"owner": "test_owner", "repo": "test_repo", "state": "open"},
            "additional_dataclasses": """
@dataclass
class Issue:
    number: int = 1
    title: str = "Test Issue"
    body: str = "Test body"
    state: str = "open"
    user: RepositoryOwner = field(default_factory=lambda: RepositoryOwner(login="test-owner"))
    html_url: str = "https://github.com/test-owner/test-repo/issues/1"
"""
        },
        "AddIssueComment": {
            "params": {"owner": "test-owner", "repo": "test-repo", "issue_number": 1, "body": "Test comment"},
            "invalid_params": {"owner": "", "repo": "", "issue_number": -1, "body": ""},
            "integration_params": {"owner": "test_owner", "repo": "test_repo", "issue_number": 1, "body": "Test comment {test_id}"},
            "additional_dataclasses": """
@dataclass
class Issue:
    number: int = 1
    title: str = "Test Issue"
    body: str = "Test body"
    state: str = "open"
    user: RepositoryOwner = field(default_factory=lambda: RepositoryOwner(login="test-owner"))
    html_url: str = "https://github.com/test-owner/test-repo/issues/1"
    
    def create_comment(self, body):
        return IssueComment(body=body)

@dataclass
class IssueComment:
    id: int = 12345
    body: str = "Test comment"
    user: RepositoryOwner = field(default_factory=lambda: RepositoryOwner(login="test-owner"))
    created_at: str = "2025-01-01T00:00:00Z"
    updated_at: str = "2025-01-01T00:00:00Z"
    html_url: str = "https://github.com/test-owner/test-repo/issues/1#issuecomment-1"
"""
        }
    }
}

def to_snake_case(name: str) -> str:
    """Convert CamelCase to snake_case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def generate_test_file(
    module: str,
    tool_name: str,
    output_dir: str,
    test_type: str = "unit",
    schema_module: Optional[str] = None,
    schema_name: Optional[str] = None,
    overwrite: bool = False
) -> Tuple[Path, bool]:
    """Generate a test file for the given tool.
    
    Args:
        module: Tool module name (e.g., issues, repositories)
        tool_name: Tool name in CamelCase (e.g., GetRepository)
        output_dir: Output directory for test files
        test_type: Test type (unit or integration)
        schema_module: Schema module name (default: same as tool module)
        schema_name: Schema class name (default: derived from tool name + 'Params')
        overwrite: Whether to overwrite existing files
        
    Returns:
        Tuple of (file path, whether file was created)
    """
    # Derive parameters
    tool_func = to_snake_case(tool_name)
    schema_module = schema_module or module
    schema_name = schema_name or f"{tool_name}Params"
    
    # Get test directory path
    if test_type == "unit":
        test_dir = Path(output_dir) / "unit" / "tools" / module
        template_key = "unit_test"
    else:
        test_dir = Path(output_dir) / "integration" / "tools" / module
        template_key = "integration_test"
    
    # Create test file path
    if test_type == "unit":
        test_file = test_dir / f"test_{tool_func}.py"
    else:
        test_file = test_dir / f"test_{tool_func}_integration.py"
    
    # Check if file exists
    if test_file.exists() and not overwrite:
        user_input = input(f"File {test_file} already exists. Overwrite? (y/n): ")
        if user_input.lower() != 'y':
            print(f"Skipping {test_file}")
            return test_file, False
    
    # Create directory if it doesn't exist
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Get parameters for this tool
    tool_params = TOOL_PARAMS.get(module, {}).get(tool_name, {})
    params = tool_params.get("params", {"param1": "value1", "param2": "value2"})
    invalid_params = tool_params.get("invalid_params", {"param1": "", "param2": ""})
    integration_params = tool_params.get("integration_params", {"owner": "test_owner", "repo": "test_repo"})
    additional_dataclasses = tool_params.get("additional_dataclasses", "")
    
    # Generate content from template
    content = TEMPLATES[template_key].format(
        module=module,
        tool_name=tool_name,
        tool_func=tool_func,
        schema_module=schema_module,
        schema_name=schema_name,
        params=repr(params),
        invalid_params=repr(invalid_params),
        integration_params=repr(integration_params),
        additional_dataclasses=additional_dataclasses
    )
    
    # Write file
    with open(test_file, 'w') as f:
        f.write(content.lstrip())
    
    print(f"Created {test_file}")
    return test_file, True


def main() -> int:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Generate standardized test files for PyGithub MCP Server tools.")
    parser.add_argument("--module", required=True, help="Tool module name (e.g., issues, repositories)")
    parser.add_argument("--tool-name", required=True, help="Tool name in CamelCase (e.g., GetRepository)")
    parser.add_argument("--output-dir", default="tests", help="Output directory for test files")
    parser.add_argument("--schema-module", help="Schema module name (default: same as tool module)")
    parser.add_argument("--schema-name", help="Schema class name (default: derived from tool name + 'Params')")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing test files")
    parser.add_argument("--integration-only", action="store_true", help="Generate only integration tests")
    parser.add_argument("--unit-only", action="store_true", help="Generate only unit tests")
    
    args = parser.parse_args()
    
    # Validate module and tool name
    if args.module not in TOOL_PARAMS:
        available_modules = list(TOOL_PARAMS.keys())
        print(f"Error: Module '{args.module}' not supported. Available modules: {', '.join(available_modules)}")
        print(f"If this is a new module, you need to add it to TOOL_PARAMS in the script.")
        return 1
    
    # Create unit test if not integration-only
    if not args.integration_only:
        unit_file, unit_created = generate_test_file(
            args.module,
            args.tool_name,
            args.output_dir,
            "unit",
            args.schema_module,
            args.schema_name,
            args.overwrite
        )
    
    # Create integration test if not unit-only
    if not args.unit_only:
        integration_file, integration_created = generate_test_file(
            args.module,
            args.tool_name,
            args.output_dir,
            "integration",
            args.schema_module,
            args.schema_name,
            args.overwrite
        )
    
    print("\nNext steps:")
    print("1. Review the generated test files and customize them for your tool")
    print("2. Add specific assertions based on your tool's behavior")
    print("3. Run the tests with 'pytest <test_file>'")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
