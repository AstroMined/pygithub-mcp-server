- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- NamedUser
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/NamedUser.rst.txt)

* * *

# NamedUser [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html\#nameduser "Permalink to this headline")

_class_ `github.NamedUser.` `NamedUser` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "Permalink to this definition")

This class represents NamedUsers.

The reference can be found here
[https://docs.github.com/en/rest/reference/users#get-a-user](https://docs.github.com/en/rest/reference/users#get-a-user)

The OpenAPI schema can be found at
\- /components/schemas/actor
\- /components/schemas/collaborator
\- /components/schemas/contributor
\- /components/schemas/nullable-simple-user
\- /components/schemas/public-user
\- /components/schemas/simple-user
\- /components/schemas/user-search-result-item

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


`get_events`() → PaginatedList\[Event\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser.get_events "Permalink to this definition")Calls

[GET /users/{user}/events](https://docs.github.com/en/rest/reference/activity#events)

`get_followers`() → github.PaginatedList.PaginatedList\[github.NamedUser.NamedUser\]\[github.NamedUser.NamedUser\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser.get_followers "Permalink to this definition")Calls

[GET /users/{user}/followers](https://docs.github.com/en/rest/reference/users#followers)

`get_following`() → github.PaginatedList.PaginatedList\[github.NamedUser.NamedUser\]\[github.NamedUser.NamedUser\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser.get_following "Permalink to this definition")Calls

[GET /users/{user}/following](https://docs.github.com/en/rest/reference/users#followers)

`get_gists`( _since: Opt\[datetime\] = NotSet_) → PaginatedList\[Gist\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser.get_gists "Permalink to this definition")Calls

[GET /users/{user}/gists](https://docs.github.com/en/rest/reference/gists)

`get_keys`() → PaginatedList\[UserKey\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser.get_keys "Permalink to this definition")Calls

[GET /users/{user}/keys](https://docs.github.com/en/rest/reference/users#create-a-public-ssh-key-for-the-authenticated-user)

`get_orgs`() → PaginatedList\[Organization\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser.get_orgs "Permalink to this definition")Calls

[GET /users/{user}/orgs](https://docs.github.com/en/rest/reference/orgs)

`get_projects`( _state: str = 'open'_) → PaginatedList\[Project\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser.get_projects "Permalink to this definition")Calls

[GET /users/{user}/projects](https://docs.github.com/en/rest/reference/projects#list-user-projects)

`get_public_events`() → PaginatedList\[Event\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser.get_public_events "Permalink to this definition")Calls

[GET /users/{user}/events/public](https://docs.github.com/en/rest/reference/activity#events)

`get_public_received_events`() → PaginatedList\[Event\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser.get_public_received_events "Permalink to this definition")Calls

[GET /users/{user}/received\_events/public](https://docs.github.com/en/rest/reference/activity#events)

`get_received_events`() → PaginatedList\[Event\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser.get_received_events "Permalink to this definition")Calls

[GET /users/{user}/received\_events](https://docs.github.com/en/rest/reference/activity#events)

`get_repo`( _name: str_) → Repository [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser.get_repo "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}](https://docs.github.com/en/rest/reference/repos)

`get_repos`( _type: Opt\[str\] = NotSet_, _sort: Opt\[str\] = NotSet_, _direction: Opt\[str\] = NotSet_) → PaginatedList\[Repository\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser.get_repos "Permalink to this definition")Calls

[GET /users/{user}/repos](https://docs.github.com/en/rest/reference/repos)

`get_starred`() → PaginatedList\[Repository\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser.get_starred "Permalink to this definition")Calls

[GET /users/{user}/starred](https://docs.github.com/en/rest/reference/activity#starring)

`get_subscriptions`() → PaginatedList\[Repository\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser.get_subscriptions "Permalink to this definition")Calls

[GET /users/{user}/subscriptions](https://docs.github.com/en/rest/reference/activity#watching)

`get_watched`() → PaginatedList\[Repository\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser.get_watched "Permalink to this definition")Calls

[GET /users/{user}/watched](https://docs.github.com/en/rest/reference/activity#starring)

`has_in_following`( _following: github.NamedUser.NamedUser_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser.has_in_following "Permalink to this definition")Calls

[GET /users/{user}/following/{target\_user}](https://docs.github.com/en/rest/reference/users#check-if-a-user-follows-another-user)

`get_organization_membership`( _org: str \| Organization_) → Membership [¶](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser.get_organization_membership "Permalink to this definition")Calls

[GET /orgs/{org}/memberships/{username}](https://docs.github.com/en/rest/reference/orgs#check-organization-membership-for-a-user)