- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- AuthenticatedUser
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/AuthenticatedUser.rst.txt)

* * *

# AuthenticatedUser [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html\#authenticateduser "Permalink to this headline")

_class_ `github.AuthenticatedUser.` `AuthenticatedUser` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser "Permalink to this definition")

This class represents AuthenticatedUsers as returned by [https://docs.github.com/en/rest/reference/users#get-the-authenticated-user](https://docs.github.com/en/rest/reference/users#get-the-authenticated-user)

An AuthenticatedUser object can be created by calling `get_user()` on a Github object.

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


`add_to_emails`( _\*emails: str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.add_to_emails "Permalink to this definition")Calls

[POST /user/emails](http://docs.github.com/en/rest/reference/users#emails)

`add_to_following`( _following: NamedUser_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.add_to_following "Permalink to this definition")Calls

[PUT /user/following/{user}](http://docs.github.com/en/rest/reference/users#followers)

`add_to_starred`( _starred: Repository_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.add_to_starred "Permalink to this definition")Calls

[PUT /user/starred/{owner}/{repo}](http://docs.github.com/en/rest/reference/activity#starring)

`add_to_subscriptions`( _subscription: Repository_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.add_to_subscriptions "Permalink to this definition")Calls

[PUT /user/subscriptions/{owner}/{repo}](http://docs.github.com/en/rest/reference/activity#watching)

`add_to_watched`( _watched: Repository_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.add_to_watched "Permalink to this definition")Calls

[PUT /repos/{owner}/{repo}/subscription](http://docs.github.com/en/rest/reference/activity#watching)

`create_authorization`( _scopes: Opt\[list\[str\]\] = NotSet_, _note: Opt\[str\] = NotSet_, _note\_url: Opt\[str\] = NotSet_, _client\_id: Opt\[str\] = NotSet_, _client\_secret: Opt\[str\] = NotSet_, _onetime\_password: str \| None = None_) → Authorization [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.create_authorization "Permalink to this definition")Calls

[POST /authorizations](https://docs.github.com/en/developers/apps/authorizing-oauth-apps)

_static_ `create_fork`( _repo: Repository_, _name: Opt\[str\] = NotSet_, _default\_branch\_only: Opt\[bool\] = NotSet_) → Repository [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.create_fork "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/forks](http://docs.github.com/en/rest/reference/repos#forks)

`create_repo_from_template`( _name: str_, _repo: Repository_, _description: Opt\[str\] = NotSet_, _include\_all\_branches: Opt\[bool\] = NotSet_, _private: Opt\[bool\] = NotSet_) → Repository [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.create_repo_from_template "Permalink to this definition")Calls

[POST /repos/{template\_owner}/{template\_repo}/generate](https://docs.github.com/en/rest/reference/repos#create-a-repository-using-a-template)

`create_gist`( _public: bool, files: dict\[str, InputFileContent\], description: Opt\[str\] = NotSet_) → Gist [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.create_gist "Permalink to this definition")Calls

[POST /gists](http://docs.github.com/en/rest/reference/gists)

`create_key`( _title: str_, _key: str_) → UserKey [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.create_key "Permalink to this definition")Calls

[POST /user/keys](http://docs.github.com/en/rest/reference/users#git-ssh-keys)

Parameters

- **title** – string

- **key** – string


Return type

[`github.UserKey.UserKey`](https://pygithub.readthedocs.io/en/stable/github_objects/UserKey.html#github.UserKey.UserKey "github.UserKey.UserKey")

`create_project`( _name: str_, _body: Opt\[str\] = NotSet_) → Project [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.create_project "Permalink to this definition")Calls

[POST /user/projects](https://docs.github.com/en/rest/reference/projects#create-a-user-project)

Parameters

- **name** – string

- **body** – string


Return type

[`github.Project.Project`](https://pygithub.readthedocs.io/en/stable/github_objects/Project.html#github.Project.Project "github.Project.Project")

`create_repo`( _name: str_, _description: Opt\[str\] = NotSet_, _homepage: Opt\[str\] = NotSet_, _private: Opt\[bool\] = NotSet_, _has\_issues: Opt\[bool\] = NotSet_, _has\_wiki: Opt\[bool\] = NotSet_, _has\_downloads: Opt\[bool\] = NotSet_, _has\_projects: Opt\[bool\] = NotSet_, _has\_discussions: Opt\[bool\] = NotSet_, _auto\_init: Opt\[bool\] = NotSet_, _license\_template: Opt\[str\] = NotSet_, _gitignore\_template: Opt\[str\] = NotSet_, _allow\_squash\_merge: Opt\[bool\] = NotSet_, _allow\_merge\_commit: Opt\[bool\] = NotSet_, _allow\_rebase\_merge: Opt\[bool\] = NotSet_, _delete\_branch\_on\_merge: Opt\[bool\] = NotSet_) → Repository [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.create_repo "Permalink to this definition")Calls

[POST /user/repos](http://docs.github.com/en/rest/reference/repos)

`edit`( _name: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _email: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _blog: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _company: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _location: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _hireable: Union\[bool_, _github.GithubObject.\_NotSetType\] = NotSet_, _bio: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.edit "Permalink to this definition")Calls

[PATCH /user](http://docs.github.com/en/rest/reference/users)

`get_authorization`( _id: int_) → Authorization [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_authorization "Permalink to this definition")Calls

[GET /authorizations/{id}](https://docs.github.com/en/developers/apps/authorizing-oauth-apps)

`get_authorizations`() → PaginatedList\[Authorization\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_authorizations "Permalink to this definition")Calls

[GET /authorizations](https://docs.github.com/en/developers/apps/authorizing-oauth-apps)

`get_emails`() → list\[EmailData\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_emails "Permalink to this definition")Calls

[GET /user/emails](http://docs.github.com/en/rest/reference/users#emails)

`get_events`() → PaginatedList\[Event\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_events "Permalink to this definition")Calls

[GET /events](http://docs.github.com/en/rest/reference/activity#events)

`get_followers`() → PaginatedList\[NamedUser\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_followers "Permalink to this definition")Calls

[GET /user/followers](http://docs.github.com/en/rest/reference/users#followers)

`get_following`() → PaginatedList\[NamedUser\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_following "Permalink to this definition")Calls

[GET /user/following](http://docs.github.com/en/rest/reference/users#followers)

`get_gists`( _since: Opt\[datetime\] = NotSet_) → PaginatedList\[Gist\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_gists "Permalink to this definition")Calls

[GET /gists](http://docs.github.com/en/rest/reference/gists)

Parameters

**since** – datetime format YYYY-MM-DDTHH:MM:SSZ

Return type

`PaginatedList` of [`github.Gist.Gist`](https://pygithub.readthedocs.io/en/stable/github_objects/Gist.html#github.Gist.Gist "github.Gist.Gist")

`get_issues`( _filter: Opt\[str\] = NotSet_, _state: Opt\[str\] = NotSet_, _labels: Opt\[list\[Label\]\] = NotSet_, _sort: Opt\[str\] = NotSet_, _direction: Opt\[str\] = NotSet_, _since: Opt\[datetime\] = NotSet_) → PaginatedList\[Issue\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_issues "Permalink to this definition")Calls

[GET /issues](http://docs.github.com/en/rest/reference/issues)

`get_user_issues`( _filter: Opt\[str\] = NotSet_, _state: Opt\[str\] = NotSet_, _labels: Opt\[list\[Label\]\] = NotSet_, _sort: Opt\[str\] = NotSet_, _direction: Opt\[str\] = NotSet_, _since: Opt\[datetime\] = NotSet_) → PaginatedList\[Issue\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_user_issues "Permalink to this definition")Calls

[GET /user/issues](http://docs.github.com/en/rest/reference/issues)

`get_key`( _id: int_) → UserKey [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_key "Permalink to this definition")Calls

[GET /user/keys/{id}](http://docs.github.com/en/rest/reference/users#git-ssh-keys)

`get_keys`() → PaginatedList\[UserKey\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_keys "Permalink to this definition")Calls

[GET /user/keys](http://docs.github.com/en/rest/reference/users#git-ssh-keys)

`get_notification`( _id: str_) → Notification [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_notification "Permalink to this definition")Calls

[GET /notifications/threads/{id}](http://docs.github.com/en/rest/reference/activity#notifications)

`get_notifications`( _all: Opt\[bool\] = NotSet_, _participating: Opt\[bool\] = NotSet_, _since: Opt\[datetime\] = NotSet_, _before: Opt\[datetime\] = NotSet_) → PaginatedList\[Notification\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_notifications "Permalink to this definition")Calls

[GET /notifications](http://docs.github.com/en/rest/reference/activity#notifications)

`get_organization_events`( _org: Organization_) → PaginatedList\[Event\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_organization_events "Permalink to this definition")Calls

[GET /users/{user}/events/orgs/{org}](http://docs.github.com/en/rest/reference/activity#events)

`get_orgs`() → PaginatedList\[Organization\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_orgs "Permalink to this definition")Calls

[GET /user/orgs](http://docs.github.com/en/rest/reference/orgs)

`get_repo`( _name: str_) → Repository [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_repo "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}](http://docs.github.com/en/rest/reference/repos)

`get_repos`( _visibility: Opt\[str\] = NotSet_, _affiliation: Opt\[str\] = NotSet_, _type: Opt\[str\] = NotSet_, _sort: Opt\[str\] = NotSet_, _direction: Opt\[str\] = NotSet_) → PaginatedList\[Repository\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_repos "Permalink to this definition")Calls

[GET /user/repos](http://docs.github.com/en/rest/reference/repos)

`get_starred`() → PaginatedList\[Repository\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_starred "Permalink to this definition")Calls

[GET /user/starred](http://docs.github.com/en/rest/reference/activity#starring)

`get_starred_gists`() → PaginatedList\[Gist\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_starred_gists "Permalink to this definition")Calls

[GET /gists/starred](http://docs.github.com/en/rest/reference/gists)

`get_subscriptions`() → PaginatedList\[Repository\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_subscriptions "Permalink to this definition")Calls

[GET /user/subscriptions](http://docs.github.com/en/rest/reference/activity#watching)

`get_teams`() → PaginatedList\[Team\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_teams "Permalink to this definition")Calls

[GET /user/teams](http://docs.github.com/en/rest/reference/teams)

`get_watched`() → PaginatedList\[Repository\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_watched "Permalink to this definition")Calls

[GET /user/subscriptions](http://docs.github.com/en/rest/reference/activity#watching)

`get_installations`() → PaginatedList\[Installation\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_installations "Permalink to this definition")Calls

[GET /user/installations](http://docs.github.com/en/rest/reference/apps)

`has_in_following`( _following: NamedUser_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.has_in_following "Permalink to this definition")Calls

[GET /user/following/{user}](http://docs.github.com/en/rest/reference/users#followers)

`has_in_starred`( _starred: Repository_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.has_in_starred "Permalink to this definition")Calls

[GET /user/starred/{owner}/{repo}](http://docs.github.com/en/rest/reference/activity#starring)

`has_in_subscriptions`( _subscription: Repository_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.has_in_subscriptions "Permalink to this definition")Calls

[GET /user/subscriptions/{owner}/{repo}](http://docs.github.com/en/rest/reference/activity#watching)

`has_in_watched`( _watched: Repository_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.has_in_watched "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/subscription](http://docs.github.com/en/rest/reference/activity#watching)

`mark_notifications_as_read`( _last\_read\_at: datetime \| None = None_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.mark_notifications_as_read "Permalink to this definition")Calls

[PUT /notifications](https://docs.github.com/en/rest/reference/activity#notifications)

`remove_from_emails`( _\*emails: str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.remove_from_emails "Permalink to this definition")Calls

[DELETE /user/emails](http://docs.github.com/en/rest/reference/users#emails)

`remove_from_following`( _following: NamedUser_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.remove_from_following "Permalink to this definition")Calls

[DELETE /user/following/{user}](http://docs.github.com/en/rest/reference/users#followers)

`remove_from_starred`( _starred: Repository_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.remove_from_starred "Permalink to this definition")Calls

[DELETE /user/starred/{owner}/{repo}](http://docs.github.com/en/rest/reference/activity#starring)

`remove_from_subscriptions`( _subscription: Repository_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.remove_from_subscriptions "Permalink to this definition")Calls

[DELETE /user/subscriptions/{owner}/{repo}](http://docs.github.com/en/rest/reference/activity#watching)

`remove_from_watched`( _watched: Repository_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.remove_from_watched "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/subscription](http://docs.github.com/en/rest/reference/activity#watching)

`accept_invitation`( _invitation: Invitation \| int_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.accept_invitation "Permalink to this definition")Calls

[PATCH /user/repository\_invitations/{invitation\_id}](https://docs.github.com/en/rest/reference/repos/invitations#)

`get_invitations`() → PaginatedList\[Invitation\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_invitations "Permalink to this definition")Calls

[GET /user/repository\_invitations](https://docs.github.com/en/rest/reference/repos#invitations)

`create_migration`( _repos: list\[Repository\] \| tuple\[Repository\], lock\_repositories: Opt\[bool\] = NotSet, exclude\_attachments: Opt\[bool\] = NotSet_) → Migration [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.create_migration "Permalink to this definition")Calls

[POST /user/migrations](https://docs.github.com/en/rest/reference/migrations)

`get_migrations`() → PaginatedList\[Migration\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_migrations "Permalink to this definition")Calls

[GET /user/migrations](https://docs.github.com/en/rest/reference/migrations)

`get_organization_memberships`() → PaginatedList\[Membership\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_organization_memberships "Permalink to this definition")Calls

[GET /user/memberships/orgs/](https://docs.github.com/en/rest/orgs/members#list-organization-memberships-for-the-authenticated-user)

`get_organization_membership`( _org: str_) → Membership [¶](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_organization_membership "Permalink to this definition")Calls

[GET /user/memberships/orgs/{org}](https://docs.github.com/en/rest/reference/orgs#get-an-organization-membership-for-the-authenticated-user)