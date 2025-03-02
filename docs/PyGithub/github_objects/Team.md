- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- Team
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/Team.rst.txt)

* * *

# Team [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html\#team "Permalink to this headline")

_class_ `github.Team.` `Team` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team "Permalink to this definition")

This class represents Teams.

The reference can be found here
[https://docs.github.com/en/rest/reference/teams](https://docs.github.com/en/rest/reference/teams)

The OpenAPI schema can be found at
\- /components/schemas/nullable-team-simple
\- /components/schemas/team
\- /components/schemas/team-full
\- /components/schemas/team-simple

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


`add_to_members`( _member: NamedUser_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.add_to_members "Permalink to this definition")

This API call is deprecated. Use add\_membership instead.
[https://docs.github.com/en/rest/reference/teams#add-or-update-team-membership-for-a-user-legacy](https://docs.github.com/en/rest/reference/teams#add-or-update-team-membership-for-a-user-legacy)

Calls

[PUT /teams/{id}/members/{user}](https://docs.github.com/en/rest/reference/teams)

`add_membership`( _member: NamedUser_, _role: Opt\[str\] = NotSet_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.add_membership "Permalink to this definition")Calls

[PUT /teams/{id}/memberships/{user}](https://docs.github.com/en/rest/reference/teams)

`get_team_membership`( _member: str \| NamedUser_) → Membership [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.get_team_membership "Permalink to this definition")Calls

[GET /orgs/{org}/memberships/team/{team\_id}/{username}](https://docs.github.com/en/rest/reference/teams#get-team-membership-for-a-user)

`add_to_repos`( _repo: Repository_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.add_to_repos "Permalink to this definition")Calls

[PUT /teams/{id}/repos/{org}/{repo}](https://docs.github.com/en/rest/reference/teams)

`get_repo_permission`( _repo: Repository_) → Permissions \| None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.get_repo_permission "Permalink to this definition")Calls

[GET /teams/{id}/repos/{org}/{repo}](https://docs.github.com/en/rest/reference/teams)

`set_repo_permission`( _repo: Repository_, _permission: str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.set_repo_permission "Permalink to this definition")Calls

[PUT /teams/{id}/repos/{org}/{repo}](https://docs.github.com/en/rest/reference/teams)

Parameters

- **repo** – [`github.Repository.Repository`](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository "github.Repository.Repository")

- **permission** – string


Return type

None

`update_team_repository`( _repo: Repository_, _permission: str_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.update_team_repository "Permalink to this definition")Calls

[PUT /orgs/{org}/teams/{team\_slug}/repos/{owner}/{repo}](https://docs.github.com/en/rest/reference/teams#check-team-permissions-for-a-repository)

`delete`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.delete "Permalink to this definition")Calls

[DELETE /teams/{id}](https://docs.github.com/en/rest/reference/teams#delete-a-team)

`edit`( _name: str_, _description: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _permission: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _privacy: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _parent\_team\_id: Union\[int_, _github.GithubObject.\_NotSetType\] = NotSet_, _notification\_setting: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.edit "Permalink to this definition")Calls

[PATCH /teams/{id}](https://docs.github.com/en/rest/reference/teams#update-a-team)

`get_teams`() → PaginatedList\[Team\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.get_teams "Permalink to this definition")Calls

[GET /teams/{id}/teams](https://docs.github.com/en/rest/reference/teams#list-teams)

`get_discussions`() → PaginatedList\[TeamDiscussion\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.get_discussions "Permalink to this definition")Calls

[GET /teams/{id}/discussions](https://docs.github.com/en/rest/reference/teams#list-discussions)

`get_members`( _role: Opt\[str\] = NotSet_) → PaginatedList\[NamedUser\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.get_members "Permalink to this definition")Calls

[GET /teams/{id}/members](https://docs.github.com/en/rest/reference/teams#list-team-members)

`get_repos`() → PaginatedList\[Repository\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.get_repos "Permalink to this definition")Calls

[GET /teams/{id}/repos](https://docs.github.com/en/rest/reference/teams)

`invitations`() → PaginatedList\[NamedUser\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.invitations "Permalink to this definition")Calls

[GET /teams/{id}/invitations](https://docs.github.com/en/rest/reference/teams#members)

`has_in_members`( _member: NamedUser_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.has_in_members "Permalink to this definition")Calls

[GET /teams/{id}/members/{user}](https://docs.github.com/en/rest/reference/teams)

`has_in_repos`( _repo: Repository_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.has_in_repos "Permalink to this definition")Calls

[GET /teams/{id}/repos/{owner}/{repo}](https://docs.github.com/en/rest/reference/teams)

`remove_membership`( _member: NamedUser_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.remove_membership "Permalink to this definition")Calls

[DELETE /teams/{team\_id}/memberships/{username}](https://docs.github.com/en/rest/reference/teams#remove-team-membership-for-a-user)

`remove_from_members`( _member: NamedUser_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.remove_from_members "Permalink to this definition")

This API call is deprecated. Use remove\_membership instead:
[https://docs.github.com/en/rest/reference/teams#add-or-update-team-membership-for-a-user-legacy](https://docs.github.com/en/rest/reference/teams#add-or-update-team-membership-for-a-user-legacy)

Calls

[DELETE /teams/{id}/members/{user}](https://docs.github.com/en/rest/reference/teams)

`remove_from_repos`( _repo: Repository_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team.remove_from_repos "Permalink to this definition")Calls

[DELETE /teams/{id}/repos/{owner}/{repo}](https://docs.github.com/en/rest/reference/teams)