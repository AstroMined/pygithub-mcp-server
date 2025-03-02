» [Examples](../examples.md) » PullRequest  
[View page source](https://pygithub.readthedocs.io/en/stable/examples/PullRequest.html)

* * *

# PullRequest [¶](https://pygithub.readthedocs.io/en/stable/examples/PullRequest.html\#pullrequest "Permalink to this headline")

## Create a new Pull Request [¶](https://pygithub.readthedocs.io/en/stable/examples/PullRequest.html\#create-a-new-pull-request "Permalink to this headline")

```
>>> repo = g.get_repo("PyGithub/PyGithub")
>>> body = '''
>>> SUMMARY
>>> Change HTTP library used to send requests
>>>
>>> TESTS
>>>   - [x] Send 'GET' request
>>>   - [x] Send 'POST' request with/without body
>>> '''
>>> pr = repo.create_pull(base="master", head="develop", title="Use 'requests' instead of 'httplib'", body=body)
>>> pr
PullRequest(title="Use 'requests' instead of 'httplib'", number=664)

```

## Get Pull Request by Number [¶](https://pygithub.readthedocs.io/en/stable/examples/PullRequest.html\#get-pull-request-by-number "Permalink to this headline")

```
>>> repo = g.get_repo("PyGithub/PyGithub")
>>> pr = repo.get_pull(664)
>>> pr
PullRequest(title="Use 'requests' instead of 'httplib'", number=664)

```

## Get Pull Requests by Query [¶](https://pygithub.readthedocs.io/en/stable/examples/PullRequest.html\#get-pull-requests-by-query "Permalink to this headline")

```
>>> repo = g.get_repo("PyGithub/PyGithub")
>>> pulls = repo.get_pulls(state='open', sort='created', base='master')
>>> for pr in pulls:
...    print(pr.number)
...
400
861
875
876

```

## Add and modify Pull Request comment [¶](https://pygithub.readthedocs.io/en/stable/examples/PullRequest.html\#add-and-modify-pull-request-comment "Permalink to this headline")

```
>>> repo = g.get_repo("PyGithub/PyGithub")
>>> pr = repo.get_pull(2390)
>>> last_commit = pr.get_commits()[pr.commits - 1]
>>> comment = pr.create_comment("This is a comment", last_commit, "file.txt", 0)
>>> comment
PullRequestComment(user=NamedUser(login="anonymous"), id=1057297855)
>>> comment.body
'This is a comment'
>>> comment.edit("This is a modified comment")
>>> comment.body
'This is a modified comment'

```