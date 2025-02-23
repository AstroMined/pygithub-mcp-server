# PyGithub MCP Server

[![smithery badge](https://smithery.ai/badge/@AstroMined/pygithub-mcp-server)](https://smithery.ai/server/@AstroMined/pygithub-mcp-server)

A Model Context Protocol server that provides tools for interacting with the GitHub API through PyGithub. This server enables AI assistants to perform GitHub operations like managing issues, repositories, and pull requests.

## Features

- Complete GitHub Issue Management:
  - Create and update issues
  - Get issue details and list repository issues
  - Add, list, update, and delete comments
  - Manage issue labels
  - Handle assignees and milestones
- Smart Parameter Handling:
  - Dynamic kwargs building for optional parameters
  - Proper type conversion for GitHub objects
  - Validation for all input parameters
  - Clear error messages for invalid inputs
- Robust Implementation:
  - Object-oriented GitHub API interactions via PyGithub
  - Centralized GitHub client management
  - Proper error handling and rate limiting
  - Clean API abstraction through MCP tools
  - Comprehensive pagination support
  - Detailed logging for debugging

## Documentation

Comprehensive guides are available in the docs/guides directory:

- error-handling.md: Error types, handling patterns, and best practices
- security.md: Authentication, access control, and content security
- tool-reference.md: Detailed tool documentation with examples

See these guides for detailed information about using the PyGithub MCP Server.

## Usage Examples

### Issue Operations

1. Creating an Issue
```json
{
  "owner": "username",
  "repo": "repository",
  "title": "Issue Title",
  "body": "Issue description",
  "assignees": ["username1", "username2"],
  "labels": ["bug", "help wanted"],
  "milestone": 1
}
```

2. Getting Issue Details
```json
{
  "owner": "username",
  "repo": "repository",
  "issue_number": 1
}
```

3. Updating an Issue
```json
{
  "owner": "username",
  "repo": "repository",
  "issue_number": 1,
  "title": "Updated Title",
  "body": "Updated description",
  "state": "closed",
  "labels": ["bug", "wontfix"]
}
```

### Comment Operations

1. Adding a Comment
```json
{
  "owner": "username",
  "repo": "repository",
  "issue_number": 1,
  "body": "This is a comment"
}
```

2. Listing Comments
```json
{
  "owner": "username",
  "repo": "repository",
  "issue_number": 1,
  "per_page": 10
}
```

3. Updating a Comment
```json
{
  "owner": "username",
  "repo": "repository",
  "issue_number": 1,
  "comment_id": 123456789,
  "body": "Updated comment text"
}
```

### Label Operations

1. Adding Labels
```json
{
  "owner": "username",
  "repo": "repository",
  "issue_number": 1,
  "labels": ["enhancement", "help wanted"]
}
```

2. Removing a Label
```json
{
  "owner": "username",
  "repo": "repository",
  "issue_number": 1,
  "label": "enhancement"
}
```

All operations handle optional parameters intelligently:
- Only includes provided parameters in API calls
- Converts primitive types to GitHub objects (e.g., milestone number to Milestone object)
- Provides clear error messages for invalid parameters
- Handles pagination automatically where applicable

## Installation

### Installing via Smithery

To install PyGithub MCP Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@AstroMined/pygithub-mcp-server):

```bash
npx -y @smithery/cli install @AstroMined/pygithub-mcp-server --client claude
```

### Manual Installation

1. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
uv pip install -e .
```

## Configuration

1. Add the server to your MCP settings (e.g., `claude_desktop_config.json` or `cline_mcp_settings.json`):
```json
{
  "mcpServers": {
    "github": {
      "command": "/path/to/repo/.venv/bin/python",
      "args": ["-m", "pygithub_mcp_server"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token-here"
      }
    }
  }
}
```

## Development

### Testing
The project includes a comprehensive test suite:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov

# Run specific test file
pytest tests/test_operations/test_issues.py

# Run tests matching a pattern
pytest -k "test_create_issue"
```

Note: Many tests are currently failing and under investigation. This is a known issue being actively worked on.

### Testing with MCP Inspector
Test MCP tools during development using the MCP Inspector:
```bash
source .venv/bin/activate  # Ensure venv is activated
npx @modelcontextprotocol/inspector -e GITHUB_PERSONAL_ACCESS_TOKEN=your-token-here uv run pygithub-mcp-server
```

Use the MCP Inspector's Web UI to:
- Experiment with available tools
- Test with real GitHub repositories
- Verify success and error cases
- Document working payloads

### Project Structure

```
tests/
├── conftest.py          # Shared test fixtures
├── test_converters.py   # Object conversion tests
├── test_error_handling.py # Error handling tests
├── test_github_client.py # Client tests
└── test_operations/     # Operation-specific tests
    └── test_issues.py   # Issue operation tests
```


```
src/
└── pygithub_mcp_server/
    ├── __init__.py
    ├── __main__.py
    ├── server.py
    ├── common/
    │   ├── __init__.py
    │   ├── errors.py
    │   ├── github.py      # GitHub client singleton
    │   ├── converters.py  # Object conversion utilities
    │   ├── types.py
    │   ├── utils.py
    │   └── version.py
    └── operations/
        ├── __init__.py
        └── issues.py
```

### Troubleshooting

1. Server fails to start:
   - Verify venv Python path in MCP settings
   - Ensure all requirements are installed in venv
   - Check GITHUB_PERSONAL_ACCESS_TOKEN is set and valid

2. Build errors:
   - Use --no-build-isolation flag with uv build
   - Ensure Python 3.10+ is being used
   - Verify all dependencies are installed

3. GitHub API errors:
   - Check token permissions and validity
   - Review pygithub_mcp_server.log for detailed error traces
   - Verify rate limits haven't been exceeded

## Dependencies
- Python 3.10+
- MCP Python SDK
- Pydantic
- PyGithub
- UV package manager

## License

MIT
