# Repository

Examples of working with GitHub repositories using PyGithub.

## Get repository topics

Get the topics/tags associated with a repository:

```python
repo = g.get_repo("PyGithub/PyGithub")
repo.get_topics()
# Output: ['pygithub', 'python', 'github', 'github-api']
```

## Get count of stars

Get the number of stars a repository has:

```python
repo = g.get_repo("PyGithub/PyGithub")
repo.stargazers_count
# Output: 2086
```

## Get list of open issues

Retrieve all open issues in a repository:

```python
repo = g.get_repo("PyGithub/PyGithub")
open_issues = repo.get_issues(state='open')
for issue in open_issues:
    print(issue)

# Output:
# Issue(title="How to get public events?", number=913)
# Issue(title="Prevent .netrc from overwriting Auth header", number=910)
# Issue(title="Cache fetch responses", number=901)
# Issue(title="Is suspended_users for github enterprise implemented in NamedUser?", number=900)
# Issue(title="Adding migration api wrapper", number=899)
```

## Get list of code scanning alerts

Get security alerts from code scanning:

```python
repo = g.get_repo("PyGithub/PyGithub")
codescan_alerts = repo.get_codescan_alerts()
for alert in codescan_alerts:
    print(alert.number, alert.created_at, alert.dismissed_at)
    print("  ", alert.tool.name, alert.tool.version, alert.tool.guid)
    print("  ", alert.rule.name, alert.rule.security_severity_level, alert.rule.severity)
    print("    ", alert.rule.description)
    print("  ", alert.most_recent_instance.ref, alert.most_recent_instance.state)
    print("    ", alert.most_recent_instance.location)
    print("    ", alert.most_recent_instance.message['text'])
```

## Get all repository labels

List all labels defined in the repository:

```python
repo = g.get_repo("PyGithub/PyGithub")
labels = repo.get_labels()
for label in labels:
    print(label)

# Output:
# Label(name="Hacktoberfest")
# Label(name="WIP")
# Label(name="bug")
# Label(name="documentation")
```

## Working with Repository Contents

### Get root directory contents

List all files and directories at the root of the repository:

```python
repo = g.get_repo("PyGithub/PyGithub")
contents = repo.get_contents("")
for content_file in contents:
    print(content_file)

# Output:
# ContentFile(path=".github")
# ContentFile(path=".gitignore")
# ContentFile(path="CONTRIBUTING.md")
# ContentFile(path="COPYING")
# ...
```

### Get contents recursively

Get all files in the repository recursively:

```python
repo = g.get_repo("PyGithub/PyGithub")
contents = repo.get_contents("")
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        print(file_content)
```

### Get a specific file

Get the contents of a specific file:

```python
repo = g.get_repo("PyGithub/PyGithub")
contents = repo.get_contents("README.md")
print(contents)
# Output: ContentFile(path="README.md")
```

### File Operations

Create a new file:
```python
repo = g.get_repo("PyGithub/PyGithub")
repo.create_file("test.txt", "test", "test", branch="test")
```

Update an existing file:
```python
repo = g.get_repo("PyGithub/PyGithub")
contents = repo.get_contents("test.txt", ref="test")
repo.update_file(contents.path, "more tests", "more tests", contents.sha, branch="test")
```

Delete a file:
```python
repo = g.get_repo("PyGithub/PyGithub")
contents = repo.get_contents("test.txt", ref="test")
repo.delete_file(contents.path, "remove test", contents.sha, branch="test")
```

## Repository Analytics

### Get top referrers

Get the top 10 referrers over the last 14 days:

```python
repo = g.get_repo("PyGithub/PyGithub")
contents = repo.get_top_referrers()
print(contents)
# Output:
# [
#   Referrer(referrer="Google", count=4, uniques=3),
#   Referrer(referrer="stackoverflow.com", count=2, uniques=2),
#   Referrer(referrer="eggsonbread.com", count=1, uniques=1),
#   Referrer(referrer="yandex.ru", count=1, uniques=1)
# ]
```

### Get popular content

Get the top 10 popular contents over the last 14 days:

```python
repo = g.get_repo("PyGithub/PyGithub")
contents = repo.get_top_paths()
print(contents)
# Returns list of Path objects with path, title, count, and uniques
```

### Get clone statistics

Get number of clones and breakdown for the last 14 days:

```python
repo = g.get_repo("PyGithub/PyGithub")
contents = repo.get_clones_traffic()
contents = repo.get_clones_traffic(per="week")
# Returns dictionary with count, uniques, and list of Clones objects
```

### Get view statistics

Get number of views and breakdown for the last 14 days:

```python
repo = g.get_repo("PyGithub/PyGithub")
contents = repo.get_views_traffic()
contents = repo.get_views_traffic(per="week")
# Returns dictionary with count, uniques, and list of View objects
```

## Notifications

Mark all notifications for the repository as read:

```python
repo = g.get_repo("PyGithub/PyGithub")
repo.mark_notifications_as_read()
