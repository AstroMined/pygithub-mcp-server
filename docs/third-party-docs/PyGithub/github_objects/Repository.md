- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- Repository
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/Repository.rst.txt)

* * *

# Repository [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html\#repository "Permalink to this headline")

_class_ `github.Repository.` `Repository` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository "Permalink to this definition")

This class represents Repositories.

The reference can be found here
[https://docs.github.com/en/rest/reference/repos](https://docs.github.com/en/rest/reference/repos)

The OpenAPI schema can be found at
\- /components/schemas/event/properties/repo
\- /components/schemas/full-repository
\- /components/schemas/minimal-repository
\- /components/schemas/nullable-repository
\- /components/schemas/pull-request-minimal/properties/base/properties/repo
\- /components/schemas/pull-request-minimal/properties/head/properties/repo
\- /components/schemas/repository
\- /components/schemas/simple-repository

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

- **url** – url of this instance, overrides attributes\[‘url’\]

- **accept** – use this accept header when completing this instance


_property_ `allow_auto_merge` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.allow_auto_merge "Permalink to this definition")Type

bool

_property_ `allow_forking` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.allow_forking "Permalink to this definition")Type

bool

_property_ `allow_merge_commit` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.allow_merge_commit "Permalink to this definition")Type

bool

_property_ `allow_rebase_merge` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.allow_rebase_merge "Permalink to this definition")Type

bool

_property_ `allow_squash_merge` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.allow_squash_merge "Permalink to this definition")Type

bool

_property_ `allow_update_branch` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.allow_update_branch "Permalink to this definition")Type

bool

_property_ `archive_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.archive_url "Permalink to this definition")Type

string

_property_ `archived` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.archived "Permalink to this definition")Type

bool

_property_ `assignees_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.assignees_url "Permalink to this definition")Type

string

_property_ `blobs_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.blobs_url "Permalink to this definition")Type

string

_property_ `branches_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.branches_url "Permalink to this definition")Type

string

_property_ `clone_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.clone_url "Permalink to this definition")Type

string

_property_ `collaborators_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.collaborators_url "Permalink to this definition")Type

string

_property_ `comments_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.comments_url "Permalink to this definition")Type

string

_property_ `commits_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.commits_url "Permalink to this definition")Type

string

_property_ `compare_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.compare_url "Permalink to this definition")Type

string

_property_ `contents_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.contents_url "Permalink to this definition")Type

string

_property_ `contributors_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.contributors_url "Permalink to this definition")Type

string

_property_ `created_at` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.created_at "Permalink to this definition")Type

datetime

_property_ `custom_properties` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.custom_properties "Permalink to this definition")Type

dict\[str, None \| str \| list\]

_property_ `default_branch` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.default_branch "Permalink to this definition")Type

string

_property_ `delete_branch_on_merge` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.delete_branch_on_merge "Permalink to this definition")Type

bool

_property_ `deployments_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.deployments_url "Permalink to this definition")Type

string

_property_ `description` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.description "Permalink to this definition")Type

string

_property_ `downloads_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.downloads_url "Permalink to this definition")Type

string

_property_ `events_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.events_url "Permalink to this definition")Type

string

_property_ `fork` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.fork "Permalink to this definition")Type

bool

_property_ `forks` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.forks "Permalink to this definition")Type

integer

_property_ `forks_count` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.forks_count "Permalink to this definition")Type

integer

_property_ `forks_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.forks_url "Permalink to this definition")Type

string

_property_ `full_name` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.full_name "Permalink to this definition")Type

string

_property_ `git_commits_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.git_commits_url "Permalink to this definition")Type

string

_property_ `git_refs_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.git_refs_url "Permalink to this definition")Type

string

_property_ `git_tags_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.git_tags_url "Permalink to this definition")Type

string

_property_ `git_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.git_url "Permalink to this definition")Type

string

_property_ `has_discussions` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.has_discussions "Permalink to this definition")Type

bool

_property_ `has_downloads` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.has_downloads "Permalink to this definition")Type

bool

_property_ `has_issues` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.has_issues "Permalink to this definition")Type

bool

_property_ `has_pages` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.has_pages "Permalink to this definition")Type

bool

_property_ `has_projects` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.has_projects "Permalink to this definition")Type

bool

_property_ `has_wiki` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.has_wiki "Permalink to this definition")Type

bool

_property_ `homepage` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.homepage "Permalink to this definition")Type

string

_property_ `hooks_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.hooks_url "Permalink to this definition")Type

string

_property_ `html_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.html_url "Permalink to this definition")Type

string

_property_ `id` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.id "Permalink to this definition")Type

integer

_property_ `is_template` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.is_template "Permalink to this definition")Type

bool

_property_ `issue_comment_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.issue_comment_url "Permalink to this definition")Type

string

_property_ `issue_events_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.issue_events_url "Permalink to this definition")Type

string

_property_ `issues_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.issues_url "Permalink to this definition")Type

string

_property_ `keys_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.keys_url "Permalink to this definition")Type

string

_property_ `labels_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.labels_url "Permalink to this definition")Type

string

_property_ `language` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.language "Permalink to this definition")Type

string

_property_ `languages_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.languages_url "Permalink to this definition")Type

string

_property_ `merge_commit_message` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.merge_commit_message "Permalink to this definition")Type

string

_property_ `merge_commit_title` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.merge_commit_title "Permalink to this definition")Type

string

_property_ `merges_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.merges_url "Permalink to this definition")Type

string

_property_ `milestones_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.milestones_url "Permalink to this definition")Type

string

_property_ `mirror_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.mirror_url "Permalink to this definition")Type

string

_property_ `name` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.name "Permalink to this definition")Type

string

_property_ `network_count` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.network_count "Permalink to this definition")Type

integer

_property_ `notifications_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.notifications_url "Permalink to this definition")Type

string

_property_ `open_issues` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.open_issues "Permalink to this definition")Type

integer

_property_ `open_issues_count` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.open_issues_count "Permalink to this definition")Type

integer

_property_ `organization` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.organization "Permalink to this definition")Type

[`github.Organization.Organization`](https://pygithub.readthedocs.io/en/stable/github_objects/Organization.html#github.Organization.Organization "github.Organization.Organization")

_property_ `owner` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.owner "Permalink to this definition")Type

[`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser")

_property_ `parent` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.parent "Permalink to this definition")Type

[`github.Repository.Repository`](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository "github.Repository.Repository")

_property_ `permissions` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.permissions "Permalink to this definition")Type

[`github.Permissions.Permissions`](https://pygithub.readthedocs.io/en/stable/github_objects/Permissions.html#github.Permissions.Permissions "github.Permissions.Permissions")

_property_ `private` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.private "Permalink to this definition")Type

bool

_property_ `pulls_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.pulls_url "Permalink to this definition")Type

string

_property_ `pushed_at` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.pushed_at "Permalink to this definition")Type

datetime

_property_ `releases_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.releases_url "Permalink to this definition")Type

string

_property_ `security_and_analysis` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.security_and_analysis "Permalink to this definition")Type

[`github.SecurityAndAnalysis.SecurityAndAnalysis`](https://pygithub.readthedocs.io/en/stable/github_objects/SecurityAndAnalysis.html#github.SecurityAndAnalysis.SecurityAndAnalysis "github.SecurityAndAnalysis.SecurityAndAnalysis")

_property_ `size` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.size "Permalink to this definition")Type

integer

_property_ `source` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.source "Permalink to this definition")Type

[`github.Repository.Repository`](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository "github.Repository.Repository")

_property_ `squash_merge_commit_message` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.squash_merge_commit_message "Permalink to this definition")Type

string

_property_ `squash_merge_commit_title` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.squash_merge_commit_title "Permalink to this definition")Type

string

_property_ `ssh_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.ssh_url "Permalink to this definition")Type

string

_property_ `stargazers_count` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.stargazers_count "Permalink to this definition")Type

integer

_property_ `stargazers_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.stargazers_url "Permalink to this definition")Type

string

_property_ `statuses_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.statuses_url "Permalink to this definition")Type

string

_property_ `subscribers_count` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.subscribers_count "Permalink to this definition")Type

integer

_property_ `subscribers_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.subscribers_url "Permalink to this definition")Type

string

_property_ `subscription_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.subscription_url "Permalink to this definition")Type

string

_property_ `svn_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.svn_url "Permalink to this definition")Type

string

_property_ `tags_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.tags_url "Permalink to this definition")Type

string

_property_ `teams_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.teams_url "Permalink to this definition")Type

string

_property_ `topics` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.topics "Permalink to this definition")Type

list of strings

_property_ `trees_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.trees_url "Permalink to this definition")Type

string

_property_ `updated_at` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.updated_at "Permalink to this definition")Type

datetime

_property_ `web_commit_signoff_required` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.web_commit_signoff_required "Permalink to this definition")Type

bool

`add_to_collaborators`( _collaborator: str \| NamedUser_, _permission: Opt\[str\] = NotSet_) → Invitation \| None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.add_to_collaborators "Permalink to this definition")Calls

[PUT /repos/{owner}/{repo}/collaborators/{user}](https://docs.github.com/en/rest/collaborators/collaborators#add-a-repository-collaborator)

Parameters

- **collaborator** – string or [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser")

- **permission** – string ‘pull’, ‘push’, ‘admin’, ‘maintain’, ‘triage’, or a custom repository role name, if the owning organization has defined any


Return type

None

`get_collaborator_permission`( _collaborator: str \| NamedUser_) → str [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_collaborator_permission "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/collaborators/{username}/permission](https://docs.github.com/en/rest/reference/repos#collaborators)

Parameters

**collaborator** – string or [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser")

Return type

string

`get_pending_invitations`() → PaginatedList\[Invitation\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_pending_invitations "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/invitations](https://docs.github.com/en/rest/reference/repos#invitations)

Return type

`PaginatedList` of [`github.Invitation.Invitation`](https://pygithub.readthedocs.io/en/stable/github_objects/Invitation.html#github.Invitation.Invitation "github.Invitation.Invitation")

`remove_invitation`( _invite\_id: int_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.remove_invitation "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/invitations/{invitation\_id}](https://docs.github.com/en/rest/reference/repos#invitations)

Return type

None

`compare`( _base: str_, _head: str_) → Comparison [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.compare "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/compare/{base…:head}](https://docs.github.com/en/rest/commits/commits#compare-two-commits)

Parameters

- **base** – string

- **head** – string


Return type

[`github.Comparison.Comparison`](https://pygithub.readthedocs.io/en/stable/github_objects/Comparison.html#github.Comparison.Comparison "github.Comparison.Comparison")

`create_autolink`( _key\_prefix: str_, _url\_template: str_, _is\_alphanumeric: Union\[bool_, _github.GithubObject.\_NotSetType\] = NotSet_) → github.Autolink.Autolink [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_autolink "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/autolinks](http://docs.github.com/en/rest/reference/repos)

Parameters

- **key\_prefix** – string

- **url\_template** – string

- **is\_alphanumeric** – bool


Return type

[`github.Autolink.Autolink`](https://pygithub.readthedocs.io/en/stable/github_objects/Autolink.html#github.Autolink.Autolink "github.Autolink.Autolink")

`create_git_blob`( _content: str_, _encoding: str_) → GitBlob [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_git_blob "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/git/blobs](https://docs.github.com/en/rest/reference/git#blobs)

Parameters

- **content** – string

- **encoding** – string


Return type

[`github.GitBlob.GitBlob`](https://pygithub.readthedocs.io/en/stable/github_objects/GitBlob.html#github.GitBlob.GitBlob "github.GitBlob.GitBlob")

`create_git_commit`( _message: str, tree: GitTree, parents: list\[GitCommit\], author: Opt\[InputGitAuthor\] = NotSet, committer: Opt\[InputGitAuthor\] = NotSet_) → GitCommit [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_git_commit "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/git/commits](https://docs.github.com/en/rest/reference/git#commits)

Parameters

- **message** – string

- **tree** – [`github.GitTree.GitTree`](https://pygithub.readthedocs.io/en/stable/github_objects/GitTree.html#github.GitTree.GitTree "github.GitTree.GitTree")

- **parents** – list of [`github.GitCommit.GitCommit`](https://pygithub.readthedocs.io/en/stable/github_objects/GitCommit.html#github.GitCommit.GitCommit "github.GitCommit.GitCommit")

- **author** – [`github.InputGitAuthor.InputGitAuthor`](https://pygithub.readthedocs.io/en/stable/utilities.html#github.InputGitAuthor.InputGitAuthor "github.InputGitAuthor.InputGitAuthor")

- **committer** – [`github.InputGitAuthor.InputGitAuthor`](https://pygithub.readthedocs.io/en/stable/utilities.html#github.InputGitAuthor.InputGitAuthor "github.InputGitAuthor.InputGitAuthor")


Return type

[`github.GitCommit.GitCommit`](https://pygithub.readthedocs.io/en/stable/github_objects/GitCommit.html#github.GitCommit.GitCommit "github.GitCommit.GitCommit")

`create_git_ref`( _ref: str_, _sha: str_) → GitRef [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_git_ref "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/git/refs](https://docs.github.com/en/rest/reference/git#references)

Parameters

- **ref** – string

- **sha** – string


Return type

[`github.GitRef.GitRef`](https://pygithub.readthedocs.io/en/stable/github_objects/GitRef.html#github.GitRef.GitRef "github.GitRef.GitRef")

`create_git_tag_and_release`( _tag: str, tag\_message: str, release\_name: Opt\[str\], release\_message: Opt\[str\], object: str, type: str, tagger: Opt\[InputGitAuthor\] = NotSet, draft: bool = False, prerelease: bool = False, generate\_release\_notes: bool = False, make\_latest: str = 'true'_) → GitRelease [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_git_tag_and_release "Permalink to this definition")

Convenience function that calls [`Repository.create_git_tag()`](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_git_tag "github.Repository.Repository.create_git_tag") and [`Repository.create_git_release()`](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_git_release "github.Repository.Repository.create_git_release").

Parameters

- **tag** – string

- **tag\_message** – string

- **release\_name** – string

- **release\_message** – string

- **object** – string

- **type** – string

- **tagger** – :class:github.InputGitAuthor.InputGitAuthor

- **draft** – bool

- **prerelease** – bool

- **generate\_release\_notes** – bool

- **make\_latest** – string


Return type

[`github.GitRelease.GitRelease`](https://pygithub.readthedocs.io/en/stable/github_objects/GitRelease.html#github.GitRelease.GitRelease "github.GitRelease.GitRelease")

`create_git_release`( _tag: str_, _name: Opt\[str\] = NotSet_, _message: Opt\[str\] = NotSet_, _draft: bool = False_, _prerelease: bool = False_, _generate\_release\_notes: bool = False_, _target\_commitish: Opt\[str\] = NotSet_, _make\_latest: str = 'true'_) → GitRelease [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_git_release "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/releases](https://docs.github.com/en/rest/reference/repos#releases)

Parameters

- **tag** – string

- **name** – string

- **message** – string

- **draft** – bool

- **prerelease** – bool

- **generate\_release\_notes** – bool

- **target\_commitish** – string or [`github.Branch.Branch`](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch "github.Branch.Branch") or [`github.Commit.Commit`](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html#github.Commit.Commit "github.Commit.Commit") or [`github.GitCommit.GitCommit`](https://pygithub.readthedocs.io/en/stable/github_objects/GitCommit.html#github.GitCommit.GitCommit "github.GitCommit.GitCommit")

- **make\_latest** – string


Return type

[`github.GitRelease.GitRelease`](https://pygithub.readthedocs.io/en/stable/github_objects/GitRelease.html#github.GitRelease.GitRelease "github.GitRelease.GitRelease")

`create_git_tag`( _tag: str_, _message: str_, _object: str_, _type: str_, _tagger: Opt\[InputGitAuthor\] = NotSet_) → GitTag [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_git_tag "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/git/tags](https://docs.github.com/en/rest/reference/git#tags)

`create_git_tree`( _tree: list\[InputGitTreeElement\], base\_tree: Opt\[GitTree\] = NotSet_) → GitTree [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_git_tree "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/git/trees](https://docs.github.com/en/rest/reference/git#trees)

Parameters

- **tree** – list of [`github.InputGitTreeElement.InputGitTreeElement`](https://pygithub.readthedocs.io/en/stable/utilities.html#github.InputGitTreeElement.InputGitTreeElement "github.InputGitTreeElement.InputGitTreeElement")

- **base\_tree** – [`github.GitTree.GitTree`](https://pygithub.readthedocs.io/en/stable/github_objects/GitTree.html#github.GitTree.GitTree "github.GitTree.GitTree")


Return type

[`github.GitTree.GitTree`](https://pygithub.readthedocs.io/en/stable/github_objects/GitTree.html#github.GitTree.GitTree "github.GitTree.GitTree")

`create_hook`( _name: str, config: dict\[str, str\], events: Opt\[list\[str\]\] = NotSet, active: Opt\[bool\] = NotSet_) → Hook [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_hook "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/hooks](https://docs.github.com/en/rest/reference/repos#webhooks)

Parameters

- **name** – string

- **config** – dict

- **events** – list of string

- **active** – bool


Return type

[`github.Hook.Hook`](https://pygithub.readthedocs.io/en/stable/github_objects/Hook.html#github.Hook.Hook "github.Hook.Hook")

`create_issue`( _title: str_, _body: Opt\[str\] = NotSet_, _assignee: NamedUser \| Opt\[str\] = NotSet_, _milestone: Opt\[Milestone\] = NotSet_, _labels: list\[Label\] \| Opt\[list\[str\]\] = NotSet_, _assignees: Opt\[list\[str\]\] \| list\[NamedUser\] = NotSet_) → Issue [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_issue "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/issues](https://docs.github.com/en/rest/reference/issues)

Parameters

- **title** – string

- **body** – string

- **assignee** – string or [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser")

- **assignees** – list of string or [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser")

- **milestone** – [`github.Milestone.Milestone`](https://pygithub.readthedocs.io/en/stable/github_objects/Milestone.html#github.Milestone.Milestone "github.Milestone.Milestone")

- **labels** – list of [`github.Label.Label`](https://pygithub.readthedocs.io/en/stable/github_objects/Label.html#github.Label.Label "github.Label.Label")


Return type

[`github.Issue.Issue`](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue "github.Issue.Issue")

`create_key`( _title: str_, _key: str_, _read\_only: bool = False_) → RepositoryKey [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_key "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/keys](https://docs.github.com/en/rest/reference/repos#deploy-keys)

Parameters

- **title** – string

- **key** – string

- **read\_only** – bool


Return type

[`github.RepositoryKey.RepositoryKey`](https://pygithub.readthedocs.io/en/stable/github_objects/RepositoryKey.html#github.RepositoryKey.RepositoryKey "github.RepositoryKey.RepositoryKey")

`create_label`( _name: str_, _color: str_, _description: Opt\[str\] = NotSet_) → Label [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_label "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/labels](https://docs.github.com/en/rest/reference/issues#labels)

Parameters

- **name** – string

- **color** – string

- **description** – string


Return type

[`github.Label.Label`](https://pygithub.readthedocs.io/en/stable/github_objects/Label.html#github.Label.Label "github.Label.Label")

`create_milestone`( _title: str_, _state: Opt\[str\] = NotSet_, _description: Opt\[str\] = NotSet_, _due\_on: Opt\[date\] = NotSet_) → Milestone [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_milestone "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/milestones](https://docs.github.com/en/rest/reference/issues#milestones)

Parameters

- **title** – string

- **state** – string

- **description** – string

- **due\_on** – datetime


Return type

[`github.Milestone.Milestone`](https://pygithub.readthedocs.io/en/stable/github_objects/Milestone.html#github.Milestone.Milestone "github.Milestone.Milestone")

`create_project`( _name: str_, _body: Opt\[str\] = NotSet_) → Project [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_project "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/projects](https://docs.github.com/en/rest/reference/projects#create-a-repository-project)

Parameters

- **name** – string

- **body** – string


Return type

[`github.Project.Project`](https://pygithub.readthedocs.io/en/stable/github_objects/Project.html#github.Project.Project "github.Project.Project")

`create_pull`( _base: str_, _head: str_, _\*_, _title: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _body: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _maintainer\_can\_modify: Union\[bool_, _github.GithubObject.\_NotSetType\] = NotSet_, _draft: Union\[bool_, _github.GithubObject.\_NotSetType\] = NotSet_, _issue: Union\[github.Issue.Issue_, _github.GithubObject.\_NotSetType\] = NotSet_) → github.PullRequest.PullRequest [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_pull "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/pulls](https://docs.github.com/en/free-pro-team@latest/rest/pulls/pulls?apiVersion=2022-11-28#create-a-pull-request)

`create_repository_advisory`( _summary: str_, _description: str_, _severity\_or\_cvss\_vector\_string: str_, _cve\_id: str \| None = None_, _vulnerabilities: Iterable\[github.AdvisoryVulnerability.AdvisoryVulnerabilityInput\] \| None = None_, _cwe\_ids: Iterable\[str\] \| None = None_, _credits: Iterable\[github.AdvisoryCredit.AdvisoryCredit\] \| None = None_) → github.RepositoryAdvisory.RepositoryAdvisory [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_repository_advisory "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/security-advisories](https://docs.github.com/en/rest/security-advisories/repository-advisories)

Parameters

- **summary** – string

- **description** – string

- **severity\_or\_cvss\_vector\_string** – string

- **cve\_id** – string

- **vulnerabilities** – iterable of `github.AdvisoryVulnerability.AdvisoryVulnerabilityInput`

- **cwe\_ids** – iterable of string

- **credits** – iterable of [`github.AdvisoryCredit.AdvisoryCredit`](https://pygithub.readthedocs.io/en/stable/github_objects/AdvisoryCredit.html#github.AdvisoryCredit.AdvisoryCredit "github.AdvisoryCredit.AdvisoryCredit")


Return type

[`github.RepositoryAdvisory.RepositoryAdvisory`](https://pygithub.readthedocs.io/en/stable/github_objects/RepositoryAdvisory.html#github.RepositoryAdvisory.RepositoryAdvisory "github.RepositoryAdvisory.RepositoryAdvisory")

`report_security_vulnerability`( _summary: str_, _description: str_, _severity\_or\_cvss\_vector\_string: str_, _cve\_id: str \| None = None_, _vulnerabilities: Iterable\[github.AdvisoryVulnerability.AdvisoryVulnerabilityInput\] \| None = None_, _cwe\_ids: Iterable\[str\] \| None = None_, _credits: Iterable\[github.AdvisoryCredit.AdvisoryCredit\] \| None = None_) → github.RepositoryAdvisory.RepositoryAdvisory [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.report_security_vulnerability "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/security-advisories/reports](https://docs.github.com/en/rest/security-advisories/repository-advisories#privately-report-a-security-vulnerability)

Parameters

- **summary** – string

- **description** – string

- **severity\_or\_cvss\_vector\_string** – string

- **cve\_id** – string

- **vulnerabilities** – iterable of `github.AdvisoryVulnerability.AdvisoryVulnerabilityInput`

- **cwe\_ids** – iterable of string

- **credits** – iterable of [`github.AdvisoryCredit.AdvisoryCredit`](https://pygithub.readthedocs.io/en/stable/github_objects/AdvisoryCredit.html#github.AdvisoryCredit.AdvisoryCredit "github.AdvisoryCredit.AdvisoryCredit")


Return type

[`github.RepositoryAdvisory.RepositoryAdvisory`](https://pygithub.readthedocs.io/en/stable/github_objects/RepositoryAdvisory.html#github.RepositoryAdvisory.RepositoryAdvisory "github.RepositoryAdvisory.RepositoryAdvisory")

`create_repository_dispatch`( _event\_type: str_, _client\_payload: Opt\[dict\[str_, _Any\]\] = NotSet_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_repository_dispatch "Permalink to this definition")Calls

POST /repos/{owner}/{repo}/dispatches < [https://docs.github.com/en/rest/repos#create-a-repository-dispatch-event](https://docs.github.com/en/rest/repos#create-a-repository-dispatch-event) >

Parameters

- **event\_type** – string

- **client\_payload** – dict


Return type

bool

`create_secret`( _secret\_name: str_, _unencrypted\_value: str_, _secret\_type: str = 'actions'_) → github.Secret.Secret [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_secret "Permalink to this definition")Calls

[PUT /repos/{owner}/{repo}/{secret\_type}/secrets/{secret\_name}](https://docs.github.com/en/rest/actions/secrets#get-a-repository-secret)

Parameters

**secret\_type** – string options actions or dependabot

`get_secrets`( _secret\_type: str = 'actions'_) → github.PaginatedList.PaginatedList\[github.Secret.Secret\]\[github.Secret.Secret\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_secrets "Permalink to this definition")

Gets all repository secrets :param secret\_type: string options actions or dependabot.

`get_secret`( _secret\_name: str_, _secret\_type: str = 'actions'_) → github.Secret.Secret [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_secret "Permalink to this definition")Calls

‘GET /repos/{owner}/{repo}/actions/secrets/{secret\_name} < [https://docs.github.com/en/rest/actions/secrets#get-an-organization-secret](https://docs.github.com/en/rest/actions/secrets#get-an-organization-secret) >\`\_

Parameters

**secret\_type** – string options actions or dependabot

`create_variable`( _variable\_name: str_, _value: str_) → github.Variable.Variable [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_variable "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/actions/variables/{variable\_name}](https://docs.github.com/en/rest/actions/variables#create-a-repository-variable)

`get_variables`() → github.PaginatedList.PaginatedList\[github.Variable.Variable\]\[github.Variable.Variable\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_variables "Permalink to this definition")

Gets all repository variables :rtype: `PaginatedList` of [`github.Variable.Variable`](https://pygithub.readthedocs.io/en/stable/github_objects/Variable.html#github.Variable.Variable "github.Variable.Variable")

`get_variable`( _variable\_name: str_) → github.Variable.Variable [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_variable "Permalink to this definition")Calls

‘GET /orgs/{org}/actions/variables/{variable\_name} < [https://docs.github.com/en/rest/actions/variables#get-an-organization-variable](https://docs.github.com/en/rest/actions/variables#get-an-organization-variable) >\`\_

Parameters

**variable\_name** – string

Return type

[github.Variable.Variable](https://pygithub.readthedocs.io/en/stable/github_objects/Variable.html#github.Variable.Variable "github.Variable.Variable")

`delete_secret`( _secret\_name: str_, _secret\_type: str = 'actions'_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.delete_secret "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/{secret\_type}/secrets/{secret\_name}](https://docs.github.com/en/rest/reference/actions#delete-a-repository-secret)

Parameters

- **secret\_name** – string

- **secret\_type** – string options actions or dependabot


Return type

bool

`delete_variable`( _variable\_name: str_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.delete_variable "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/actions/variables/{variable\_name}](https://docs.github.com/en/rest/reference/actions#delete-a-repository-variable)

Parameters

**variable\_name** – string

Return type

bool

`create_source_import`( _vcs: str_, _vcs\_url: str_, _vcs\_username: Opt\[str\] = NotSet_, _vcs\_password: Opt\[str\] = NotSet_) → SourceImport [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_source_import "Permalink to this definition")Calls

[PUT /repos/{owner}/{repo}/import](https://docs.github.com/en/rest/reference/migrations#start-an-import)

Parameters

- **vcs** – string

- **vcs\_url** – string

- **vcs\_username** – string

- **vcs\_password** – string


Return type

[`github.SourceImport.SourceImport`](https://pygithub.readthedocs.io/en/stable/github_objects/SourceImport.html#github.SourceImport.SourceImport "github.SourceImport.SourceImport")

`delete`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.delete "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}](https://docs.github.com/en/rest/reference/repos)

Return type

None

`edit`( _name: str \| None = None_, _description: Opt\[str\] = NotSet_, _homepage: Opt\[str\] = NotSet_, _private: Opt\[bool\] = NotSet_, _visibility: Opt\[str\] = NotSet_, _has\_issues: Opt\[bool\] = NotSet_, _has\_projects: Opt\[bool\] = NotSet_, _has\_wiki: Opt\[bool\] = NotSet_, _has\_discussions: Opt\[bool\] = NotSet_, _is\_template: Opt\[bool\] = NotSet_, _default\_branch: Opt\[str\] = NotSet_, _allow\_squash\_merge: Opt\[bool\] = NotSet_, _allow\_merge\_commit: Opt\[bool\] = NotSet_, _allow\_rebase\_merge: Opt\[bool\] = NotSet_, _allow\_auto\_merge: Opt\[bool\] = NotSet_, _delete\_branch\_on\_merge: Opt\[bool\] = NotSet_, _allow\_update\_branch: Opt\[bool\] = NotSet_, _use\_squash\_pr\_title\_as\_default: Opt\[bool\] = NotSet_, _squash\_merge\_commit\_title: Opt\[str\] = NotSet_, _squash\_merge\_commit\_message: Opt\[str\] = NotSet_, _merge\_commit\_title: Opt\[str\] = NotSet_, _merge\_commit\_message: Opt\[str\] = NotSet_, _archived: Opt\[bool\] = NotSet_, _allow\_forking: Opt\[bool\] = NotSet_, _web\_commit\_signoff\_required: Opt\[bool\] = NotSet_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.edit "Permalink to this definition")Calls

[PATCH /repos/{owner}/{repo}](https://docs.github.com/en/rest/reference/repos)

`get_archive_link`( _archive\_format: str_, _ref: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_) → str [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_archive_link "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/{archive\_format}/{ref}](https://docs.github.com/en/rest/reference/repos#contents)

Parameters

- **archive\_format** – string

- **ref** – string


Return type

string

`get_assignees`() → PaginatedList\[NamedUser\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_assignees "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/assignees](https://docs.github.com/en/rest/reference/issues#assignees)

Return type

`PaginatedList` of [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser")

`get_branch`( _branch: str_) → Branch [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_branch "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/branches/{branch}](https://docs.github.com/en/rest/reference/repos#get-a-branch)

Parameters

**branch** – string

Return type

[`github.Branch.Branch`](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch "github.Branch.Branch")

`rename_branch`( _branch: str \| Branch_, _new\_name: str_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.rename_branch "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/branches/{branch}/rename](https://docs.github.com/en/rest/reference/repos#branches)

Parameters

- **branch** – [`github.Branch.Branch`](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch "github.Branch.Branch") or string

- **new\_name** – string


Return type

bool

NOTE: This method does not return the branch since it may take some
time to fully complete server-side.

`get_branches`() → PaginatedList\[Branch\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_branches "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/branches](https://docs.github.com/en/rest/reference/repos)

Return type

`PaginatedList` of [`github.Branch.Branch`](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch "github.Branch.Branch")

`get_collaborators`( _affiliation: Opt\[str\] = NotSet_, _permission: Opt\[str\] = NotSet_) → PaginatedList\[NamedUser\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_collaborators "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/collaborators](https://docs.github.com/en/rest/collaborators/collaborators)

Parameters

- **affiliation** – string

- **permission** – string


Return type

`PaginatedList` of [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser")

`get_comment`( _id: int_) → CommitComment [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_comment "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/comments/{id}](https://docs.github.com/en/rest/reference/repos#comments)

Parameters

**id** – integer

Return type

[`github.CommitComment.CommitComment`](https://pygithub.readthedocs.io/en/stable/github_objects/CommitComment.html#github.CommitComment.CommitComment "github.CommitComment.CommitComment")

`get_comments`() → PaginatedList\[CommitComment\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_comments "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/comments](https://docs.github.com/en/rest/reference/repos#comments)

Return type

`PaginatedList` of [`github.CommitComment.CommitComment`](https://pygithub.readthedocs.io/en/stable/github_objects/CommitComment.html#github.CommitComment.CommitComment "github.CommitComment.CommitComment")

`get_commit`( _sha: str_) → Commit [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_commit "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/commits/{sha}](https://docs.github.com/en/rest/reference/repos#commits)

Parameters

**sha** – string

Return type

[`github.Commit.Commit`](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html#github.Commit.Commit "github.Commit.Commit")

`get_commits`( _sha: Opt\[str\] = NotSet_, _path: Opt\[str\] = NotSet_, _since: Opt\[datetime\] = NotSet_, _until: Opt\[datetime\] = NotSet_, _author: Opt\[AuthenticatedUser \| NamedUser \| str\] = NotSet_) → PaginatedList\[Commit\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_commits "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/commits](https://docs.github.com/en/rest/reference/repos#commits)

Parameters

- **sha** – string

- **path** – string

- **since** – datetime

- **until** – datetime

- **author** – string or [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser") or [`github.AuthenticatedUser.AuthenticatedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser "github.AuthenticatedUser.AuthenticatedUser")


Return type

`PaginatedList` of [`github.Commit.Commit`](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html#github.Commit.Commit "github.Commit.Commit")

`get_contents`( _path: str_, _ref: Opt\[str\] = NotSet_) → list\[ContentFile\] \| ContentFile [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_contents "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/contents/{path}](https://docs.github.com/en/rest/reference/repos#contents)

Parameters

- **path** – string

- **ref** – string


Return type

[`github.ContentFile.ContentFile`](https://pygithub.readthedocs.io/en/stable/github_objects/ContentFile.html#github.ContentFile.ContentFile "github.ContentFile.ContentFile") or a list of them

`get_deployments`( _sha: Opt\[str\] = NotSet_, _ref: Opt\[str\] = NotSet_, _task: Opt\[str\] = NotSet_, _environment: Opt\[str\] = NotSet_) → PaginatedList\[Deployment\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_deployments "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/deployments](https://docs.github.com/en/rest/reference/repos#deployments)

Param

sha: string

Param

ref: string

Param

task: string

Param

environment: string

Return type

`PaginatedList` of [`github.Deployment.Deployment`](https://pygithub.readthedocs.io/en/stable/github_objects/Deployment.html#github.Deployment.Deployment "github.Deployment.Deployment")

`get_deployment`( _id\_: int_) → Deployment [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_deployment "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/deployments/{deployment\_id}](https://docs.github.com/en/rest/reference/repos#deployments)

Param

[id\_](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#id11): int

Return type

[`github.Deployment.Deployment`](https://pygithub.readthedocs.io/en/stable/github_objects/Deployment.html#github.Deployment.Deployment "github.Deployment.Deployment")

`create_deployment`( _ref: str_, _task: Opt\[str\] = NotSet_, _auto\_merge: Opt\[bool\] = NotSet_, _required\_contexts: Opt\[list\[str\]\] = NotSet_, _payload: Opt\[dict\[str_, _Any\]\] = NotSet_, _environment: Opt\[str\] = NotSet_, _description: Opt\[str\] = NotSet_, _transient\_environment: Opt\[bool\] = NotSet_, _production\_environment: Opt\[bool\] = NotSet_) → Deployment [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_deployment "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/deployments](https://docs.github.com/en/rest/reference/repos#deployments)

Param

ref: string

Param

task: string

Param

auto\_merge: bool

Param

required\_contexts: list of status contexts

Param

payload: dict

Param

environment: string

Param

description: string

Param

transient\_environment: bool

Param

production\_environment: bool

Return type

[`github.Deployment.Deployment`](https://pygithub.readthedocs.io/en/stable/github_objects/Deployment.html#github.Deployment.Deployment "github.Deployment.Deployment")

`get_top_referrers`() → None \| list\[Referrer\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_top_referrers "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/traffic/popular/referrers](https://docs.github.com/en/rest/reference/repos#traffic)

`get_top_paths`() → None \| list\[Path\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_top_paths "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/traffic/popular/paths](https://docs.github.com/en/rest/reference/repos#traffic)

Return type

`list` of [`github.Path.Path`](https://pygithub.readthedocs.io/en/stable/github_objects/Path.html#github.Path.Path "github.Path.Path")

`get_views_traffic`( _per: Opt\[str\] = NotSet_) → View \| None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_views_traffic "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/traffic/views](https://docs.github.com/en/rest/reference/repos#traffic)

Parameters

**per** – string, must be one of day or week, day by default

Return type

None or list of [`github.View.View`](https://pygithub.readthedocs.io/en/stable/github_objects/View.html#github.View.View "github.View.View")

`get_clones_traffic`( _per: Opt\[str\] = NotSet_) → Clones \| None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_clones_traffic "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/traffic/clones](https://docs.github.com/en/rest/reference/repos#traffic)

Parameters

**per** – string, must be one of day or week, day by default

Return type

None or list of [`github.Clones.Clones`](https://pygithub.readthedocs.io/en/stable/github_objects/Clones.html#github.Clones.Clones "github.Clones.Clones")

`get_projects`( _state: Opt\[str\] = NotSet_) → PaginatedList\[Project\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_projects "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/projects](https://docs.github.com/en/rest/reference/projects#list-repository-projects)

Return type

`PaginatedList` of [`github.Project.Project`](https://pygithub.readthedocs.io/en/stable/github_objects/Project.html#github.Project.Project "github.Project.Project")

Parameters

**state** – string

`get_autolinks`() → PaginatedList\[Autolink\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_autolinks "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/autolinks](http://docs.github.com/en/rest/reference/repos)

Return type

`PaginatedList` of [`github.Autolink.Autolink`](https://pygithub.readthedocs.io/en/stable/github_objects/Autolink.html#github.Autolink.Autolink "github.Autolink.Autolink")

`create_file`( _path: str_, _message: str_, _content: str \| bytes_, _branch: Opt\[str\] = NotSet_, _committer: Opt\[InputGitAuthor\] = NotSet_, _author: Opt\[InputGitAuthor\] = NotSet_) → dict\[str, ContentFile \| Commit\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_file "Permalink to this definition")

Create a file in this repository.

Calls

[\`](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#id1) PUT /repos/{owner}/{repo}/contents/{path} < [https://docs.github.com/en/rest/reference/repos#create-or](https://docs.github.com/en/rest/reference/repos#create-or)-

update-file-contents>\`\_
:param path: string, (required), path of the file in the repository
:param message: string, (required), commit message
:param content: string, (required), the actual data in the file
:param branch: string, (optional), branch to create the commit on. Defaults to the default branch of the

> repository

Parameters

- **committer** – InputGitAuthor, (optional), if no information is given the authenticated user’s information
will be used. You must specify both a name and email.

- **author** – InputGitAuthor, (optional), if omitted this will be filled in with committer information. If
passed, you must specify both a name and email.


Return type

{ ‘content’: [`ContentFile`](https://pygithub.readthedocs.io/en/stable/github_objects/ContentFile.html#github.ContentFile.ContentFile "github.ContentFile.ContentFile"):, ‘commit’: [`Commit`](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html#github.Commit.Commit "github.Commit.Commit")}

`get_repository_advisories`() → github.PaginatedList.PaginatedList\[github.RepositoryAdvisory.RepositoryAdvisory\]\[github.RepositoryAdvisory.RepositoryAdvisory\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_repository_advisories "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/security-advisories](https://docs.github.com/en/rest/security-advisories/repository-advisories)

Return type

`PaginatedList` of [`github.RepositoryAdvisory.RepositoryAdvisory`](https://pygithub.readthedocs.io/en/stable/github_objects/RepositoryAdvisory.html#github.RepositoryAdvisory.RepositoryAdvisory "github.RepositoryAdvisory.RepositoryAdvisory")

`get_repository_advisory`( _ghsa: str_) → github.RepositoryAdvisory.RepositoryAdvisory [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_repository_advisory "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/security-advisories/{ghsa}](https://docs.github.com/en/rest/security-advisories/repository-advisories)

Parameters

**ghsa** – string

Return type

[`github.RepositoryAdvisory.RepositoryAdvisory`](https://pygithub.readthedocs.io/en/stable/github_objects/RepositoryAdvisory.html#github.RepositoryAdvisory.RepositoryAdvisory "github.RepositoryAdvisory.RepositoryAdvisory")

`update_file`( _path: str_, _message: str_, _content: bytes \| str_, _sha: str_, _branch: Opt\[str\] = NotSet_, _committer: Opt\[InputGitAuthor\] = NotSet_, _author: Opt\[InputGitAuthor\] = NotSet_) → dict\[str, ContentFile \| Commit\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.update_file "Permalink to this definition")

This method updates a file in a repository.

Calls

[\`](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#id3) PUT /repos/{owner}/{repo}/contents/{path} < [https://docs.github.com/en/rest/reference/repos#create-or](https://docs.github.com/en/rest/reference/repos#create-or)-

update-file-contents>\`\_
:param path: string, Required. The content path.
:param message: string, Required. The commit message.
:param content: string, Required. The updated file content, either base64 encoded, or ready to be encoded.
:param sha: string, Required. The blob SHA of the file being replaced.
:param branch: string. The branch name. Default: the repository’s default branch (usually master)
:param committer: InputGitAuthor, (optional), if no information is given the authenticated user’s information

> will be used. You must specify both a name and email.

Parameters

**author** – InputGitAuthor, (optional), if omitted this will be filled in with committer information. If
passed, you must specify both a name and email.

Return type

{ ‘content’: [`ContentFile`](https://pygithub.readthedocs.io/en/stable/github_objects/ContentFile.html#github.ContentFile.ContentFile "github.ContentFile.ContentFile"):, ‘commit’: [`Commit`](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html#github.Commit.Commit "github.Commit.Commit")}

`delete_file`( _path: str_, _message: str_, _sha: str_, _branch: Opt\[str\] = NotSet_, _committer: Opt\[InputGitAuthor\] = NotSet_, _author: Opt\[InputGitAuthor\] = NotSet_) → dict\[str, Commit \| \_NotSetType\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.delete_file "Permalink to this definition")

This method deletes a file in a repository.

Calls

[\`](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#id5) DELETE /repos/{owner}/{repo}/contents/{path} < [https://docs.github.com/en/rest/reference/repos#delete-a](https://docs.github.com/en/rest/reference/repos#delete-a)-

file>\`\_
:param path: string, Required. The content path.
:param message: string, Required. The commit message.
:param sha: string, Required. The blob SHA of the file being replaced.
:param branch: string. The branch name. Default: the repository’s default branch (usually master)
:param committer: InputGitAuthor, (optional), if no information is given the authenticated user’s information

> will be used. You must specify both a name and email.

Parameters

**author** – InputGitAuthor, (optional), if omitted this will be filled in with committer information. If
passed, you must specify both a name and email.

Return type

{ ‘content’: `null`:, ‘commit’: [`Commit`](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html#github.Commit.Commit "github.Commit.Commit")}

`get_dir_contents`( _path: str_, _ref: Opt\[str\] = NotSet_) → list\[ContentFile\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_dir_contents "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/contents/{path}](https://docs.github.com/en/rest/reference/repos#contents)

`get_contributors`( _anon: Opt\[str\] = NotSet_) → PaginatedList\[NamedUser\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_contributors "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/contributors](https://docs.github.com/en/rest/reference/repos)

Parameters

**anon** – string

Return type

`PaginatedList` of [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser")

`get_download`( _id: int_) → Download [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_download "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/downloads/{id}](https://docs.github.com/en/rest/reference/repos)

Parameters

**id** – integer

Return type

[`github.Download.Download`](https://pygithub.readthedocs.io/en/stable/github_objects/Download.html#github.Download.Download "github.Download.Download")

`get_downloads`() → PaginatedList\[Download\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_downloads "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/downloads](https://docs.github.com/en/rest/reference/repos)

Return type

`PaginatedList` of [`github.Download.Download`](https://pygithub.readthedocs.io/en/stable/github_objects/Download.html#github.Download.Download "github.Download.Download")

`get_events`() → PaginatedList\[Event\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_events "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/events](https://docs.github.com/en/rest/reference/activity#events)

Return type

`PaginatedList` of [`github.Event.Event`](https://pygithub.readthedocs.io/en/stable/github_objects/Event.html#github.Event.Event "github.Event.Event")

`get_forks`() → github.PaginatedList.PaginatedList\[github.Repository.Repository\]\[github.Repository.Repository\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_forks "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/forks](https://docs.github.com/en/rest/reference/repos#forks)

Return type

`PaginatedList` of [`github.Repository.Repository`](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository "github.Repository.Repository")

`create_fork`( _organization: Organization \| Opt\[str\] = NotSet_, _name: Opt\[str\] = NotSet_, _default\_branch\_only: Opt\[bool\] = NotSet_) → Repository [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_fork "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/forks](https://docs.github.com/en/rest/reference/repos#forks)

Parameters

- **organization** – [`github.Organization.Organization`](https://pygithub.readthedocs.io/en/stable/github_objects/Organization.html#github.Organization.Organization "github.Organization.Organization") or string

- **name** – string

- **default\_branch\_only** – bool


Return type

[`github.Repository.Repository`](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository "github.Repository.Repository")

`get_git_blob`( _sha: str_) → GitBlob [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_git_blob "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/git/blobs/{sha}](https://docs.github.com/en/rest/reference/git#blobs)

Parameters

**sha** – string

Return type

[`github.GitBlob.GitBlob`](https://pygithub.readthedocs.io/en/stable/github_objects/GitBlob.html#github.GitBlob.GitBlob "github.GitBlob.GitBlob")

`get_git_commit`( _sha: str_) → GitCommit [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_git_commit "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/git/commits/{sha}](https://docs.github.com/en/rest/reference/git#commits)

Parameters

**sha** – string

Return type

[`github.GitCommit.GitCommit`](https://pygithub.readthedocs.io/en/stable/github_objects/GitCommit.html#github.GitCommit.GitCommit "github.GitCommit.GitCommit")

`get_git_ref`( _ref: str_) → GitRef [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_git_ref "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/git/refs/{ref}](https://docs.github.com/en/rest/reference/git#references)

Parameters

**ref** – string

Return type

[`github.GitRef.GitRef`](https://pygithub.readthedocs.io/en/stable/github_objects/GitRef.html#github.GitRef.GitRef "github.GitRef.GitRef")

`get_git_refs`() → PaginatedList\[GitRef\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_git_refs "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/git/refs](https://docs.github.com/en/rest/reference/git#references)

Return type

`PaginatedList` of [`github.GitRef.GitRef`](https://pygithub.readthedocs.io/en/stable/github_objects/GitRef.html#github.GitRef.GitRef "github.GitRef.GitRef")

`get_git_matching_refs`( _ref: str_) → PaginatedList\[GitRef\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_git_matching_refs "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/git/matching-refs/{ref}](https://docs.github.com/en/rest/reference/git#list-matching-references)

Return type

`PaginatedList` of [`github.GitRef.GitRef`](https://pygithub.readthedocs.io/en/stable/github_objects/GitRef.html#github.GitRef.GitRef "github.GitRef.GitRef")

`get_git_tag`( _sha: str_) → GitTag [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_git_tag "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/git/tags/{sha}](https://docs.github.com/en/rest/reference/git#tags)

Parameters

**sha** – string

Return type

[`github.GitTag.GitTag`](https://pygithub.readthedocs.io/en/stable/github_objects/GitTag.html#github.GitTag.GitTag "github.GitTag.GitTag")

`get_git_tree`( _sha: str_, _recursive: Opt\[bool\] = NotSet_) → GitTree [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_git_tree "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/git/trees/{sha}](https://docs.github.com/en/rest/reference/git#trees)

Parameters

- **sha** – string

- **recursive** – bool


Return type

[`github.GitTree.GitTree`](https://pygithub.readthedocs.io/en/stable/github_objects/GitTree.html#github.GitTree.GitTree "github.GitTree.GitTree")

`get_hook`( _id: int_) → Hook [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_hook "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/hooks/{id}](https://docs.github.com/en/rest/reference/repos#webhooks)

Parameters

**id** – integer

Return type

[`github.Hook.Hook`](https://pygithub.readthedocs.io/en/stable/github_objects/Hook.html#github.Hook.Hook "github.Hook.Hook")

`get_hooks`() → PaginatedList\[Hook\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_hooks "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/hooks](https://docs.github.com/en/rest/reference/repos#webhooks)

Return type

`PaginatedList` of [`github.Hook.Hook`](https://pygithub.readthedocs.io/en/stable/github_objects/Hook.html#github.Hook.Hook "github.Hook.Hook")

`get_hook_delivery`( _hook\_id: int_, _delivery\_id: int_) → github.HookDelivery.HookDelivery [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_hook_delivery "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/hooks/{hook\_id}/deliveries/{delivery\_id}](https://docs.github.com/en/rest/webhooks/repo-deliveries)

Parameters

- **hook\_id** – integer

- **delivery\_id** – integer


Return type

[`github.HookDelivery.HookDelivery`](https://pygithub.readthedocs.io/en/stable/github_objects/HookDelivery.html#github.HookDelivery.HookDelivery "github.HookDelivery.HookDelivery")

`get_hook_deliveries`( _hook\_id: int_) → github.PaginatedList.PaginatedList\[github.HookDelivery.HookDeliverySummary\]\[github.HookDelivery.HookDeliverySummary\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_hook_deliveries "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/hooks/{hook\_id}/deliveries](https://docs.github.com/en/rest/webhooks/repo-deliveries)

Parameters

**hook\_id** – integer

Return type

`PaginatedList` of [`github.HookDelivery.HookDeliverySummary`](https://pygithub.readthedocs.io/en/stable/github_objects/HookDeliverySummary.html#github.HookDelivery.HookDeliverySummary "github.HookDelivery.HookDeliverySummary")

`get_issue`( _number: int_) → Issue [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_issue "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/issues/{number}](https://docs.github.com/en/rest/reference/issues)

Parameters

**number** – integer

Return type

[`github.Issue.Issue`](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue "github.Issue.Issue")

`get_issues`( _milestone: Milestone \| Opt\[str\] = NotSet_, _state: Opt\[str\] = NotSet_, _assignee: NamedUser \| Opt\[str\] = NotSet_, _mentioned: Opt\[NamedUser\] = NotSet_, _labels: Opt\[list\[str\] \| list\[Label\]\] = NotSet_, _sort: Opt\[str\] = NotSet_, _direction: Opt\[str\] = NotSet_, _since: Opt\[datetime\] = NotSet_, _creator: Opt\[NamedUser\] = NotSet_) → PaginatedList\[Issue\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_issues "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/issues](https://docs.github.com/en/rest/reference/issues)

Parameters

- **milestone** – [`github.Milestone.Milestone`](https://pygithub.readthedocs.io/en/stable/github_objects/Milestone.html#github.Milestone.Milestone "github.Milestone.Milestone") or “none” or “\*”

- **state** – string. open, closed, or all. If this is not set the GitHub API default behavior will be used. At the moment this is to return only open issues. This might change anytime on GitHub API side and it could be clever to explicitly specify the state value.

- **assignee** – string or [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser") or “none” or “\*”

- **mentioned** – [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser")

- **labels** – list of string or [`github.Label.Label`](https://pygithub.readthedocs.io/en/stable/github_objects/Label.html#github.Label.Label "github.Label.Label")

- **sort** – string

- **direction** – string

- **since** – datetime

- **creator** – string or [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser")


Return type

`PaginatedList` of [`github.Issue.Issue`](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue "github.Issue.Issue")

`get_issues_comments`( _sort: Opt\[str\] = NotSet_, _direction: Opt\[str\] = NotSet_, _since: Opt\[datetime\] = NotSet_) → PaginatedList\[IssueComment\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_issues_comments "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/issues/comments](https://docs.github.com/en/rest/reference/issues#comments)

Parameters

- **sort** – string

- **direction** – string

- **since** – datetime


Return type

`PaginatedList` of [`github.IssueComment.IssueComment`](https://pygithub.readthedocs.io/en/stable/github_objects/IssueComment.html#github.IssueComment.IssueComment "github.IssueComment.IssueComment")

`get_issues_event`( _id: int_) → IssueEvent [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_issues_event "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/issues/events/{id}](https://docs.github.com/en/rest/reference/issues#events)

Parameters

**id** – integer

Return type

[`github.IssueEvent.IssueEvent`](https://pygithub.readthedocs.io/en/stable/github_objects/IssueEvent.html#github.IssueEvent.IssueEvent "github.IssueEvent.IssueEvent")

`get_issues_events`() → PaginatedList\[IssueEvent\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_issues_events "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/issues/events](https://docs.github.com/en/rest/reference/issues#events)

Return type

`PaginatedList` of [`github.IssueEvent.IssueEvent`](https://pygithub.readthedocs.io/en/stable/github_objects/IssueEvent.html#github.IssueEvent.IssueEvent "github.IssueEvent.IssueEvent")

`get_key`( _id: int_) → RepositoryKey [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_key "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/keys/{id}](https://docs.github.com/en/rest/reference/repos#deploy-keys)

Parameters

**id** – integer

Return type

[`github.RepositoryKey.RepositoryKey`](https://pygithub.readthedocs.io/en/stable/github_objects/RepositoryKey.html#github.RepositoryKey.RepositoryKey "github.RepositoryKey.RepositoryKey")

`get_keys`() → PaginatedList\[RepositoryKey\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_keys "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/keys](https://docs.github.com/en/rest/reference/repos#deploy-keys)

Return type

`PaginatedList` of [`github.RepositoryKey.RepositoryKey`](https://pygithub.readthedocs.io/en/stable/github_objects/RepositoryKey.html#github.RepositoryKey.RepositoryKey "github.RepositoryKey.RepositoryKey")

`get_label`( _name: str_) → Label [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_label "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/labels/{name}](https://docs.github.com/en/rest/reference/issues#labels)

Parameters

**name** – string

Return type

[`github.Label.Label`](https://pygithub.readthedocs.io/en/stable/github_objects/Label.html#github.Label.Label "github.Label.Label")

`get_labels`() → PaginatedList\[Label\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_labels "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/labels](https://docs.github.com/en/rest/reference/issues#labels)

Return type

`PaginatedList` of [`github.Label.Label`](https://pygithub.readthedocs.io/en/stable/github_objects/Label.html#github.Label.Label "github.Label.Label")

`get_languages`() → dict\[str, int\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_languages "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/languages](https://docs.github.com/en/rest/reference/repos)

Return type

dict of string to integer

`get_license`() → ContentFile [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_license "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/license](https://docs.github.com/en/rest/reference/licenses)

Return type

[`github.ContentFile.ContentFile`](https://pygithub.readthedocs.io/en/stable/github_objects/ContentFile.html#github.ContentFile.ContentFile "github.ContentFile.ContentFile")

`get_milestone`( _number: int_) → Milestone [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_milestone "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/milestones/{number}](https://docs.github.com/en/rest/reference/issues#milestones)

Parameters

**number** – integer

Return type

[`github.Milestone.Milestone`](https://pygithub.readthedocs.io/en/stable/github_objects/Milestone.html#github.Milestone.Milestone "github.Milestone.Milestone")

`get_milestones`( _state: Opt\[str\] = NotSet_, _sort: Opt\[str\] = NotSet_, _direction: Opt\[str\] = NotSet_) → PaginatedList\[Milestone\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_milestones "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/milestones](https://docs.github.com/en/rest/reference/issues#milestones)

Parameters

- **state** – string

- **sort** – string

- **direction** – string


Return type

`PaginatedList` of [`github.Milestone.Milestone`](https://pygithub.readthedocs.io/en/stable/github_objects/Milestone.html#github.Milestone.Milestone "github.Milestone.Milestone")

`get_network_events`() → PaginatedList\[Event\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_network_events "Permalink to this definition")Calls

[GET /networks/{owner}/{repo}/events](https://docs.github.com/en/rest/reference/activity#events)

Return type

`PaginatedList` of [`github.Event.Event`](https://pygithub.readthedocs.io/en/stable/github_objects/Event.html#github.Event.Event "github.Event.Event")

`get_public_key`( _secret\_type: str = 'actions'_) → PublicKey [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_public_key "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/actions/secrets/public-key](https://docs.github.com/en/rest/reference/actions#get-a-repository-public-key)

Parameters

**secret\_type** – string options actions or dependabot

Return type

[`github.PublicKey.PublicKey`](https://pygithub.readthedocs.io/en/stable/github_objects/PublicKey.html#github.PublicKey.PublicKey "github.PublicKey.PublicKey")

`get_pull`( _number: int_) → PullRequest [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_pull "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/pulls/{number}](https://docs.github.com/en/rest/reference/pulls)

Parameters

**number** – integer

Return type

[`github.PullRequest.PullRequest`](https://pygithub.readthedocs.io/en/stable/github_objects/PullRequest.html#github.PullRequest.PullRequest "github.PullRequest.PullRequest")

`get_pulls`( _state: Opt\[str\] = NotSet_, _sort: Opt\[str\] = NotSet_, _direction: Opt\[str\] = NotSet_, _base: Opt\[str\] = NotSet_, _head: Opt\[str\] = NotSet_) → PaginatedList\[PullRequest\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_pulls "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/pulls](https://docs.github.com/en/rest/reference/pulls)

Parameters

- **state** – string

- **sort** – string

- **direction** – string

- **base** – string

- **head** – string


Return type

`PaginatedList` of [`github.PullRequest.PullRequest`](https://pygithub.readthedocs.io/en/stable/github_objects/PullRequest.html#github.PullRequest.PullRequest "github.PullRequest.PullRequest")

`get_pulls_comments`( _sort: Opt\[str\] = NotSet_, _direction: Opt\[str\] = NotSet_, _since: Opt\[datetime\] = NotSet_) → PaginatedList\[PullRequestComment\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_pulls_comments "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/pulls/comments](https://docs.github.com/en/rest/reference/pulls#comments)

Parameters

- **sort** – string

- **direction** – string

- **since** – datetime


Return type

`PaginatedList` of [`github.PullRequestComment.PullRequestComment`](https://pygithub.readthedocs.io/en/stable/github_objects/PullRequestComment.html#github.PullRequestComment.PullRequestComment "github.PullRequestComment.PullRequestComment")

`get_pulls_review_comments`( _sort: Opt\[str\] = NotSet_, _direction: Opt\[str\] = NotSet_, _since: Opt\[datetime\] = NotSet_) → PaginatedList\[PullRequestComment\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_pulls_review_comments "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/pulls/comments](https://docs.github.com/en/rest/reference/pulls#review-comments)

Parameters

- **sort** – string ‘created’, ‘updated’, ‘created\_at’

- **direction** – string ‘asc’ or ‘desc’

- **since** – datetime


Return type

`PaginatedList` of [`github.PullRequestComment.PullRequestComment`](https://pygithub.readthedocs.io/en/stable/github_objects/PullRequestComment.html#github.PullRequestComment.PullRequestComment "github.PullRequestComment.PullRequestComment")

`get_readme`( _ref: Opt\[str\] = NotSet_) → ContentFile [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_readme "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/readme](https://docs.github.com/en/rest/reference/repos#contents)

Parameters

**ref** – string

Return type

[`github.ContentFile.ContentFile`](https://pygithub.readthedocs.io/en/stable/github_objects/ContentFile.html#github.ContentFile.ContentFile "github.ContentFile.ContentFile")

`get_self_hosted_runner`( _runner\_id: int_) → SelfHostedActionsRunner [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_self_hosted_runner "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/actions/runners/{id}](https://docs.github.com/en/rest/reference/actions#get-a-self-hosted-runner-for-a-repository)

Parameters

**runner\_id** – int

Return type

[`github.SelfHostedActionsRunner.SelfHostedActionsRunner`](https://pygithub.readthedocs.io/en/stable/github_objects/SelfHostedActionsRunner.html#github.SelfHostedActionsRunner.SelfHostedActionsRunner "github.SelfHostedActionsRunner.SelfHostedActionsRunner")

`get_self_hosted_runners`() → PaginatedList\[SelfHostedActionsRunner\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_self_hosted_runners "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/actions/runners](https://docs.github.com/en/rest/reference/actions#list-self-hosted-runners-for-a-repository)

Return type

`PaginatedList` of [`github.SelfHostedActionsRunner.SelfHostedActionsRunner`](https://pygithub.readthedocs.io/en/stable/github_objects/SelfHostedActionsRunner.html#github.SelfHostedActionsRunner.SelfHostedActionsRunner "github.SelfHostedActionsRunner.SelfHostedActionsRunner")

`get_source_import`() → SourceImport \| None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_source_import "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/import](https://docs.github.com/en/rest/reference/migrations#source-imports)

`get_stargazers`() → PaginatedList\[NamedUser\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_stargazers "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/stargazers](https://docs.github.com/en/rest/reference/activity#starring)

Return type

`PaginatedList` of [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser")

`get_stargazers_with_dates`() → PaginatedList\[Stargazer\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_stargazers_with_dates "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/stargazers](https://docs.github.com/en/rest/reference/activity#starring)

Return type

`PaginatedList` of [`github.Stargazer.Stargazer`](https://pygithub.readthedocs.io/en/stable/github_objects/Stargazer.html#github.Stargazer.Stargazer "github.Stargazer.Stargazer")

`get_stats_contributors`() → list\[StatsContributor\] \| None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_stats_contributors "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/stats/contributors](https://docs.github.com/en/rest/reference/repos#get-all-contributor-commit-activity)

Return type

None or list of [`github.StatsContributor.StatsContributor`](https://pygithub.readthedocs.io/en/stable/github_objects/StatsContributor.html#github.StatsContributor.StatsContributor "github.StatsContributor.StatsContributor")

`get_stats_commit_activity`() → list\[StatsCommitActivity\] \| None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_stats_commit_activity "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/stats/commit\_activity](https://docs.github.com/en/rest/reference/repos#get-the-last-year-of-commit-activity)

Return type

None or list of [`github.StatsCommitActivity.StatsCommitActivity`](https://pygithub.readthedocs.io/en/stable/github_objects/StatsCommitActivity.html#github.StatsCommitActivity.StatsCommitActivity "github.StatsCommitActivity.StatsCommitActivity")

`get_stats_code_frequency`() → list\[StatsCodeFrequency\] \| None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_stats_code_frequency "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/stats/code\_frequency](https://docs.github.com/en/rest/reference/repos#get-the-weekly-commit-activity)

Return type

None or list of [`github.StatsCodeFrequency.StatsCodeFrequency`](https://pygithub.readthedocs.io/en/stable/github_objects/StatsCodeFrequency.html#github.StatsCodeFrequency.StatsCodeFrequency "github.StatsCodeFrequency.StatsCodeFrequency")

`get_stats_participation`() → StatsParticipation \| None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_stats_participation "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/stats/participation](https://docs.github.com/en/rest/reference/repos#get-the-weekly-commit-count)

Return type

None or [`github.StatsParticipation.StatsParticipation`](https://pygithub.readthedocs.io/en/stable/github_objects/StatsParticipation.html#github.StatsParticipation.StatsParticipation "github.StatsParticipation.StatsParticipation")

`get_stats_punch_card`() → StatsPunchCard \| None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_stats_punch_card "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/stats/punch\_card](https://docs.github.com/en/rest/reference/repos#get-the-hourly-commit-count-for-each-day)

Return type

None or [`github.StatsPunchCard.StatsPunchCard`](https://pygithub.readthedocs.io/en/stable/github_objects/StatsPunchCard.html#github.StatsPunchCard.StatsPunchCard "github.StatsPunchCard.StatsPunchCard")

`get_subscribers`() → PaginatedList\[NamedUser\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_subscribers "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/subscribers](https://docs.github.com/en/rest/reference/activity#watching)

Return type

`PaginatedList` of [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser")

`get_tags`() → PaginatedList\[Tag\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_tags "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/tags](https://docs.github.com/en/rest/reference/repos)

Return type

`PaginatedList` of [`github.Tag.Tag`](https://pygithub.readthedocs.io/en/stable/github_objects/Tag.html#github.Tag.Tag "github.Tag.Tag")

`get_releases`() → PaginatedList\[GitRelease\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_releases "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/releases](https://docs.github.com/en/rest/reference/repos#list-releases)

Return type

`PaginatedList` of [`github.GitRelease.GitRelease`](https://pygithub.readthedocs.io/en/stable/github_objects/GitRelease.html#github.GitRelease.GitRelease "github.GitRelease.GitRelease")

`get_release`( _id: int \| str_) → GitRelease [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_release "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/releases/{id}](https://docs.github.com/en/rest/reference/repos#get-a-release)

Parameters

**id** – int (release id), str (tag name)

Return type

None or [`github.GitRelease.GitRelease`](https://pygithub.readthedocs.io/en/stable/github_objects/GitRelease.html#github.GitRelease.GitRelease "github.GitRelease.GitRelease")

`get_latest_release`() → GitRelease [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_latest_release "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/releases/latest](https://docs.github.com/en/rest/reference/repos#get-the-latest-release)

Return type

[`github.GitRelease.GitRelease`](https://pygithub.readthedocs.io/en/stable/github_objects/GitRelease.html#github.GitRelease.GitRelease "github.GitRelease.GitRelease")

`get_teams`() → PaginatedList\[Team\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_teams "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/teams](https://docs.github.com/en/rest/reference/repos)

Return type

`PaginatedList` of [`github.Team.Team`](https://pygithub.readthedocs.io/en/stable/github_objects/Team.html#github.Team.Team "github.Team.Team")

`get_topics`() → list\[str\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_topics "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/topics](https://docs.github.com/en/rest/reference/repos#replace-all-repository-topics)

Return type

list of strings

`get_watchers`() → PaginatedList\[NamedUser\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_watchers "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/watchers](https://docs.github.com/en/rest/reference/activity#starring)

Return type

`PaginatedList` of [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser")

`get_workflows`() → PaginatedList\[Workflow\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_workflows "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/actions/workflows](https://docs.github.com/en/rest/reference/actions#workflows)

Return type

`PaginatedList` of [`github.Workflow.Workflow`](https://pygithub.readthedocs.io/en/stable/github_objects/Workflow.html#github.Workflow.Workflow "github.Workflow.Workflow")

`get_workflow`( _id\_or\_file\_name: str \| int_) → Workflow [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_workflow "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/actions/workflows/{workflow\_id}](https://docs.github.com/en/rest/reference/actions#workflows)

Parameters

**id\_or\_file\_name** – int or string. Can be either a workflow ID or a filename.

Return type

[`github.Workflow.Workflow`](https://pygithub.readthedocs.io/en/stable/github_objects/Workflow.html#github.Workflow.Workflow "github.Workflow.Workflow")

`get_workflow_runs`( _actor: Opt\[NamedUser\] = NotSet_, _branch: Opt\[Branch\] = NotSet_, _event: Opt\[str\] = NotSet_, _status: Opt\[str\] = NotSet_, _exclude\_pull\_requests: Opt\[bool\] = NotSet_, _head\_sha: Opt\[str\] = NotSet_, _created: Opt\[str\] = NotSet_, _check\_suite\_id: Opt\[int\] = NotSet_) → PaginatedList\[WorkflowRun\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_workflow_runs "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/actions/runs](https://docs.github.com/en/rest/reference/actions#list-workflow-runs-for-a-repository)

Parameters

- **actor** – [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser") or string

- **branch** – [`github.Branch.Branch`](https://pygithub.readthedocs.io/en/stable/github_objects/Branch.html#github.Branch.Branch "github.Branch.Branch") or string

- **event** – string

- **status** – string queued, in\_progress, completed, success, failure, neutral, cancelled, skipped, timed\_out, or action\_required

- **exclude\_pull\_requests** – bool

- **head\_sha** – string

- **created** – string Created filter, see [https://docs.github.com/en/search-github/getting-started-with-searching-on-github/understanding-the-search-syntax#query-for-dates](https://docs.github.com/en/search-github/getting-started-with-searching-on-github/understanding-the-search-syntax#query-for-dates)

- **check\_suite\_id** – int


Return type

`PaginatedList` of [`github.WorkflowRun.WorkflowRun`](https://pygithub.readthedocs.io/en/stable/github_objects/WorkflowRun.html#github.WorkflowRun.WorkflowRun "github.WorkflowRun.WorkflowRun")

`get_workflow_run`( _id\_: int_) → WorkflowRun [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_workflow_run "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/actions/runs/{run\_id}](https://docs.github.com/en/rest/reference/actions#workflow-runs)

Parameters

**id** – int

Return type

[`github.WorkflowRun.WorkflowRun`](https://pygithub.readthedocs.io/en/stable/github_objects/WorkflowRun.html#github.WorkflowRun.WorkflowRun "github.WorkflowRun.WorkflowRun")

`has_in_assignees`( _assignee: str \| NamedUser_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.has_in_assignees "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/assignees/{assignee}](https://docs.github.com/en/rest/reference/issues#assignees)

Parameters

**assignee** – string or [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser")

Return type

bool

`has_in_collaborators`( _collaborator: str \| NamedUser_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.has_in_collaborators "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/collaborators/{user}](https://docs.github.com/en/rest/reference/repos#collaborators)

Parameters

**collaborator** – string or [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser")

Return type

bool

`legacy_search_issues`( _state: str_, _keyword: str_) → list\[Issue\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.legacy_search_issues "Permalink to this definition")Calls

[GET /legacy/issues/search/{owner}/{repository}/{state}/{keyword}](https://docs.github.com/en/rest/reference/search)

Parameters

- **state** – “open” or “closed”

- **keyword** – string


Return type

List of [`github.Issue.Issue`](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue "github.Issue.Issue")

`get_notifications`( _all: Opt\[bool\] = NotSet_, _participating: Opt\[bool\] = NotSet_, _since: Opt\[datetime\] = NotSet_, _before: Opt\[datetime\] = NotSet_) → PaginatedList\[Notification\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_notifications "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/notifications](https://docs.github.com/en/rest/reference/activity#notifications)

Parameters

- **all** – bool

- **participating** – bool

- **since** – datetime

- **before** – datetime


Return type

`PaginatedList` of [`github.Notification.Notification`](https://pygithub.readthedocs.io/en/stable/github_objects/Notification.html#github.Notification.Notification "github.Notification.Notification")

`mark_notifications_as_read`( _last\_read\_at: datetime.datetime = datetime.datetime(2025_, _2_, _21_, _14_, _22_, _43_, _886166_, _tzinfo=datetime.timezone.utc)_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.mark_notifications_as_read "Permalink to this definition")Calls

[PUT /repos/{owner}/{repo}/notifications](https://docs.github.com/en/rest/reference/activity#notifications)

Parameters

**last\_read\_at** – datetime

`merge`( _base: str_, _head: str_, _commit\_message: Opt\[str\] = NotSet_) → Commit \| None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.merge "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/merges](https://docs.github.com/en/rest/reference/repos#merging)

Parameters

- **base** – string

- **head** – string

- **commit\_message** – string


Return type

[`github.Commit.Commit`](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html#github.Commit.Commit "github.Commit.Commit")

`merge_upstream`( _branch: str_) → MergedUpstream [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.merge_upstream "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/merge-upstream](https://docs.github.com/en/rest/branches/branches#sync-a-fork-branch-with-the-upstream-repository)

Parameters

**branch** – string

Return type

[`github.MergedUpstream.MergedUpstream`](https://pygithub.readthedocs.io/en/stable/github_objects/MergedUpstream.html#github.MergedUpstream.MergedUpstream "github.MergedUpstream.MergedUpstream")

Raises

`GithubException` for error status codes

`replace_topics`( _topics: list\[str\]_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.replace_topics "Permalink to this definition")Calls

[PUT /repos/{owner}/{repo}/topics](https://docs.github.com/en/rest/reference/repos)

Parameters

**topics** – list of strings

Return type

None

`get_vulnerability_alert`() → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_vulnerability_alert "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/vulnerability-alerts](https://docs.github.com/en/rest/reference/repos)

Return type

bool

`enable_vulnerability_alert`() → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.enable_vulnerability_alert "Permalink to this definition")Calls

[PUT /repos/{owner}/{repo}/vulnerability-alerts](https://docs.github.com/en/rest/reference/repos)

Return type

bool

`disable_vulnerability_alert`() → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.disable_vulnerability_alert "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/vulnerability-alerts](https://docs.github.com/en/rest/reference/repos)

Return type

bool

`enable_automated_security_fixes`() → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.enable_automated_security_fixes "Permalink to this definition")Calls

[PUT /repos/{owner}/{repo}/automated-security-fixes](https://docs.github.com/en/rest/reference/repos)

Return type

bool

`disable_automated_security_fixes`() → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.disable_automated_security_fixes "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/automated-security-fixes](https://docs.github.com/en/rest/reference/repos)

Return type

bool

`remove_from_collaborators`( _collaborator: str \| NamedUser_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.remove_from_collaborators "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/collaborators/{user}](https://docs.github.com/en/rest/reference/repos#collaborators)

Parameters

**collaborator** – string or [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser")

Return type

None

`remove_self_hosted_runner`( _runner: SelfHostedActionsRunner \| int_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.remove_self_hosted_runner "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/actions/runners/{runner\_id}](https://docs.github.com/en/rest/reference/actions#delete-a-self-hosted-runner-from-a-repository)

Parameters

**runner** – int or [`github.SelfHostedActionsRunner.SelfHostedActionsRunner`](https://pygithub.readthedocs.io/en/stable/github_objects/SelfHostedActionsRunner.html#github.SelfHostedActionsRunner.SelfHostedActionsRunner "github.SelfHostedActionsRunner.SelfHostedActionsRunner")

Return type

bool

`remove_autolink`( _autolink: Autolink \| int_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.remove_autolink "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/autolinks/{id}](https://docs.github.com/en/rest/reference/repos)

Parameters

**autolink** – int or [`github.Autolink.Autolink`](https://pygithub.readthedocs.io/en/stable/github_objects/Autolink.html#github.Autolink.Autolink "github.Autolink.Autolink")

Return type

None

`subscribe_to_hub`( _event: str_, _callback: str_, _secret: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.subscribe_to_hub "Permalink to this definition")Calls

[POST /hub](https://docs.github.com/en/rest/reference/repos#pubsubhubbub)

Parameters

- **event** – string

- **callback** – string

- **secret** – string


Return type

None

`unsubscribe_from_hub`( _event: str_, _callback: str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.unsubscribe_from_hub "Permalink to this definition")Calls

[POST /hub](https://docs.github.com/en/rest/reference/repos#pubsubhubbub)

Parameters

- **event** – string

- **callback** – string

- **secret** – string


Return type

None

`create_check_suite`( _head\_sha: str_) → CheckSuite [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_check_suite "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/check-suites](https://docs.github.com/en/rest/reference/checks#create-a-check-suite)

Parameters

**head\_sha** – string

Return type

[`github.CheckSuite.CheckSuite`](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite "github.CheckSuite.CheckSuite")

`get_check_suite`( _check\_suite\_id: int_) → CheckSuite [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_check_suite "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/check-suites/{check\_suite\_id}](https://docs.github.com/en/rest/reference/checks#get-a-check-suite)

Parameters

**check\_suite\_id** – int

Return type

[`github.CheckSuite.CheckSuite`](https://pygithub.readthedocs.io/en/stable/github_objects/CheckSuite.html#github.CheckSuite.CheckSuite "github.CheckSuite.CheckSuite")

`update_check_suites_preferences`( _auto\_trigger\_checks: list\[dict\[str, bool \| int\]\]_) → RepositoryPreferences [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.update_check_suites_preferences "Permalink to this definition")Calls

[PATCH /repos/{owner}/{repo}/check-suites/preferences](https://docs.github.com/en/rest/reference/checks#update-repository-preferences-for-check-suites)

Parameters

**auto\_trigger\_checks** – list of dict

Return type

[`github.RepositoryPreferences.RepositoryPreferences`](https://pygithub.readthedocs.io/en/stable/github_objects/RepositoryPreferences.html#github.RepositoryPreferences.RepositoryPreferences "github.RepositoryPreferences.RepositoryPreferences")

`create_check_run`( _name: str_, _head\_sha: str_, _details\_url: Opt\[str\] = NotSet_, _external\_id: Opt\[str\] = NotSet_, _status: Opt\[str\] = NotSet_, _started\_at: Opt\[datetime\] = NotSet_, _conclusion: Opt\[str\] = NotSet_, _completed\_at: Opt\[datetime\] = NotSet_, _output: Opt\[dict\[str_, _str \| list\[dict\[str_, _str \| int\]\]\]\] = NotSet_, _actions: Opt\[list\[dict\[str_, _str\]\]\] = NotSet_) → CheckRun [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_check_run "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/check-runs](https://docs.github.com/en/rest/reference/checks#create-a-check-run)

Parameters

- **name** – string

- **head\_sha** – string

- **details\_url** – string

- **external\_id** – string

- **status** – string

- **started\_at** – datetime

- **conclusion** – string

- **completed\_at** – datetime

- **output** – dict

- **actions** – list of dict


Return type

[`github.CheckRun.CheckRun`](https://pygithub.readthedocs.io/en/stable/github_objects/CheckRun.html#github.CheckRun.CheckRun "github.CheckRun.CheckRun")

`get_check_run`( _check\_run\_id: int_) → CheckRun [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_check_run "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/check-runs/{check\_run\_id}](https://docs.github.com/en/rest/reference/checks#get-a-check-run)

Parameters

**check\_run\_id** – int

Return type

[`github.CheckRun.CheckRun`](https://pygithub.readthedocs.io/en/stable/github_objects/CheckRun.html#github.CheckRun.CheckRun "github.CheckRun.CheckRun")

`get_artifacts`( _name: Opt\[str\] = NotSet_) → PaginatedList\[Artifact\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_artifacts "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/actions/artifacts](https://docs.github.com/en/rest/actions/artifacts#list-artifacts-for-a-repository)

Parameters

**name** – str

Return type

`PaginatedList` of [`github.Artifact.Artifact`](https://pygithub.readthedocs.io/en/stable/github_objects/Artifact.html#github.Artifact.Artifact "github.Artifact.Artifact")

`get_artifact`( _artifact\_id: int_) → Artifact [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_artifact "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/actions/artifacts/{artifact\_id}](https://docs.github.com/en/rest/actions/artifacts#get-an-artifact)

Parameters

**artifact\_id** – int

Return type

[`github.Artifact.Artifact`](https://pygithub.readthedocs.io/en/stable/github_objects/Artifact.html#github.Artifact.Artifact "github.Artifact.Artifact")

`get_codescan_alerts`() → PaginatedList\[CodeScanAlert\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_codescan_alerts "Permalink to this definition")Calls

[GET https://api.github.com/repos/{owner}/{repo}/code-scanning/alerts](https://docs.github.com/en/rest/reference/code-scanning#list-code-scanning-alerts-for-a-repository)

Return type

`PaginatedList` of [`github.CodeScanAlert.CodeScanAlert`](https://pygithub.readthedocs.io/en/stable/github_objects/CodeScanAlert.html#github.CodeScanAlert.CodeScanAlert "github.CodeScanAlert.CodeScanAlert")

`get_environments`() → github.PaginatedList.PaginatedList\[github.Environment.Environment\]\[github.Environment.Environment\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_environments "Permalink to this definition")Calls

[GET /repositories/{self.\_repository.id}/environments/{self.environment\_name}/environments](https://docs.github.com/en/rest/reference/deployments#get-all-environments)

Return type

`PaginatedList` of [`github.Environment.Environment`](https://pygithub.readthedocs.io/en/stable/github_objects/Environment.html#github.Environment.Environment "github.Environment.Environment")

`get_environment`( _environment\_name: str_) → github.Environment.Environment [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_environment "Permalink to this definition")Calls

[GET /repositories/{self.\_repository.id}/environments/{self.environment\_name}/environments/{environment\_name}](https://docs.github.com/en/rest/reference/deployments#get-an-environment)

Return type

[`github.Environment.Environment`](https://pygithub.readthedocs.io/en/stable/github_objects/Environment.html#github.Environment.Environment "github.Environment.Environment")

`create_environment`( _environment\_name: str_, _wait\_timer: int = 0_, _reviewers: list\[ReviewerParams\] = \[\]_, _deployment\_branch\_policy: EnvironmentDeploymentBranchPolicyParams \| None = None_) → Environment [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.create_environment "Permalink to this definition")Calls

[PUT /repositories/{self.\_repository.id}/environments/{self.environment\_name}/environments/{environment\_name}](https://docs.github.com/en/rest/reference/deployments#create-or-update-an-environment)

Parameters

- **environment\_name** – string

- **wait\_timer** – int

- **reviews** – List\[:class:github.EnvironmentDeploymentBranchPolicy.EnvironmentDeploymentBranchPolicyParams\]

- **deployment\_branch\_policy** – Optional\[:class:github.EnvironmentDeploymentBranchPolicy.EnvironmentDeploymentBranchPolicyParams\`\]


Return type

[`github.Environment.Environment`](https://pygithub.readthedocs.io/en/stable/github_objects/Environment.html#github.Environment.Environment "github.Environment.Environment")

`delete_environment`( _environment\_name: str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.delete_environment "Permalink to this definition")Calls

[DELETE /repositories/{self.\_repository.id}/environments/{self.environment\_name}/environments/{environment\_name}](https://docs.github.com/en/rest/reference/deployments#delete-an-environment)

Parameters

**environment\_name** – string

Return type

None

`get_dependabot_alerts`( _state: Opt\[str\] = NotSet_, _severity: Opt\[str\] = NotSet_, _ecosystem: Opt\[str\] = NotSet_, _package: Opt\[str\] = NotSet_, _manifest: Opt\[str\] = NotSet_, _scope: Opt\[str\] = NotSet_, _sort: Opt\[str\] = NotSet_, _direction: Opt\[str\] = NotSet_) → PaginatedList\[DependabotAlert\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_dependabot_alerts "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/dependabot/alerts](https://docs.github.com/en/rest/dependabot/alerts#list-dependabot-alerts-for-a-repository)

Parameters

- **state** – Optional string

- **severity** – Optional string

- **ecosystem** – Optional string

- **package** – Optional string

- **manifest** – Optional string

- **scope** – Optional string

- **sort** – Optional string

- **direction** – Optional string


Return type

`PaginatedList` of [`github.DependabotAlert.DependabotAlert`](https://pygithub.readthedocs.io/en/stable/github_objects/DependabotAlert.html#github.DependabotAlert.DependabotAlert "github.DependabotAlert.DependabotAlert")

`get_dependabot_alert`( _number: int_) → DependabotAlert [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_dependabot_alert "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/dependabot/alerts/{alert\_number}](https://docs.github.com/en/rest/dependabot/alerts#get-a-dependabot-alert)

Parameters

**number** – int

Return type

[`github.DependabotAlert.DependabotAlert`](https://pygithub.readthedocs.io/en/stable/github_objects/DependabotAlert.html#github.DependabotAlert.DependabotAlert "github.DependabotAlert.DependabotAlert")

`update_dependabot_alert`( _number: int_, _state: str_, _dismissed\_reason: Opt\[str\] = NotSet_, _dismissed\_comment: Opt\[str\] = NotSet_) → DependabotAlert [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.update_dependabot_alert "Permalink to this definition")Calls

[PATCH /repos/{owner}/{repo}/dependabot/alerts/{alert\_number}](https://docs.github.com/en/rest/dependabot/alerts#update-a-dependabot-alert)

Parameters

- **number** – int

- **state** – string

- **dismissed\_reason** – Optional string

- **dismissed\_comment** – Optional string


Return type

[`github.DependabotAlert.DependabotAlert`](https://pygithub.readthedocs.io/en/stable/github_objects/DependabotAlert.html#github.DependabotAlert.DependabotAlert "github.DependabotAlert.DependabotAlert")

`get_custom_properties`() → dict\[str, None \| str \| list\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_custom_properties "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/properties/values](https://docs.github.com/en/rest/repos/custom-properties#get-all-custom-property-values-for-a-repository)

Return type

dict\[str, None \| str \| list\]

`update_custom_properties`( _properties: dict\[str, None \| str \| list\]_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.update_custom_properties "Permalink to this definition")Calls

[PATCH /repos/{owner}/{repo}/properties/values](https://docs.github.com/en/rest/repos/custom-properties#create-or-update-custom-property-values-for-a-repository)

Return type

None

`attach_security_config`( _id: int_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.attach_security_config "Permalink to this definition")Calls

[POST /orgs/{org}/code-security/configurations/{configuration\_id}/attach](https://docs.github.com/en/rest/code-security/configurations#attach-a-configuration-to-repositories)

`detach_security_config`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.detach_security_config "Permalink to this definition")Calls

[DELETE /orgs/{org}/code-security/configurations/detach](https://docs.github.com/en/rest/code-security/configurations#detach-configurations-from-repositories)

`get_security_config`() → RepoCodeSecurityConfig \| None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.get_security_config "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/code-security-configuration](https://docs.github.com/en/rest/code-security/configurations?apiVersion=2022-11-28#get-the-code-security-configuration-associated-with-a-repository)

Return type

RepoCodeSecurityConfig \| None

`transfer_ownership`( _new\_owner: str_, _new\_name: Opt\[str\] = NotSet_, _teams: Opt\[list\[int\]\] = NotSet_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository.transfer_ownership "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/transfer](https://docs.github.com/en/rest/repos/repos#transfer-a-repository)

Parameters

- **new\_owner** – string

- **new\_name** – Optional string

- **teams** – Optional list of int


Return type

bool