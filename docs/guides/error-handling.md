# Error Handling Guide

## Overview
The PyGithub MCP Server provides consistent error handling across all GitHub operations. This guide explains the error types, their meanings, and how to handle them in your applications.

## Error Types

### GitHubResourceNotFoundError
- Status Code: 404
- Description: Indicates that the requested resource does not exist
- Common Scenarios:
  - Repository not found
  - Issue not found
  - Comment not found
  - Label not found
- Example Message: "Issue not found" or "Repository not found"

### GitHubAuthenticationError
- Status Code: 401
- Description: Authentication failed or token is invalid
- Common Scenarios:
  - Invalid token
  - Token expired
  - Token lacks required scopes
- Example Message: "Authentication failed. Please verify your GitHub token."

### GitHubPermissionError
- Status Code: 403
- Description: User lacks permission for the requested operation
- Common Scenarios:
  - Insufficient repository permissions
  - Organization access required
  - Private repository access denied
- Example Message: "You don't have permission to perform this operation."

### GitHubRateLimitError
- Status Code: 403 (with rate limit headers)
- Description: API rate limit exceeded
- Common Scenarios:
  - Too many requests in a short time
  - Secondary rate limits hit
- Example Message: "API rate limit exceeded. Please wait before making more requests."
- Additional Info: Includes reset time in error object

### GitHubValidationError
- Status Code: 422
- Description: Request validation failed
- Common Scenarios:
  - Invalid field values
  - Missing required fields
  - Invalid state transitions
- Example Message: 
  ```
  Validation failed:
  - title: cannot be blank (missing_field)
  - labels: invalid format (invalid)
  ```

### GitHubError
- Description: Base error type for unhandled or unexpected errors
- Common Scenarios:
  - Network issues
  - Server errors
  - Unexpected API responses
- Example Message: "GitHub API error (HTTP 500): Internal server error"

## Error Handling Best Practices

### 1. Resource Type Detection
The error handler automatically detects the type of resource from the error message or response data:
```python
if "issue" in error_msg.lower():
    resource_type = "issue"
elif "repository" in error_msg.lower():
    resource_type = "repository"
```

### 2. Validation Error Formatting
Validation errors are formatted to provide clear, actionable feedback:
```python
Validation failed:
- field_name: error message (error_code)
- another_field: another message (another_code)
```

### 3. Rate Limit Handling
Rate limit errors include reset time information to help manage API usage:
```python
except GitHubRateLimitError as e:
    print(f"Rate limit exceeded. Resets at: {e.reset_at}")
```

### 4. Error Response Data
All error types include the original response data when available:
```python
except GitHubError as e:
    if e.response:
        print(f"Additional error data: {e.response}")
```

## Common Error Scenarios

### Repository Access
```python
try:
    repo = client.get_repo("owner/repo")
except GitHubResourceNotFoundError:
    print("Repository not found")
except GitHubPermissionError:
    print("No access to repository")
```

### Issue Operations
```python
try:
    issue = get_issue(owner, repo, number)
except GitHubResourceNotFoundError:
    print("Issue does not exist")
except GitHubValidationError as e:
    print(f"Invalid request: {e}")
```

### Label Management
```python
try:
    add_issue_labels(owner, repo, number, labels)
except GitHubPermissionError:
    print("Cannot modify labels")
except GitHubResourceNotFoundError:
    print("Issue or label not found")
```

## Error Logging

All errors are automatically logged with appropriate severity levels:
- Authentication errors: ERROR
- Permission errors: ERROR
- Resource not found: ERROR
- Validation errors: ERROR
- Rate limit errors: ERROR
- Unknown errors: ERROR

Log messages include:
- Error status code
- Error message
- Response data when available
- Stack trace for unexpected errors

## Best Practices

1. Always catch specific error types first:
```python
try:
    # GitHub operation
except GitHubResourceNotFoundError:
    # Handle 404
except GitHubValidationError:
    # Handle validation
except GitHubError:
    # Handle other errors
```

2. Check error response data for additional context:
```python
except GitHubError as e:
    if e.response:
        # Handle with context
    else:
        # Handle generic error
```

3. Log errors appropriately:
```python
except GitHubError as e:
    logger.error(f"GitHub operation failed: {e}")
    # Handle error
```

4. Handle rate limits gracefully:
```python
except GitHubRateLimitError as e:
    wait_time = e.reset_at - datetime.now()
    logger.warning(f"Rate limit hit. Waiting {wait_time}")
