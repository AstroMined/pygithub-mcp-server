# Branch

Examples of working with GitHub repository branches using PyGithub.

## Get list of branches

List all branches in a repository:

```python
repo = g.get_repo("PyGithub/PyGithub")
list(repo.get_branches())
# Output: [Branch(name="master")]
```

**Important Note**: The Branch object returned by `get_branches()` is not fully populated,
and you cannot query everything. Use `get_branch(branch="master")` once you
have the branch name to get a fully populated Branch object.

## Get a specific branch

Get detailed information about a specific branch:

```python
repo = g.get_repo("PyGithub/PyGithub")
repo.get_branch(branch="master")
# Output: Branch(name="master")
```

## Get HEAD commit of a branch

Get the latest commit on a branch:

```python
branch = g.get_repo("PyGithub/PyGithub").get_branch("master")
branch.commit
# Output: Commit(sha="5e69ff00a3be0a76b13356c6ff42af79ff469ef3")
```

## Get protection status of a branch

Check if a branch has protection rules enabled:

```python
branch = g.get_repo("PyGithub/PyGithub").get_branch("master")
branch.protected
# Output: True
```

## See required status checks of a branch

Get information about required status checks for a protected branch:

```python
branch = g.get_repo("PyGithub/PyGithub").get_branch("master")
branch.get_required_status_checks()
# Output: RequiredStatusChecks(url="https://api.github.com/repos/PyGithub/PyGithub/branches/master/protection/required_status_checks", strict=True)
```

This shows whether the branch requires status checks to pass before merging and whether it requires branches to be up to date before merging.
