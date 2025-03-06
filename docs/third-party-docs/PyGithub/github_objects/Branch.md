- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- Branch
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/Branch.rst.txt)

* * *

# Branch [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html\#branch "Permalink to this headline")

_class_ `github.Branch.` `Branch` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch "Permalink to this definition")

This class represents Branches.

The reference can be found here
[https://docs.github.com/en/rest/reference/repos#branches](https://docs.github.com/en/rest/reference/repos#branches)

The OpenAPI schema can be found at
\- /components/schemas/branch-short
\- /components/schemas/branch-with-protection
\- /components/schemas/short-branch

`get_protection`() → BranchProtection [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.get_protection "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/branches/{branch}/protection](https://docs.github.com/en/rest/reference/repos#branches)

`edit_protection`( _strict: Opt\[bool\] = NotSet_, _contexts: Opt\[list\[str\]\] = NotSet_, _enforce\_admins: Opt\[bool\] = NotSet_, _dismissal\_users: Opt\[list\[str\]\] = NotSet_, _dismissal\_teams: Opt\[list\[str\]\] = NotSet_, _dismissal\_apps: Opt\[list\[str\]\] = NotSet_, _dismiss\_stale\_reviews: Opt\[bool\] = NotSet_, _require\_code\_owner\_reviews: Opt\[bool\] = NotSet_, _required\_approving\_review\_count: Opt\[int\] = NotSet_, _user\_push\_restrictions: Opt\[list\[str\]\] = NotSet_, _team\_push\_restrictions: Opt\[list\[str\]\] = NotSet_, _app\_push\_restrictions: Opt\[list\[str\]\] = NotSet_, _required\_linear\_history: Opt\[bool\] = NotSet_, _allow\_force\_pushes: Opt\[bool\] = NotSet_, _required\_conversation\_resolution: Opt\[bool\] = NotSet_, _lock\_branch: Opt\[bool\] = NotSet_, _allow\_fork\_syncing: Opt\[bool\] = NotSet_, _users\_bypass\_pull\_request\_allowances: Opt\[list\[str\]\] = NotSet_, _teams\_bypass\_pull\_request\_allowances: Opt\[list\[str\]\] = NotSet_, _apps\_bypass\_pull\_request\_allowances: Opt\[list\[str\]\] = NotSet_, _block\_creations: Opt\[bool\] = NotSet_, _require\_last\_push\_approval: Opt\[bool\] = NotSet_, _allow\_deletions: Opt\[bool\] = NotSet_, _checks: Opt\[list\[str \| tuple\[str_, _int\]\]\] = NotSet_) → BranchProtection [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.edit_protection "Permalink to this definition")Calls

[PUT /repos/{owner}/{repo}/branches/{branch}/protection](https://docs.github.com/en/rest/reference/repos#get-branch-protection)

NOTE: The GitHub API groups strict and contexts together, both must
be submitted. Take care to pass both as arguments even if only one is
changing. Use edit\_required\_status\_checks() to avoid this.

`remove_protection`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.remove_protection "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/branches/{branch}/protection](https://docs.github.com/en/rest/reference/repos#branches)

`get_required_status_checks`() → RequiredStatusChecks [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.get_required_status_checks "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/branches/{branch}/protection/required\_status\_checks](https://docs.github.com/en/rest/reference/repos#branches)

Return type

[`github.RequiredStatusChecks.RequiredStatusChecks`](https://pygithub.readthedocs.io/en/stable/github_objects/RequiredStatusChecks.html#github.RequiredStatusChecks.RequiredStatusChecks "github.RequiredStatusChecks.RequiredStatusChecks")

`edit_required_status_checks`( _strict: Opt\[bool\] = NotSet_, _contexts: Opt\[list\[str\]\] = NotSet_, _checks: Opt\[list\[str \| tuple\[str_, _int\]\]\] = NotSet_) → RequiredStatusChecks [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.edit_required_status_checks "Permalink to this definition")Calls

[PATCH /repos/{owner}/{repo}/branches/{branch}/protection/required\_status\_checks](https://docs.github.com/en/rest/reference/repos#branches)

`remove_required_status_checks`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.remove_required_status_checks "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/branches/{branch}/protection/required\_status\_checks](https://docs.github.com/en/rest/reference/repos#branches)

`get_required_pull_request_reviews`() → RequiredPullRequestReviews [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.get_required_pull_request_reviews "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/branches/{branch}/protection/required\_pull\_request\_reviews](https://docs.github.com/en/rest/reference/repos#branches)

`edit_required_pull_request_reviews`( _dismissal\_users: Opt\[list\[str\]\] = NotSet_, _dismissal\_teams: Opt\[list\[str\]\] = NotSet_, _dismissal\_apps: Opt\[list\[str\]\] = NotSet_, _dismiss\_stale\_reviews: Opt\[bool\] = NotSet_, _require\_code\_owner\_reviews: Opt\[bool\] = NotSet_, _required\_approving\_review\_count: Opt\[int\] = NotSet_, _require\_last\_push\_approval: Opt\[bool\] = NotSet_) → RequiredStatusChecks [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.edit_required_pull_request_reviews "Permalink to this definition")Calls

[PATCH /repos/{owner}/{repo}/branches/{branch}/protection/required\_pull\_request\_reviews](https://docs.github.com/en/rest/reference/repos#branches)

`remove_required_pull_request_reviews`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.remove_required_pull_request_reviews "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/branches/{branch}/protection/required\_pull\_request\_reviews](https://docs.github.com/en/rest/reference/repos#branches)

`get_admin_enforcement`() → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.get_admin_enforcement "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/branches/{branch}/protection/enforce\_admins](https://docs.github.com/en/rest/reference/repos#branches)

`set_admin_enforcement`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.set_admin_enforcement "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/branches/{branch}/protection/enforce\_admins](https://docs.github.com/en/rest/reference/repos#branches)

`remove_admin_enforcement`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.remove_admin_enforcement "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/branches/{branch}/protection/enforce\_admins](https://docs.github.com/en/rest/reference/repos#branches)

`get_user_push_restrictions`() → PaginatedList\[NamedUser\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.get_user_push_restrictions "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users](https://docs.github.com/en/rest/reference/repos#branches)

`get_team_push_restrictions`() → PaginatedList\[Team\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.get_team_push_restrictions "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams](https://docs.github.com/en/rest/reference/repos#branches)

`add_user_push_restrictions`( _\*users: str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.add_user_push_restrictions "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users](https://docs.github.com/en/rest/reference/repos#branches)

Users

list of strings (user names)

`replace_user_push_restrictions`( _\*users: str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.replace_user_push_restrictions "Permalink to this definition")Calls

[PUT /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users](https://docs.github.com/en/rest/reference/repos#branches)

Users

list of strings (user names)

`remove_user_push_restrictions`( _\*users: str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.remove_user_push_restrictions "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users](https://docs.github.com/en/rest/reference/repos#branches)

Users

list of strings (user names)

`add_team_push_restrictions`( _\*teams: str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.add_team_push_restrictions "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams](https://docs.github.com/en/rest/reference/repos#branches)

Teams

list of strings (team slugs)

`replace_team_push_restrictions`( _\*teams: str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.replace_team_push_restrictions "Permalink to this definition")Calls

[PUT /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams](https://docs.github.com/en/rest/reference/repos#branches)

Teams

list of strings (team slugs)

`remove_team_push_restrictions`( _\*teams: str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.remove_team_push_restrictions "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams](https://docs.github.com/en/rest/reference/repos#branches)

Teams

list of strings (team slugs)

`remove_push_restrictions`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.remove_push_restrictions "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/branches/{branch}/protection/restrictions](https://docs.github.com/en/rest/reference/repos#branches)

`get_required_signatures`() → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.get_required_signatures "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/branches/{branch}/protection/required\_signatures](https://docs.github.com/en/rest/reference/repos#branches)

`add_required_signatures`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.add_required_signatures "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/branches/{branch}/protection/required\_signatures](https://docs.github.com/en/rest/reference/repos#branches)

`remove_required_signatures`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.remove_required_signatures "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/branches/{branch}/protection/required\_signatures](https://docs.github.com/en/rest/reference/repos#branches)

`get_allow_deletions`() → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.get_allow_deletions "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/branches/{branch}/protection/allow\_deletions](https://docs.github.com/en/rest/reference/repos#branches)

`set_allow_deletions`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.set_allow_deletions "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/branches/{branch}/protection/allow\_deletions](https://docs.github.com/en/rest/reference/repos#branches)

`remove_allow_deletions`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch.remove_allow_deletions "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/branches/{branch}/protection/allow\_deletions](https://docs.github.com/en/rest/reference/repos#branches)