- »
- [Examples](https://pygithub.readthedocs.io/en/stable/examples.html) »
- Branch
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/examples/Branch.rst.txt)

* * *

# Branch [¶](https://pygithub.readthedocs.io/en/stable/examples/Branch.html\#branch "Permalink to this headline")

## Get list of branches [¶](https://pygithub.readthedocs.io/en/stable/examples/Branch.html\#get-list-of-branches "Permalink to this headline")

```
>>> repo = g.get_repo("PyGithub/PyGithub")
>>> list(repo.get_branches())
[Branch(name="master")]

```

Note that the Branch object returned by get\_branches() is not fully populated,
and you can not query everything. Use get\_branch(branch="master") once you
have the branch name.

## Get a branch [¶](https://pygithub.readthedocs.io/en/stable/examples/Branch.html\#get-a-branch "Permalink to this headline")

```
>>> repo = g.get_repo("PyGithub/PyGithub")
>>> repo.get_branch(branch="master")
Branch(name="master")

```

## Get HEAD commit of a branch [¶](https://pygithub.readthedocs.io/en/stable/examples/Branch.html\#get-head-commit-of-a-branch "Permalink to this headline")

```
>>> branch = g.get_repo("PyGithub/PyGithub").get_branch("master")
>>> branch.commit
Commit(sha="5e69ff00a3be0a76b13356c6ff42af79ff469ef3")

```

## Get protection status of a branch [¶](https://pygithub.readthedocs.io/en/stable/examples/Branch.html\#get-protection-status-of-a-branch "Permalink to this headline")

```
>>> branch = g.get_repo("PyGithub/PyGithub").get_branch("master")
>>> branch.protected
True

```

## See required status checks of a branch [¶](https://pygithub.readthedocs.io/en/stable/examples/Branch.html\#see-required-status-checks-of-a-branch "Permalink to this headline")

```
>>> branch = g.get_repo("PyGithub/PyGithub").get_branch("master")
>>> branch.get_required_status_checks()
RequiredStatusChecks(url="https://api.github.com/repos/PyGithub/PyGithub/branches/master/protection/required_status_checks", strict=True)

```