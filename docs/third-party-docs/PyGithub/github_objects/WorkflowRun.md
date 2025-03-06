- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- WorkflowRun
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/WorkflowRun.rst.txt)

* * *

# WorkflowRun [¶](https://pygithub.readthedocs.io/en/stable/github_objects/WorkflowRun.html\#workflowrun "Permalink to this headline")

_class_ `github.WorkflowRun.` `WorkflowRun` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/WorkflowRun.html#github.WorkflowRun.WorkflowRun "Permalink to this definition")

This class represents Workflow Runs.

The reference can be found here
[https://docs.github.com/en/rest/reference/actions#workflow-runs](https://docs.github.com/en/rest/reference/actions#workflow-runs)

The OpenAPI schema can be found at
\- /components/schemas/artifact/properties/workflow\_run
\- /components/schemas/workflow-run

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


`cancel`() → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/WorkflowRun.html#github.WorkflowRun.WorkflowRun.cancel "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/actions/runs/{run\_id}/cancel](https://docs.github.com/en/rest/reference/actions#workflow-runs)

`rerun`() → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/WorkflowRun.html#github.WorkflowRun.WorkflowRun.rerun "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/actions/runs/{run\_id}/rerun](https://docs.github.com/en/rest/reference/actions#workflow-runs)

`rerun_failed_jobs`() → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/WorkflowRun.html#github.WorkflowRun.WorkflowRun.rerun_failed_jobs "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/actions/runs/{run\_id}/rerun-failed-jobs](https://docs.github.com/en/rest/reference/actions#workflow-runs)

`timing`() → github.WorkflowRun.TimingData [¶](https://pygithub.readthedocs.io/en/stable/github_objects/WorkflowRun.html#github.WorkflowRun.WorkflowRun.timing "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/actions/runs/{run\_id}/timing](https://docs.github.com/en/rest/reference/actions#workflow-runs)

`delete`() → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/WorkflowRun.html#github.WorkflowRun.WorkflowRun.delete "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/actions/runs/{run\_id}](https://docs.github.com/en/rest/reference/actions#workflow-runs)

`jobs`( _\_filter: Opt\[str\] = NotSet_) → PaginatedList\[WorkflowJob\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/WorkflowRun.html#github.WorkflowRun.WorkflowRun.jobs "Permalink to this definition")

:calls " [GET /repos/{owner}/{repo}/actions/runs/{run\_id}/jobs](https://docs.github.com/en/rest/reference/actions#list-jobs-for-a-workflow-run)
:param \_filter: string latest, or all