# Pull Request

Examples of working with GitHub Pull Requests using PyGithub.

## Create a new Pull Request

Create a new PR with a formatted body:

```python
repo = g.get_repo("PyGithub/PyGithub")
body = '''
SUMMARY
Change HTTP library used to send requests

TESTS
  - [x] Send 'GET' request
  - [x] Send 'POST' request with/without body
'''
pr = repo.create_pull(
    base="master",
    head="develop",
    title="Use 'requests' instead of 'httplib'",
    body=body
)
pr
# Output: PullRequest(title="Use 'requests' instead of 'httplib'", number=664)
```

Parameters:
- `base`: The branch you want your changes pulled into
- `head`: The branch containing your changes
- `title`: Title of the pull request
- `body`: Detailed description of the changes

## Get Pull Request by Number

Retrieve a specific PR using its number:

```python
repo = g.get_repo("PyGithub/PyGithub")
pr = repo.get_pull(664)
pr
# Output: PullRequest(title="Use 'requests' instead of 'httplib'", number=664)
```

## Get Pull Requests by Query

Get multiple PRs matching specific criteria:

```python
repo = g.get_repo("PyGithub/PyGithub")
pulls = repo.get_pulls(
    state='open',
    sort='created',
    base='master'
)
for pr in pulls:
    print(pr.number)

# Output:
# 400
# 861
# 875
# 876
```

Parameters:
- `state`: Filter by PR state ('open', 'closed', 'all')
- `sort`: Sort by ('created', 'updated', 'popularity', 'long-running')
- `base`: Filter by base branch name

## Add and modify Pull Request comment

Create and edit comments on specific lines of code in a PR:

```python
repo = g.get_repo("PyGithub/PyGithub")
pr = repo.get_pull(2390)

# Get the last commit in the PR
last_commit = pr.get_commits()[pr.commits - 1]

# Create a comment
comment = pr.create_comment(
    "This is a comment",
    last_commit,
    "file.txt",
    0
)
comment
# Output: PullRequestComment(user=NamedUser(login="anonymous"), id=1057297855)

# Verify comment body
comment.body
# Output: 'This is a comment'

# Edit the comment
comment.edit("This is a modified comment")
comment.body
# Output: 'This is a modified comment'
```

Parameters for `create_comment`:
- `body`: The text of the comment
- `commit`: The commit to comment on
- `path`: The file path to comment on
- `position`: The line number in the file to comment on
