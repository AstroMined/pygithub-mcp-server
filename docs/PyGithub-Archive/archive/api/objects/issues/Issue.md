# Issue Object

The Issue object represents a GitHub issue and provides access to all issue-related operations, including comments, labels, assignees, and reactions.

## Getting an Issue

Issues are typically obtained through a Repository object:

```python
# Get specific issue
issue = repo.get_issue(number)

# Get all repository issues
issues = repo.get_issues(state="open")  # or "closed", "all"

# Get issues with filters
issues = repo.get_issues(
    state="open",
    labels=["bug"],
    assignee="username",
    milestone="v1.0",
    sort="created",  # or "updated", "comments"
    direction="desc"
)
```

## Properties

### Basic Information
- `number`: Issue number
- `title`: Issue title
- `body`: Issue description/content
- `state`: Issue state ("open" or "closed")
- `state_reason`: Reason for state (e.g., "completed", "not_planned")
- `locked`: Whether the issue is locked
- `active_lock_reason`: Reason for being locked

### Metadata
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `closed_at`: When the issue was closed
- `comments`: Number of comments
- `url`: API URL for this issue
- `html_url`: Web URL for this issue

### Relationships
- `user`: User who created the issue
- `assignee`: User assigned to the issue (deprecated, use assignees)
- `assignees`: List of users assigned to the issue
- `milestone`: Associated milestone
- `labels`: List of labels
- `repository`: Parent repository

## Methods

### Basic Operations

```python
# Edit issue
issue.edit(
    title="New title",
    body="New description",
    state="closed",  # or "open"
    state_reason="completed",  # or "not_planned"
    assignees=["user1", "user2"],
    milestone=milestone_obj,
    labels=["bug", "high-priority"]
)

# Convert to pull request (if issue was created from PR)
pull_request = issue.as_pull_request()

# Lock/unlock issue
issue.lock("resolved")  # or "off-topic", "too heated", "spam"
issue.unlock()
```

### Comment Management

```python
# Get all comments
comments = issue.get_comments()

# Get comments since a specific date
comments = issue.get_comments(since=datetime(2024, 1, 1))

# Get specific comment
comment = issue.get_comment(comment_id)

# Create comment
comment = issue.create_comment("This is a comment")
```

### Label Management

```python
# Get labels
labels = issue.get_labels()

# Add labels
issue.add_to_labels("bug", "high-priority")

# Remove specific label
issue.remove_from_labels("bug")

# Set labels (replaces all existing labels)
issue.set_labels("bug", "high-priority")

# Remove all labels
issue.delete_labels()
```

### Assignee Management

```python
# Add assignees
issue.add_to_assignees("user1", "user2")

# Remove assignees
issue.remove_from_assignees("user1", "user2")
```

### Reaction Management

```python
# Get reactions
reactions = issue.get_reactions()

# Create reaction
reaction = issue.create_reaction("+1")  # or "-1", "laugh", "confused", "heart", "hooray", "rocket", "eyes"

# Delete reaction
issue.delete_reaction(reaction_id)
```

### Timeline Events

```python
# Get timeline of issue events
timeline = issue.get_timeline()

# Get issue events
events = issue.get_events()
```

## Common Patterns

### Creating a Bug Report

```python
issue = repo.create_issue(
    title="Bug: Application crashes on startup",
    body="""
## Description
Application crashes immediately after launch

## Steps to Reproduce
1. Launch application
2. Observe immediate crash

## Expected Behavior
Application should start normally

## Actual Behavior
Application crashes with error XYZ

## System Information
- OS: Windows 10
- Version: 1.2.3
""",
    labels=["bug", "high-priority"],
    assignees=["developer1"],
    milestone=version_milestone
)
```

### Managing Issue Workflow

```python
# Assign issue to sprint milestone
issue.edit(milestone=sprint_milestone)

# Add labels for tracking
issue.add_to_labels("in-progress", "backend")

# Assign to team members
issue.add_to_assignees("developer1", "developer2")

# Add technical details
issue.create_comment("Related to database connection timeout in module XYZ")

# Mark as completed
issue.edit(
    state="closed",
    state_reason="completed"
)
```

### Handling Issue Updates

```python
# Update issue status
issue.edit(
    body=issue.body + "\n\nUpdate: Investigation in progress",
    labels=["bug", "in-progress"]
)

# Add progress update
issue.create_comment("Root cause identified: Connection timeout setting too low")

# Request review
issue.create_comment("@reviewer Please review the proposed solution")
```

## Error Handling

```python
try:
    issue.edit(state="closed")
except github.GithubException as e:
    if e.status == 404:
        print("Issue not found")
    elif e.status == 403:
        print("Permission denied")
    else:
        print(f"Error: {e.status} - {e.data}")
```

## Best Practices

1. Issue Creation
   - Use clear, descriptive titles
   - Provide detailed descriptions
   - Include steps to reproduce for bugs
   - Add appropriate labels
   - Assign to relevant milestone

2. Issue Management
   - Keep descriptions up to date
   - Use labels for categorization
   - Assign issues appropriately
   - Close resolved issues promptly
   - Document resolution in comments

3. Comments
   - Keep comments focused and constructive
   - Use markdown for formatting
   - Reference related issues/PRs
   - Update status regularly

4. Labels
   - Use consistent labeling scheme
   - Maintain reasonable number of labels
   - Review and update labels regularly
   - Use color coding effectively

5. Workflow
   - Follow team's issue workflow
   - Update status appropriately
   - Link related issues
   - Use milestones for tracking
   - Keep timeline events clear
