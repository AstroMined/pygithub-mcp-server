# Main Class

This is the main class that provides core functionality for interacting with GitHub.

## Get current user

Get information about the authenticated user:

```python
user = g.get_user()
user.login
# Output: 'sfdye'
```

## Get user by name

Get information about any GitHub user by their username:

```python
user = g.get_user("sfdye")
user.name
# Output: 'Wan Liuyang'
```

## Get repository by name

Access a GitHub repository using the format "owner/repo":

```python
repo = g.get_repo("PyGithub/PyGithub")
repo.name
# Output: 'PyGithub'
```

## Get organization by name

Access a GitHub organization by its name:

```python
org = g.get_organization("PyGithub")
org.login
# Output: 'PyGithub'
```

## Get enterprise consumed licenses by name

Get information about enterprise license consumption:

```python
enterprise = g.get_enterprise_consumed_licenses("PyGithub")
enterprise_consumed_licenses = enterprise.get_enterprise_consumed_licenses()
enterprise_consumed_licenses.total_seats_consumed
# Output: 5000
```

## Search repositories by language

Search for repositories using language as a criteria:

```python
repositories = g.search_repositories(query='language:python')
for repo in repositories:
    print(repo)

# Output:
# Repository(full_name="vinta/awesome-python")
# Repository(full_name="donnemartin/system-design-primer")
# Repository(full_name="toddmotto/public-apis")
# Repository(full_name="rg3/youtube-dl")
# Repository(full_name="tensorflow/models")
# Repository(full_name="django/django")
```

## Search repositories based on number of issues with good-first-issue

Find repositories that have multiple issues tagged as 'good first issue':

```python
repositories = g.search_repositories(query='good-first-issues:>3')
for repo in repositories:
    print(repo)

# Output:
# Repository(full_name="vuejs/vue")
# Repository(full_name="facebook/react")
# Repository(full_name="facebook/react-native")
# Repository(full_name="electron/electron")
# Repository(full_name="Microsoft/vscode")
