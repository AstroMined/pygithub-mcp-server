- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- Workflow
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/Workflow.rst.txt)

* * *

# Workflow [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Workflow.html\#workflow "Permalink to this headline")

_class_ `github.Workflow.` `Workflow` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Workflow.html#github.Workflow.Workflow "Permalink to this definition")

This class represents Workflows.

The reference can be found here
[https://docs.github.com/en/rest/reference/actions#workflows](https://docs.github.com/en/rest/reference/actions#workflows)

The OpenAPI schema can be found at
\- /components/schemas/workflow

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


`create_dispatch`( _ref: github.Branch.Branch \| github.Tag.Tag \| github.Commit.Commit \| str_, _inputs: Opt\[dict\] = NotSet_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Workflow.html#github.Workflow.Workflow.create_dispatch "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/actions/workflows/{workflow\_id}/dispatches](https://docs.github.com/en/rest/reference/actions#create-a-workflow-dispatch-event)

`get_runs`( _actor: Opt\[github.NamedUser.NamedUser \| str\] = NotSet_, _branch: Opt\[github.Branch.Branch \| str\] = NotSet_, _event: Opt\[str\] = NotSet_, _status: Opt\[str\] = NotSet_, _created: Opt\[str\] = NotSet_, _exclude\_pull\_requests: Opt\[bool\] = NotSet_, _check\_suite\_id: Opt\[int\] = NotSet_, _head\_sha: Opt\[str\] = NotSet_) → PaginatedList\[github.WorkflowRun.WorkflowRun\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Workflow.html#github.Workflow.Workflow.get_runs "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/actions/workflows/{workflow\_id}/runs](https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2022-11-28#list-workflow-runs-for-a-workflow)

`disable`() → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Workflow.html#github.Workflow.Workflow.disable "Permalink to this definition")Calls

[PUT /repos/{owner}/{repo}/actions/workflows/{workflow\_id}/disable](https://docs.github.com/en/rest/actions/workflows?apiVersion=2022-11-28#disable-a-workflow)

Return type

bool

`enable`() → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Workflow.html#github.Workflow.Workflow.enable "Permalink to this definition")Calls

[PUT /repos/{owner}/{repo}/actions/workflows/{workflow\_id}/enable](https://docs.github.com/en/rest/actions/workflows?apiVersion=2022-11-28#enable-a-workflow)

Return type

bool