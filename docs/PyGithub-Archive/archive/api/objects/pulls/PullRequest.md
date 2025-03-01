# PullRequest Object

The PullRequest object represents a GitHub pull request, which is used to propose changes to a repository and facilitate code review.

## Getting a Pull Request

Pull requests can be accessed through a Repository object:

```python
# Get specific pull request
pull = repo.get_pull(number)

# Get all pull requests
pulls = repo.get_pulls()

# Get pull requests with filters
pulls = repo.get_pulls(
    state="open",  # or "closed", "all"
    sort="created",  # or "updated", "popularity", "long-running"
    direction="desc",  # or "asc"
    base="main",  # filter by base branch
    head="feature"  # filter by head branch
)

# Create pull request
pull = repo.create_pull(
    title="Feature implementation",
    body="Implements new feature X",
    base="main",
    head="feature-branch"
)
```

## Properties

### Basic Information
- `number`: Pull request number
- `title`: Pull request title
- `body`: Pull request description
- `state`: State ("open" or "closed")
- `locked`: Whether the pull request is locked
- `draft`: Whether it's a draft pull request
- `merged`: Whether the pull request has been merged
- `mergeable`: Whether the pull request can be merged
- `mergeable_state`: Detailed merge status
- `merge_commit_sha`: SHA of the merge commit

### Branches
- `base`: Base branch information
- `head`: Head branch information
- `base_ref`: Base branch name
- `head_ref`: Head branch name
- `base_commit`: Base commit SHA
- `head_commit`: Head commit SHA

### Review Information
- `comments`: Number of comments
- `review_comments`: Number of review comments
- `commits`: Number of commits
- `additions`: Number of lines added
- `deletions`: Number of lines deleted
- `changed_files`: Number of files changed

### Timestamps
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `closed_at`: When the pull request was closed
- `merged_at`: When the pull request was merged

### URLs
- `url`: API URL
- `html_url`: Web URL
- `diff_url`: Diff URL
- `patch_url`: Patch URL
- `issue_url`: Related issue URL

### Relationships
- `user`: User who created the pull request
- `assignee`: User assigned (deprecated, use assignees)
- `assignees`: List of assigned users
- `requested_reviewers`: Users requested to review
- `labels`: List of labels
- `milestone`: Associated milestone

## Methods

### Basic Operations

```python
# Edit pull request
pull.edit(
    title="Updated title",
    body="Updated description",
    state="closed",  # or "open"
    base="main",
    maintainer_can_modify=True
)

# Convert to draft
pull.convert_to_draft()

# Mark as ready for review
pull.mark_ready_for_review()
```

### Review Management

```python
# Create review
review = pull.create_review(
    body="Looks good!",
    event="APPROVE"  # or "REQUEST_CHANGES", "COMMENT"
)

# Request reviewers
pull.create_review_request(
    reviewers=["username1", "username2"],
    team_reviewers=["team1", "team2"]
)

# Delete review request
pull.delete_review_request(
    reviewers=["username1"],
    team_reviewers=["team1"]
)

# Get reviews
reviews = pull.get_reviews()

# Get specific review
review = pull.get_review(review_id)
```

### Comment Management

```python
# Add general comment
comment = pull.create_issue_comment("General comment")

# Add review comment on specific line
comment = pull.create_review_comment(
    body="Consider using a different approach",
    commit=commit_obj,
    path="file.py",
    line=42
)

# Reply to review comment
reply = pull.create_review_comment_reply(
    comment_id=123,
    body="Good suggestion, will update"
)

# Get comments
review_comments = pull.get_review_comments()
issue_comments = pull.get_issue_comments()
```

### Merge Operations

```python
# Check if mergeable
if pull.mergeable:
    # Merge pull request
    pull.merge(
        commit_message="Merge feature branch",
        commit_title="Feature: Add new functionality",
        merge_method="merge",  # or "squash", "rebase"
        sha=pull.head.sha
    )

# Enable auto-merge
pull.enable_automerge(
    merge_method="SQUASH",  # or "MERGE", "REBASE"
    commit_title="Auto-merge feature branch",
    commit_body="Automatically merged PR #123"
)

# Disable auto-merge
pull.disable_automerge()
```

### Branch Management

```python
# Update branch with base
pull.update_branch()

# Delete head branch after merge
pull.delete_branch()

# Restore deleted branch
pull.restore_branch()
```

### Label Management

```python
# Get labels
labels = pull.get_labels()

# Add labels
pull.add_to_labels("bug", "high-priority")

# Remove label
pull.remove_from_labels("bug")

# Set labels (replaces existing)
pull.set_labels("feature", "approved")

# Remove all labels
pull.delete_labels()
```

### File Operations

```python
# Get changed files
files = pull.get_files()

# Get commits
commits = pull.get_commits()
```

## Common Patterns

### Code Review Workflow

```python
# Reviewer workflow
def review_pull_request(pull):
    # Check changes
    files = pull.get_files()
    commits = pull.get_commits()
    
    comments = []
    for file in files:
        if file.filename.endswith('.py'):
            # Add review comments
            comments.append({
                'path': file.filename,
                'position': file.changes,
                'body': 'Consider adding docstring'
            })
    
    # Submit review
    pull.create_review(
        body="Please address the following comments",
        event="REQUEST_CHANGES",
        comments=comments
    )

# Author workflow
def update_pull_request(pull):
    # Address review comments
    for comment in pull.get_review_comments():
        pull.create_review_comment_reply(
            comment.id,
            "Updated with suggested changes"
        )
    
    # Request re-review
    pull.create_review_request(
        reviewers=[reviewer.login for reviewer in pull.requested_reviewers]
    )
```

### Automated Merge

```python
def auto_merge_when_ready(pull):
    if (pull.mergeable and 
        len(list(pull.get_reviews())) >= 2 and
        all(label.name != 'do-not-merge' for label in pull.get_labels())):
        
        pull.merge(
            commit_title=f"Merge: {pull.title}",
            commit_message=f"Automatically merged PR #{pull.number}\n\n{pull.body}",
            merge_method="squash"
        )
```

## Error Handling

```python
try:
    pull.merge()
except github.GithubException as e:
    if e.status == 405:  # Method not allowed
        if "Pull Request is not mergeable" in e.data["message"]:
            print("Pull request has conflicts")
        elif "Required status check" in e.data["message"]:
            print("Status checks are pending or failed")
        elif "Required reviews" in e.data["message"]:
            print("Required reviews are missing")
    elif e.status == 404:
        print("Pull request not found")
    else:
        print(f"Error: {e.status} - {e.data}")
```

## Best Practices

1. Pull Request Creation
   - Use clear, descriptive titles
   - Provide detailed descriptions
   - Reference related issues
   - Keep changes focused
   - Include test coverage

2. Code Review
   - Review all changed files
   - Add specific comments
   - Use suggestion syntax
   - Be constructive
   - Follow team guidelines

3. Merge Management
   - Keep branches up to date
   - Resolve conflicts promptly
   - Use appropriate merge strategy
   - Clean up after merge
   - Maintain linear history

4. Automation
   - Set up CI/CD checks
   - Use auto-merge when appropriate
   - Automate routine tasks
   - Monitor status checks
   - Keep branches clean

5. Communication
   - Respond to reviews promptly
   - Keep discussions focused
   - Update status regularly
   - Document decisions
   - Use clear labels
