# PyGithub API Reference

This directory contains comprehensive documentation for the PyGithub library, organized by major components and functionality.

## Core Components

1. [Authentication](../examples/Authentication.md)
   - Login authentication
   - OAuth token authentication
   - Netrc authentication
   - App authentication
   - App installation authentication
   - App user authentication

2. [Main Class](../examples/MainClass.md)
   - Getting users and organizations
   - Repository access
   - Enterprise features
   - Search functionality

## Repository Operations

1. [Repository Management](../examples/Repository.md)
   - Repository information
   - Content operations
   - Analytics and statistics
   - Repository settings

2. [Branch Operations](../examples/Branch.md)
   - List and get branches
   - Branch protection
   - Status checks
   - HEAD commit access

3. [Commit Operations](../examples/Commit.md)
   - Status checks
   - Commit metadata
   - Commit operations

## Issue Tracking

1. [Issues](../examples/Issue.md)
   - Create and manage issues
   - Issue comments
   - Labels and assignees
   - Bulk operations

2. [Milestones](../examples/Milestone.md)
   - Create milestones
   - Milestone management
   - Progress tracking
   - Issue organization

## Pull Requests

1. [Pull Request Management](../examples/PullRequest.md)
   - Create pull requests
   - PR queries and filters
   - Comments and reviews
   - PR metadata

## Integration

1. [Webhooks](../examples/Webhook.md)
   - Webhook creation
   - Event handling
   - Server implementation
   - Payload processing

## Getting Started

For new users, we recommend starting with:
1. [Introduction](../guides/introduction.md) - Basic setup and authentication
2. [Authentication Examples](../examples/Authentication.md) - Different ways to authenticate
3. [Repository Examples](../examples/Repository.md) - Common repository operations

## Best Practices

When using PyGithub:
- Always handle authentication securely
- Use appropriate error handling
- Consider rate limiting in your applications
- Follow GitHub's API best practices
- Properly close connections when done

## Additional Resources

- [GitHub API Documentation](https://docs.github.com/en/rest)
- [PyGithub Repository](https://github.com/PyGithub/PyGithub)
- [GitHub Developer Guide](https://docs.github.com/en/developers)
