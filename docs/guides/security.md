# Security Guide

## Overview
This guide documents important security considerations when using the PyGithub MCP Server, including authentication, access control, and content handling.

## Authentication

### Token Security
- Personal Access Tokens (PATs) are used for authentication
- Tokens must be kept secure and never committed to source control
- Set token via GITHUB_PERSONAL_ACCESS_TOKEN environment variable
- Use fine-grained tokens with minimal required permissions

### Token Permissions
- Read access required for viewing issues, comments
- Write access required for creating/updating issues
- Admin access required for managing repository settings
- Token permissions are validated by GitHub API

## Access Control

### Repository Access
- Private repositories return 404 "Not Found" instead of 401/403
  - This is a GitHub security feature to prevent repository enumeration
  - Same response whether repository doesn't exist or user lacks access
  - Helps prevent information disclosure about private repositories

### Permission Levels
- Repository permissions determine available operations
- Operations fail with GitHubPermissionError if insufficient permissions
- Permission hierarchy:
  - Read: View issues, comments, labels
  - Write: Create/update issues, add labels
  - Admin: Manage repository settings

### Rate Limiting
- Rate limits help prevent abuse
- Limits tracked per token/IP
- Secondary rate limits may apply
- Rate limit errors include reset time
- Consider implementing retry logic with backoff

## Content Security

### Content Sanitization
- GitHub automatically sanitizes HTML content
- Script tags are removed
- javascript: URLs are blocked
- HTML is rendered as markdown
- Content length limits enforced

### Input Validation
- Title length should be reasonable (recommended: 150 chars max)
- Labels are case-sensitive
- Milestone numbers must be valid
- Invalid input results in GitHubValidationError

### Content Processing
- Markdown rendering handled by GitHub
- Image references preserved but sanitized
- Links validated and sanitized
- Code blocks preserved and syntax-highlighted

## Best Practices

### Token Management
```python
# Set token securely via environment
token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
if not token:
    raise GitHubError("Token not configured")
```

### Permission Checking
```python
try:
    # Attempt operation
    repo.create_issue(title="Test")
except GitHubPermissionError:
    # Handle permission denied
    logger.error("Insufficient permissions")
```

### Content Handling
```python
# Content is automatically sanitized
body = """
<script>alert('xss')</script>
# Markdown heading
```code block```
"""
# GitHub will sanitize HTML and preserve markdown
```

### Rate Limit Handling
```python
try:
    # GitHub operation
except GitHubRateLimitError as e:
    # Wait until reset or use exponential backoff
    logger.warning(f"Rate limited until {e.reset_at}")
```

## Security Recommendations

1. Token Security
   - Use environment variables for tokens
   - Rotate tokens regularly
   - Use fine-grained tokens
   - Monitor token usage

2. Error Handling
   - Don't expose internal errors
   - Log security events
   - Handle rate limits gracefully
   - Validate all input

3. Content Management
   - Trust GitHub's content sanitization
   - Implement reasonable limits
   - Validate input before sending
   - Handle errors appropriately

4. Access Control
   - Request minimal permissions
   - Handle 404s appropriately
   - Check operation permissions
   - Log access attempts

## Common Security Scenarios

### Private Repository Access
```python
try:
    repo = client.get_repo("owner/private-repo")
except GitHubResourceNotFoundError:
    # Could be missing permissions or non-existent
    logger.error("Repository not accessible")
```

### Content Validation
```python
if len(title) > 150:
    raise GitHubValidationError("Title too long")
```

### Rate Limit Management
```python
try:
    result = github_operation()
except GitHubRateLimitError as e:
    wait_seconds = (e.reset_at - datetime.now()).total_seconds()
    if wait_seconds > 0:
        time.sleep(wait_seconds)
```

## Security Logging

Important events to log:
- Authentication failures
- Permission denied errors
- Rate limit hits
- Invalid access attempts
- Content validation failures

Example logging:
```python
# Authentication failure
logger.error("Authentication failed", extra={
    "token_prefix": token[:4] if token else None,
    "error": str(e)
})

# Permission denied
logger.warning("Permission denied", extra={
    "operation": operation_name,
    "resource": resource_id
})

# Rate limit
logger.debug("Rate limit hit", extra={
    "reset_at": e.reset_at,
    "operation": operation_name
})
