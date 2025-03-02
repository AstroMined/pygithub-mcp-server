- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- CheckSuite
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/CheckSuite.rst.txt)

* * *

# CheckSuite [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html\#checksuite "Permalink to this headline")

_class_ `github.CheckSuite.` `CheckSuite` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite "Permalink to this definition")

This class represents check suites.

The reference can be found here
[https://docs.github.com/en/rest/reference/checks#check-suites](https://docs.github.com/en/rest/reference/checks#check-suites)

The OpenAPI schema can be found at
\- /components/schemas/check-run/properties/check\_suite
\- /components/schemas/check-suite

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


_property_ `after` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite.after "Permalink to this definition")Type

string

_property_ `app` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite.app "Permalink to this definition")Type

[`github.GithubApp.GithubApp`](https://pygithub.readthedocs.io/en/stable/github_objects/GithubApp.html#github.GithubApp.GithubApp "github.GithubApp.GithubApp")

_property_ `before` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite.before "Permalink to this definition")Type

string

_property_ `check_runs_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite.check_runs_url "Permalink to this definition")Type

string

_property_ `conclusion` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite.conclusion "Permalink to this definition")Type

string

_property_ `created_at` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite.created_at "Permalink to this definition")Type

datetime.datetime

_property_ `head_branch` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite.head_branch "Permalink to this definition")Type

string

_property_ `head_commit` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite.head_commit "Permalink to this definition")Type

[`github.GitCommit.GitCommit`](https://pygithub.readthedocs.io/en/stable/github_objects/GitCommit.html#github.GitCommit.GitCommit "github.GitCommit.GitCommit")

_property_ `head_sha` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite.head_sha "Permalink to this definition")Type

string

_property_ `id` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite.id "Permalink to this definition")Type

int

_property_ `latest_check_runs_count` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite.latest_check_runs_count "Permalink to this definition")Type

int

_property_ `pull_requests` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite.pull_requests "Permalink to this definition")Type

list of [`github.PullRequest.PullRequest`](https://pygithub.readthedocs.io/en/stable/github_objects/PullRequest.html#github.PullRequest.PullRequest "github.PullRequest.PullRequest")

_property_ `repository` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite.repository "Permalink to this definition")Type

[`github.Repository.Repository`](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository "github.Repository.Repository")

_property_ `status` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite.status "Permalink to this definition")Type

string

_property_ `updated_at` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite.updated_at "Permalink to this definition")Type

datetime.datetime

_property_ `url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite.url "Permalink to this definition")Type

string

`rerequest`() → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite.rerequest "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/check-suites/{check\_suite\_id}/rerequest](https://docs.github.com/en/rest/reference/checks#rerequest-a-check-suite)

Return type

bool

`get_check_runs`( _check\_name: Opt\[str\] = NotSet_, _status: Opt\[str\] = NotSet_, _filter: Opt\[str\] = NotSet_) → PaginatedList\[CheckRun\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite.get_check_runs "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/check-suites/{check\_suite\_id}/check-runs](https://docs.github.com/en/rest/reference/checks#list-check-runs-in-a-check-suite)