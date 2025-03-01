# Issues

Examples of working with GitHub Issues using PyGithub.

## Get issue

Retrieve a specific issue by its number:

```python
repo = g.get_repo("PyGithub/PyGithub")
repo.get_issue(number=874)
# Output: Issue(title="PyGithub example usage", number=874)
```

## Create comment on issue

Add a comment to an existing issue:

```python
repo = g.get_repo("PyGithub/PyGithub")
issue = repo.get_issue(number=874)
issue.create_comment("Test")
# Output: IssueComment(user=NamedUser(login="user"), id=36763078)
```

## Create Issues

### Basic issue

Create a simple issue with just a title:

```python
repo = g.get_repo("PyGithub/PyGithub")
repo.create_issue(title="This is a new issue")
# Output: Issue(title="This is a new issue", number=XXX)
```

### Issue with body

Create an issue with a description:

```python
repo = g.get_repo("PyGithub/PyGithub")
repo.create_issue(
    title="This is a new issue",
    body="This is the issue body"
)
# Output: Issue(title="This is a new issue", number=XXX)
```

### Issue with labels

Create an issue with labels:

```python
repo = g.get_repo("PyGithub/PyGithub")
label = repo.get_label("My Label")
repo.create_issue(
    title="This is a new issue",
    labels=[label]
)
# Output: Issue(title="This is a new issue", number=XXX)
```

### Issue with assignee

Create an issue and assign it to someone:

```python
repo = g.get_repo("PyGithub/PyGithub")
repo.create_issue(
    title="This is a new issue",
    assignee="github-username"
)
# Output: Issue(title="This is a new issue", number=XXX)
```

### Issue with milestone

Create an issue and associate it with a milestone:

```python
repo = g.get_repo("PyGithub/PyGithub")
milestone = repo.create_milestone("New Issue Milestone")
repo.create_issue(
    title="This is a new issue",
    milestone=milestone
)
# Output: Issue(title="This is a new issue", number=XXX)
```

## Close all issues

Close all open issues in a repository:

```python
repo = g.get_repo("PyGithub/PyGithub")
open_issues = repo.get_issues(state='open')
for issue in open_issues:
    issue.edit(state='closed')
```

## Common Parameters

When creating or editing issues, you can use these parameters:
- `title`: The title of the issue
- `body`: The body/description of the issue
- `assignee`: GitHub username to assign the issue to
- `milestone`: Milestone object to associate with the issue
- `labels`: List of Label objects to apply to the issue
- `state`: Issue state ('open' or 'closed')
