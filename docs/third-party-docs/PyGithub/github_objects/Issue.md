- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- Issue
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/Issue.rst.txt)

* * *

# Issue [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html\#issue "Permalink to this headline")

_class_ `github.Issue.` `Issue` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue "Permalink to this definition")

This class represents Issues.

The reference can be found here
[https://docs.github.com/en/rest/reference/issues](https://docs.github.com/en/rest/reference/issues)

The OpenAPI schema can be found at
\- /components/schemas/issue
\- /components/schemas/issue-search-result-item
\- /components/schemas/nullable-issue

A CompletableGithubObject can be partially initialised (completed=False). Accessing attributes that are not
initialized will then trigger a request to complete all attributes.

A partially initialized CompletableGithubObject (completed=False) can be completed
via complete(). This requires the url to be given via parameter url or attributes.

With a requester where Requester.is\_lazy == True, this CompletableGithubObjects is
partially initialized. This requires the url to be given via parameter url or attributes.
Any CompletableGithubObject created from this lazy object will be lazy itself if created with
parameter url or attributes.

Parameters

- **requester** – requester

- **headers** – response headers

- **attributes** – attributes to initialize

- **completed** – do not update non-initialized attributes when True

- **url** – url of this instance, overrides attributes\['url'\]

- **accept** – use this accept header when completing this instance


`as_pull_request`() → PullRequest [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.as_pull_request "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/pulls/{number}](https://docs.github.com/en/rest/reference/pulls)

`add_to_assignees`( _\*assignees: NamedUser \| str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.add_to_assignees "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/issues/{number}/assignees](https://docs.github.com/en/rest/reference/issues#assignees)

`add_to_labels`( _\*labels: Label \| str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.add_to_labels "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/issues/{number}/labels](https://docs.github.com/en/rest/reference/issues#labels)

`create_comment`( _body: str_) → IssueComment [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.create_comment "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/issues/{number}/comments](https://docs.github.com/en/rest/reference/issues#comments)

`delete_labels`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.delete_labels "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/issues/{number}/labels](https://docs.github.com/en/rest/reference/issues#labels)

`edit`( _title: Opt\[str\] = NotSet_, _body: Opt\[str\] = NotSet_, _assignee: Opt\[str \| NamedUser \| None\] = NotSet_, _state: Opt\[str\] = NotSet_, _milestone: Opt\[Milestone \| None\] = NotSet_, _labels: Opt\[list\[str\]\] = NotSet_, _assignees: Opt\[list\[NamedUser \| str\]\] = NotSet_, _state\_reason: Opt\[str\] = NotSet_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.edit "Permalink to this definition")Calls

[PATCH /repos/{owner}/{repo}/issues/{number}](https://docs.github.com/en/rest/reference/issues)

Parameters

- **assignee** – deprecated, use assignees instead. assignee=None means to remove current assignee.

- **milestone** – milestone=None means to remove current milestone.


`lock`( _lock\_reason: str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.lock "Permalink to this definition")Calls

[PUT /repos/{owner}/{repo}/issues/{issue\_number}/lock](https://docs.github.com/en/rest/reference/issues)

`unlock`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.unlock "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/issues/{issue\_number}/lock](https://docs.github.com/en/rest/reference/issues)

`get_comment`( _id: int_) → IssueComment [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.get_comment "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/issues/comments/{id}](https://docs.github.com/en/rest/reference/issues#comments)

`get_comments`( _since: Opt\[datetime\] = NotSet_) → PaginatedList\[IssueComment\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.get_comments "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/issues/{number}/comments](https://docs.github.com/en/rest/reference/issues#comments)

`get_events`() → PaginatedList\[IssueEvent\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.get_events "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/issues/{issue\_number}/events](https://docs.github.com/en/rest/reference/issues#events)

`get_labels`() → PaginatedList\[Label\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.get_labels "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/issues/{number}/labels](https://docs.github.com/en/rest/reference/issues#labels)

`remove_from_assignees`( _\*assignees: NamedUser \| str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.remove_from_assignees "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/issues/{number}/assignees](https://docs.github.com/en/rest/reference/issues#assignees)

`remove_from_labels`( _label: Label \| str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.remove_from_labels "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/issues/{number}/labels/{name}](https://docs.github.com/en/rest/reference/issues#labels)

`set_labels`( _\*labels: Label \| str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.set_labels "Permalink to this definition")Calls

[PUT /repos/{owner}/{repo}/issues/{number}/labels](https://docs.github.com/en/rest/reference/issues#labels)

`get_reactions`() → PaginatedList\[Reaction\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.get_reactions "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/issues/{number}/reactions](https://docs.github.com/en/rest/reference/reactions#list-reactions-for-an-issue)

`create_reaction`( _reaction\_type: str_) → Reaction [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.create_reaction "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/issues/{number}/reactions](https://docs.github.com/en/rest/reference/reactions)

`delete_reaction`( _reaction\_id: int_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.delete_reaction "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/issues/{issue\_number}/reactions/{reaction\_id}](https://docs.github.com/en/rest/reference/reactions#delete-an-issue-reaction)

`get_timeline`() → PaginatedList\[TimelineEvent\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue.get_timeline "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/issues/{number}/timeline](https://docs.github.com/en/rest/reference/issues#list-timeline-events-for-an-issue)