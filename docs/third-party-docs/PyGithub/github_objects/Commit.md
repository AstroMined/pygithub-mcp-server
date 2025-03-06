- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- Commit
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/Commit.rst.txt)

* * *

# Commit [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html\#commit "Permalink to this headline")

_class_ `github.Commit.` `Commit` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html#github.Commit.Commit "Permalink to this definition")

This class represents Commits.

The reference can be found here
[https://docs.github.com/en/rest/commits/commits#get-a-commit-object](https://docs.github.com/en/rest/commits/commits#get-a-commit-object)

The OpenAPI schema can be found at
\- /components/schemas/branch-short/properties/commit
\- /components/schemas/commit
\- /components/schemas/commit-search-result-item
\- /components/schemas/commit-search-result-item/properties/parents/items
\- /components/schemas/commit/properties/parents/items
\- /components/schemas/short-branch/properties/commit
\- /components/schemas/tag/properties/commit

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


`create_comment`( _body: str_, _line: Opt\[int\] = NotSet_, _path: Opt\[str\] = NotSet_, _position: Opt\[int\] = NotSet_) → CommitComment [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html#github.Commit.Commit.create_comment "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/commits/{sha}/comments](https://docs.github.com/en/rest/reference/repos#comments)

`create_status`( _state: str_, _target\_url: Opt\[str\] = NotSet_, _description: Opt\[str\] = NotSet_, _context: Opt\[str\] = NotSet_) → CommitStatus [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html#github.Commit.Commit.create_status "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/statuses/{sha}](https://docs.github.com/en/rest/reference/repos#statuses)

`get_branches_where_head`() → list\[Branch\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html#github.Commit.Commit.get_branches_where_head "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/commits/{commit\_sha}/branches-where-head](https://docs.github.com/rest/commits/commits#list-branches-for-head-commit)

`get_comments`() → PaginatedList\[CommitComment\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html#github.Commit.Commit.get_comments "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/commits/{sha}/comments](https://docs.github.com/en/rest/reference/repos#comments)

`get_statuses`() → PaginatedList\[CommitStatus\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html#github.Commit.Commit.get_statuses "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/statuses/{ref}](https://docs.github.com/en/rest/reference/repos#statuses)

`get_combined_status`() → CommitCombinedStatus [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html#github.Commit.Commit.get_combined_status "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/commits/{ref}/status/](http://docs.github.com/en/rest/reference/repos#statuses)

`get_pulls`() → PaginatedList\[PullRequest\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html#github.Commit.Commit.get_pulls "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/commits/{sha}/pulls](https://docs.github.com/en/rest/reference/repos#list-pull-requests-associated-with-a-commit)

`get_check_runs`( _check\_name: Opt\[str\] = NotSet_, _status: Opt\[str\] = NotSet_, _filter: Opt\[str\] = NotSet_) → PaginatedList\[CheckRun\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html#github.Commit.Commit.get_check_runs "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/commits/{sha}/check-runs](https://docs.github.com/en/rest/reference/checks#list-check-runs-for-a-git-reference)

`get_check_suites`( _app\_id: Opt\[int\] = NotSet_, _check\_name: Opt\[str\] = NotSet_) → PaginatedList\[CheckSuite\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html#github.Commit.Commit.get_check_suites "Permalink to this definition")Class

[GET /repos/{owner}/{repo}/commits/{ref}/check-suites](https://docs.github.com/en/rest/reference/checks#list-check-suites-for-a-git-reference)