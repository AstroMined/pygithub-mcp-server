# Tool Reference Guide

## Overview
This guide documents all available MCP tools in the PyGithub MCP Server, including their parameters, behavior, and usage examples.

## Issue Management Tools

### create_issue
Creates a new issue in a repository.

```python
{
  "params": {
    "owner": "repository owner",
    "repo": "repository name",
    "title": "issue title",
    "body": "issue description (optional)",
    "assignees": ["username1", "username2"],  # optional
    "labels": ["bug", "help wanted"],  # optional
    "milestone": 1  # optional milestone number
  }
}
```

Notes:
- Title is required, all other fields are optional
- Non-existent labels will be created automatically
- Invalid milestone numbers will raise GitHubValidationError
- HTML content in body will be sanitized and rendered as markdown

### get_issue
Retrieves details about a specific issue.

```python
{
  "params": {
    "owner": "repository owner",
    "repo": "repository name",
    "issue_number": 123
  }
}
```

Notes:
- Returns 404 if issue doesn't exist
- Returns 404 for private repositories without access
- Includes full issue details including comments count

### update_issue
Updates an existing issue.

```python
{
  "params": {
    "owner": "repository owner",
    "repo": "repository name",
    "issue_number": 123,
    "title": "new title (optional)",
    "body": "new description (optional)",
    "state": "open or closed (optional)",
    "labels": ["new", "labels"],  # optional
    "assignees": ["username1"],  # optional
    "milestone": 2  # optional, null to clear
  }
}
```

Notes:
- Only provided fields will be updated
- State must be "open" or "closed"
- Labels replace existing labels
- Assignees replace existing assignees

### list_issues
Lists issues in a repository.

```python
{
  "params": {
    "owner": "repository owner",
    "repo": "repository name",
    "state": "open (default), closed, or all",
    "labels": ["label1", "label2"],  # optional
    "sort": "created, updated, comments",  # optional
    "direction": "asc or desc",  # optional
    "since": "2024-01-01T00:00:00Z",  # optional
    "page": 1,  # optional
    "per_page": 30  # optional, max 100
  }
}
```

Notes:
- Defaults to open issues if state not provided
- Supports pagination for large result sets
- Can filter by multiple labels
- Date filtering uses ISO 8601 format

## Comment Management Tools

### add_issue_comment
Adds a comment to an issue.

```python
{
  "params": {
    "owner": "repository owner",
    "repo": "repository name",
    "issue_number": 123,
    "body": "comment text"
  }
}
```

Notes:
- Body is required
- HTML content will be sanitized
- Markdown formatting supported
- Returns created comment details

### list_issue_comments
Lists comments on an issue.

```python
{
  "params": {
    "owner": "repository owner",
    "repo": "repository name",
    "issue_number": 123,
    "since": "2024-01-01T00:00:00Z",  # optional
    "page": 1,  # optional
    "per_page": 30  # optional, max 100
  }
}
```

Notes:
- Returns all comments if no date filter
- Supports pagination
- Comments ordered by creation date
- Includes user and timestamp details

### update_issue_comment
Updates an existing comment.

```python
{
  "params": {
    "owner": "repository owner",
    "repo": "repository name",
    "issue_number": 123,
    "comment_id": 456,
    "body": "new comment text"
  }
}
```

Notes:
- Body is required
- Returns updated comment details
- Preserves creation timestamp
- Updates modified timestamp

### delete_issue_comment
Deletes a comment from an issue.

```python
{
  "params": {
    "owner": "repository owner",
    "repo": "repository name",
    "issue_number": 123,
    "comment_id": 456
  }
}
```

Notes:
- No response body on success
- Returns 404 if comment doesn't exist
- Requires write permission

## Label Management Tools

### add_issue_labels
Adds labels to an issue.

```python
{
  "params": {
    "owner": "repository owner",
    "repo": "repository name",
    "issue_number": 123,
    "labels": ["label1", "label2"]
  }
}
```

Notes:
- Non-existent labels are created automatically
- New labels use default color (ededed)
- Labels are case-sensitive
- Returns complete list of issue labels

### remove_issue_label
Removes a label from an issue.

```python
{
  "params": {
    "owner": "repository owner",
    "repo": "repository name",
    "issue_number": 123,
    "label": "label-name"
  }
}
```

Notes:
- No response body on success
- Label name is case-sensitive
- Returns 404 if label doesn't exist
- Requires write permission

## Content Handling

### Markdown Support
All text content (issue body, comments) supports GitHub Flavored Markdown:
- Headers (#, ##, ###)
- Lists (-, *, numbers)
- Code blocks (``` or indent)
- Tables (| separator)
- Task lists (- [ ], - [x])
- Mentions (@username)
- References (#123, owner/repo#123)
- Emoji (:smile:)

### HTML Processing
GitHub automatically processes HTML content:
- Most HTML tags removed
- Some tags allowed (details, summary)
- Script tags removed
- Style attributes stripped
- javascript: URLs blocked

### Content Limits
- Issue titles: 150 chars recommended
- Issue body: No strict limit
- Comments: No strict limit
- Labels: 50 chars max
- Milestone titles: 255 chars max

### Special Features
- User mentions trigger notifications
- Issue references auto-link
- Commit SHAs auto-link
- URLs auto-link
- Emoji shortcodes converted
- Task lists rendered as checkboxes

## Error Handling
See error-handling.md for detailed error handling documentation.

## Security Considerations
See security.md for security best practices and considerations.
