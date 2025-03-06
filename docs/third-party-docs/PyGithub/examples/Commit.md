- »
- [Examples](https://pygithub.readthedocs.io/en/stable/examples.html) »
- Commit
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/examples/Commit.rst.txt)

* * *

# Commit [¶](https://pygithub.readthedocs.io/en/stable/examples/Commit.html\#commit "Permalink to this headline")

## Create commit status check [¶](https://pygithub.readthedocs.io/en/stable/examples/Commit.html\#create-commit-status-check "Permalink to this headline")

```
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

## Get commit date [¶](https://pygithub.readthedocs.io/en/stable/examples/Commit.html\#get-commit-date "Permalink to this headline")

```
>>> commit = repo.get_commit(sha=sha)
>>> print(commit.commit.author.date)
2018-10-11 03:04:52
>>> print(commit.commit.committer.date)
2018-10-11 03:04:52

```