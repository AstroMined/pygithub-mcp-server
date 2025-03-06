- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- CheckRun
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/CheckRun.rst.txt)

* * *

# CheckRun [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckRun.html\#checkrun "Permalink to this headline")

_class_ `github.CheckRun.` `CheckRun` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckRun.html#github.CheckRun.CheckRun "Permalink to this definition")

This class represents check runs.

The reference can be found here
[https://docs.github.com/en/rest/reference/checks#check-runs](https://docs.github.com/en/rest/reference/checks#check-runs)

The OpenAPI schema can be found at
\- /components/schemas/check-run

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


`get_annotations`() → PaginatedList\[CheckRunAnnotation\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckRun.html#github.CheckRun.CheckRun.get_annotations "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/check-runs/{check\_run\_id}/annotations](https://docs.github.com/en/rest/reference/checks#list-check-run-annotations)

`edit`( _name: Opt\[str\] = NotSet_, _head\_sha: Opt\[str\] = NotSet_, _details\_url: Opt\[str\] = NotSet_, _external\_id: Opt\[str\] = NotSet_, _status: Opt\[str\] = NotSet_, _started\_at: Opt\[datetime\] = NotSet_, _conclusion: Opt\[str\] = NotSet_, _completed\_at: Opt\[datetime\] = NotSet_, _output: Opt\[dict\] = NotSet_, _actions: Opt\[list\[dict\]\] = NotSet_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckRun.html#github.CheckRun.CheckRun.edit "Permalink to this definition")Calls

[PATCH /repos/{owner}/{repo}/check-runs/{check\_run\_id}](https://docs.github.com/en/rest/reference/checks#update-a-check-run)