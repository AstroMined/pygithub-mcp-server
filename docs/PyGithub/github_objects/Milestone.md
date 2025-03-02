- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- Milestone
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/Milestone.rst.txt)

* * *

# Milestone [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Milestone.html\#milestone "Permalink to this headline")

_class_ `github.Milestone.` `Milestone` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Milestone.html#github.Milestone.Milestone "Permalink to this definition")

This class represents Milestones.

The reference can be found here
[https://docs.github.com/en/rest/reference/issues#milestones](https://docs.github.com/en/rest/reference/issues#milestones)

The OpenAPI schema can be found at
\- /components/schemas/issue-event-milestone
\- /components/schemas/milestone
\- /components/schemas/nullable-milestone

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


`delete`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Milestone.html#github.Milestone.Milestone.delete "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/milestones/{number}](https://docs.github.com/en/rest/reference/issues#milestones)

`edit`( _title: str_, _state: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _description: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _due\_on: Union\[datetime.date_, _github.GithubObject.\_NotSetType\] = NotSet_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Milestone.html#github.Milestone.Milestone.edit "Permalink to this definition")Calls

[PATCH /repos/{owner}/{repo}/milestones/{number}](https://docs.github.com/en/rest/reference/issues#milestones)

`get_labels`() → github.PaginatedList.PaginatedList\[github.Label.Label\]\[github.Label.Label\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Milestone.html#github.Milestone.Milestone.get_labels "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/milestones/{number}/labels](https://docs.github.com/en/rest/reference/issues#labels)