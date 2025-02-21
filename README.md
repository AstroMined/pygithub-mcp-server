# GitHub MCP Server

A Model Context Protocol server that provides tools for interacting with the GitHub API. This server enables AI assistants to perform GitHub operations like managing issues, repositories, and pull requests.

## Features

- List, create, update, and manage GitHub issues
- Handle issue comments and labels
- Proper error handling and rate limit management
- Clean API abstraction through MCP tools

## Installation

1. Install dependencies:
```bash
uv sync --dev --all-extras
```

2. Set up environment variables:
```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="your-token-here"
```

## Usage

Run the server:
```bash
uv run github-mcp-server
```

## Development

This project uses:
- Python MCP SDK for server implementation
- Pydantic for data validation
- Requests for GitHub API interaction
- UV for dependency management

### Project Structure

```
src/
└── github_mcp_server/
    ├── __init__.py
    ├── __main__.py
    ├── server.py
    ├── common/
    │   ├── __init__.py
    │   ├── errors.py
    │   ├── types.py
    │   ├── utils.py
    │   └── version.py
    └── operations/
        ├── __init__.py
        └── issues.py
```

### Testing

Run tests with:
```bash
pytest
```

## License

MIT
