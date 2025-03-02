- »
- [Examples](https://pygithub.readthedocs.io/en/stable/examples.html) »
- Issues
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/examples/Issue.rst.txt)

* * *

# Issues [¶](https://pygithub.readthedocs.io/en/stable/examples/Issue.html\#issues "Permalink to this headline")

## Get issue [¶](https://pygithub.readthedocs.io/en/stable/examples/Issue.html\#get-issue "Permalink to this headline")

```
>>> repo = g.get_repo("PyGithub/PyGithub")
>>> repo.get_issue(number=874)
    Issue(title="PyGithub example usage", number=874)

```

## Create comment on issue [¶](https://pygithub.readthedocs.io/en/stable/examples/Issue.html\#create-comment-on-issue "Permalink to this headline")

```
>>> repo = g.get_repo("PyGithub/PyGithub")
>>> issue = repo.get_issue(number=874)
>>> issue.create_comment("Test")
    IssueComment(user=NamedUser(login="user"), id=36763078)

```

## Create issue [¶](https://pygithub.readthedocs.io/en/stable/examples/Issue.html\#create-issue "Permalink to this headline")

```
>>> repo = g.get_repo("PyGithub/PyGithub")
>>> repo.create_issue(title="This is a new issue")
    Issue(title="This is a new issue", number=XXX)

```

## Create issue with body [¶](https://pygithub.readthedocs.io/en/stable/examples/Issue.html\#create-issue-with-body "Permalink to this headline")

```
>>> repo = g.get_repo("PyGithub/PyGithub")
>>> repo.create_issue(title="This is a new issue", body="This is the issue body")
    Issue(title="This is a new issue", number=XXX)

```

## Create issue with labels [¶](https://pygithub.readthedocs.io/en/stable/examples/Issue.html\#create-issue-with-labels "Permalink to this headline")

```
>>> repo = g.get_repo("PyGithub/PyGithub")
>>> label = repo.get_label("My Label")
>>> repo.create_issue(title="This is a new issue", labels=[label])
    Issue(title="This is a new issue", number=XXX)

```

## Create issue with assignee [¶](https://pygithub.readthedocs.io/en/stable/examples/Issue.html\#create-issue-with-assignee "Permalink to this headline")

```
>>> repo = g.get_repo("PyGithub/PyGithub")
>>> repo.create_issue(title="This is a new issue", assignee="github-username")
    Issue(title="This is a new issue", number=XXX)

```

## Create issue with milestone [¶](https://pygithub.readthedocs.io/en/stable/examples/Issue.html\#create-issue-with-milestone "Permalink to this headline")

```
>>> repo = g.get_repo("PyGithub/PyGithub")
>>> milestone = repo.create_milestone("New Issue Milestone")
>>> repo.create_issue(title="This is a new issue", milestone=milestone)
    Issue(title="This is a new issue", number=XXX)

```

## Close all issues [¶](https://pygithub.readthedocs.io/en/stable/examples/Issue.html\#close-all-issues "Permalink to this headline")

```
>>> repo = g.get_repo("PyGithub/PyGithub")
>>> open_issues = repo.get_issues(state='open')
>>> for issue in open_issues:
...     issue.edit(state='closed')

```