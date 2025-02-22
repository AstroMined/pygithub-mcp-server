# Commit

Examples of working with GitHub commits using PyGithub.

## Create commit status check

Create a status check on a specific commit, which is useful for CI/CD integrations:

```python
# sha -> commit on which the status check will be created
# For example, for a webhook payload
# sha = data["pull_request"]["head"]["sha"]
repo.get_commit(sha=sha).create_status(
    state="pending",
    target_url="https://FooCI.com",
    description="FooCI is building",
    context="ci/FooCI"
)
```

The status check parameters:
- `state`: Can be "pending", "success", "error", or "failure"
- `target_url`: URL where users can find more details about this status
- `description`: Short description of the status
- `context`: String label to differentiate this status from other status checks

## Get commit date

Get the author and committer dates for a commit:

```python
commit = repo.get_commit(sha=sha)
print(commit.commit.author.date)
# Output: 2018-10-11 03:04:52

print(commit.commit.committer.date)
# Output: 2018-10-11 03:04:52
```

Note: 
- The `author.date` is when the commit was originally created
- The `committer.date` might be different if the commit was amended or rebased
