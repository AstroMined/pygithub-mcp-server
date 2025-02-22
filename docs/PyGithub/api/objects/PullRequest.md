# Pull Request Object

The PullRequest object represents a GitHub pull request and provides access to all pull request-related operations.

## Constructor

Pull requests are typically obtained through a Repository object:

```python
# Get pull request by number
pr = repo.get_pull(number)

# Create new pull request
pr = repo.create_pull(
    title="Feature implementation",
    body="Description of changes",
    base="main",
    head="feature-branch"
)
```

## Properties

- `number`: Pull request number
- `title`: Pull request title
- `body`: Pull request description
- `state`: State of the pull request (open/closed)
- `merged`: Whether the pull request has been merged
- `mergeable`: Whether the pull request can be merged
- `mergeable_state`: Detailed merge state
- `merged_by`: User who merged the pull request
- `merged_at`: When the pull request was merged
- `comments`: Number of comments
- `commits`: Number of commits
- `additions`: Number of added lines
- `deletions`: Number of deleted lines
- `changed_files`: Number of changed files
- `head`: Reference to the source branch
- `base`: Reference to the target branch
- `user`: User who created the pull request
- `assignee`: User assigned to the pull request
- `assignees`: List of users assigned to the pull request
- `labels`: List of labels
- `milestone`: Associated milestone
- `draft`: Whether the pull request is a draft

## Methods

### Basic Operations

```python
# Edit pull request
pr.edit(
    title="Updated title",
    body="Updated description",
    state="closed"
)

# Convert to draft
pr.convert_to_draft()

# Mark ready for review
pr.mark_ready_for_review()

# Check if merged
is_merged = pr.is_merged()

# Merge pull request
pr.merge(
    commit_message="Merge message",
    merge_method="merge"  # or "squash" or "rebase"
)
```

### Review Operations

```python
# Get reviews
reviews = pr.get_reviews()

# Create review
review = pr.create_review(
    body="Review comments",
    event="APPROVE"  # or "REQUEST_CHANGES" or "COMMENT"
)

# Get specific review
review = pr.get_review(review_id)

# Get review comments
comments = pr.get_review_comments()

# Create review comment
comment = pr.create_review_comment(
    body="Comment",
    commit_id="sha",
    path="file.py",
    position=1
)

# Create review comment reply
reply = pr.create_review_comment_reply(
    body="Reply",
    comment_id=comment.id
)
```

### Commit Operations

```python
# Get commits
commits = pr.get_commits()

# Get files
files = pr.get_files()
```

### Issue Operations

Since pull requests are also issues, you can use issue-related methods:

```python
# Get issue comments
comments = pr.get_issue_comments()

# Create issue comment
comment = pr.create_issue_comment("Comment text")

# Get labels
labels = pr.get_labels()

# Add labels
pr.add_to_labels("bug", "enhancement")

# Remove labels
pr.remove_from_labels("bug")

# Set labels
pr.set_labels("bug", "enhancement")
```

### Review Request Operations

```python
# Get review requests
requests = pr.get_review_requests()

# Create review request
pr.create_review_request(
    reviewers=["username"],
    team_reviewers=["team-name"]
)

# Delete review request
pr.delete_review_request(
    reviewers=["username"],
    team_reviewers=["team-name"]
)
```

### Assignee Operations

```python
# Add assignees
pr.add_to_assignees("username1", "username2")

# Remove assignees
pr.remove_from_assignees("username1")
```

### Status Check Operations

```python
# Get last commit
last_commit = pr.get_commits().reversed[0]

# Get status checks
statuses = last_commit.get_statuses()

# Get combined status
combined_status = last_commit.get_combined_status()
```

### Auto-merge Operations

```python
# Enable auto-merge
pr.enable_automerge(
    merge_method="MERGE",
    commit_title="Auto merge PR",
    commit_message="Auto merge commit message"
)

# Disable auto-merge
pr.disable_automerge()
```

## Error Handling

Pull request operations can raise various exceptions:

```python
try:
    pr = repo.get_pull(number)
    pr.merge()
except github.UnknownObjectException:
    print("Pull request not found")
except github.GithubException as e:
    if e.status == 405:  # Method not allowed
        print("Pull request cannot be merged")
    else:
        print(f"Error: {e.status} - {e.data}")
```

## Best Practices

1. Review Management
   - Always provide meaningful review comments
   - Use appropriate review events (APPROVE/REQUEST_CHANGES/COMMENT)
   - Consider using draft PRs for work in progress

2. Merge Strategy
   - Choose appropriate merge method (merge/squash/rebase)
   - Verify mergeable state before attempting merge
   - Handle merge conflicts appropriately

3. Status Checks
   - Wait for required status checks to complete
   - Verify all checks pass before merging
   - Handle check failures appropriately

4. Collaboration
   - Assign appropriate reviewers
   - Use labels effectively
   - Keep descriptions and comments clear and professional

5. Performance
   - Batch operations when possible
   - Use conditional requests
   - Monitor API rate limits

6. Error Handling
   - Handle merge conflicts gracefully
   - Implement proper error recovery
   - Log important events and errors
