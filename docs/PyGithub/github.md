- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- Main class: Github
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github.rst.txt)

* * *

# Main class: Github [¶](https://pygithub.readthedocs.io/en/stable/github.html\#main-class-github "Permalink to this headline")

_class_ `github.MainClass.` `Github`( _login\_or\_token: str \| None = None_, _password: str \| None = None_, _jwt: str \| None = None_, _app\_auth: AppAuthentication \| None = None_, _base\_url: str = 'https://api.github.com'_, _timeout: int = 15_, _user\_agent: str = 'PyGithub/Python'_, _per\_page: int = 30_, _verify: bool \| str = True_, _retry: int \| Retry \| None = GithubRetry(total=10_, _connect=None_, _read=None_, _redirect=None_, _status=None)_, _pool\_size: int \| None = None_, _seconds\_between\_requests: float \| None = 0.25_, _seconds\_between\_writes: float \| None = 1.0_, _auth: github.Auth.Auth \| None = None_, _lazy: bool = False_) [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github "Permalink to this definition")

This is the main class you instantiate to access the Github API v3.

Optional parameters allow different authentication methods.

Parameters

- **login\_or\_token** – string deprecated, use auth=github.Auth.Login(…) or auth=github.Auth.Token(…) instead

- **password** – string deprecated, use auth=github.Auth.Login(…) instead

- **jwt** – string deprecated, use auth=github.Auth.AppAuth(…) or auth=github.Auth.AppAuthToken(…) instead

- **app\_auth** – github.AppAuthentication deprecated, use auth=github.Auth.AppInstallationAuth(…) instead

- **base\_url** – string

- **timeout** – integer

- **user\_agent** – string

- **per\_page** – int

- **verify** – boolean or string

- **retry** – int or urllib3.util.retry.Retry object,
defaults to github.Github.default\_retry,
set to None to disable retries

- **pool\_size** – int

- **seconds\_between\_requests** – float

- **seconds\_between\_writes** – float

- **auth** – authentication method

- **lazy** – completable objects created from this instance are lazy,
as well as completable objects created from those, and so on


`withLazy`( _lazy: bool_) → github.MainClass.Github [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.withLazy "Permalink to this definition")

Create a Github instance with identical configuration but the given lazy setting.

Parameters

**lazy** – completable objects created from this instance are lazy, as well as completable objects created
from those, and so on

Returns

new Github instance

`close`() → None [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.close "Permalink to this definition")

Close connections to the server. Alternatively, use the Github
object as a context manager:

```
with github.Github(...) as gh:
  # do something

```

_property_ `requester` [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.requester "Permalink to this definition")

Return my Requester object.

For example, to make requests to API endpoints not yet supported by PyGitHub.

_property_ `rate_limiting` [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.rate_limiting "Permalink to this definition")

First value is requests remaining, second value is request limit.

_property_ `rate_limiting_resettime` [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.rate_limiting_resettime "Permalink to this definition")

Unix timestamp indicating when rate limiting will reset.

`get_rate_limit`() → github.RateLimit.RateLimit [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_rate_limit "Permalink to this definition")

Rate limit status for different resources (core/search/graphql).

[:calls:\`GET /rate\_limit <https://docs.github.com/en/rest/reference/rate-limit>\`\_](https://pygithub.readthedocs.io/en/stable/github.html#id1)

_property_ `oauth_scopes` [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.oauth_scopes "Permalink to this definition")Type

list of string

`get_license`( _key: Opt\[str\] = NotSet_) → License [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_license "Permalink to this definition")Calls

[GET /license/{license}](https://docs.github.com/en/rest/reference/licenses#get-a-license)

`get_licenses`() → PaginatedList\[License\] [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_licenses "Permalink to this definition")Calls

[GET /licenses](https://docs.github.com/en/rest/reference/licenses#get-all-commonly-used-licenses)

`get_events`() → PaginatedList\[Event\] [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_events "Permalink to this definition")Calls

[GET /events](https://docs.github.com/en/rest/reference/activity#list-public-events)

`get_user`( _login: Opt\[str\] = NotSet_) → NamedUser \| AuthenticatedUser [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_user "Permalink to this definition")Calls

[GET /users/{user}](https://docs.github.com/en/rest/reference/users) or [GET /user](https://docs.github.com/en/rest/reference/users)

`get_user_by_id`( _user\_id: int_) → NamedUser [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_user_by_id "Permalink to this definition")Calls

[GET /user/{id}](https://docs.github.com/en/rest/reference/users)

Parameters

**user\_id** – int

Return type

[`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser")

`get_users`( _since: Opt\[int\] = NotSet_) → PaginatedList\[NamedUser\] [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_users "Permalink to this definition")Calls

[GET /users](https://docs.github.com/en/rest/reference/users)

`get_organization`( _org: str_) → Organization [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_organization "Permalink to this definition")Calls

[GET /orgs/{org}](https://docs.github.com/en/rest/reference/orgs)

`get_organizations`( _since: Opt\[int\] = NotSet_) → PaginatedList\[Organization\] [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_organizations "Permalink to this definition")Calls

[GET /organizations](https://docs.github.com/en/rest/reference/orgs#list-organizations)

`get_enterprise`( _enterprise: str_) → github.Enterprise.Enterprise [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_enterprise "Permalink to this definition")Calls

[GET /enterprises/{enterprise}](https://docs.github.com/en/enterprise-cloud@latest/rest/enterprise-admin)

Parameters

**enterprise** – string

Return type

`Enterprise`

`get_repo`( _full\_name\_or\_id: int \| str_, _lazy: bool = False_) → Repository [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_repo "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}](https://docs.github.com/en/rest/reference/repos) or [GET /repositories/{id}](https://docs.github.com/en/rest/reference/repos)

`get_repos`( _since: Opt\[int\] = NotSet_, _visibility: Opt\[str\] = NotSet_) → PaginatedList\[Repository\] [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_repos "Permalink to this definition")Calls

[GET /repositories](https://docs.github.com/en/rest/reference/repos#list-public-repositories)

Parameters

- **since** – integer

- **visibility** – string ('all','public')


`get_project`( _id: int_) → Project [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_project "Permalink to this definition")Calls

[GET /projects/{project\_id}](https://docs.github.com/en/rest/reference/projects#get-a-project)

`get_project_column`( _id: int_) → ProjectColumn [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_project_column "Permalink to this definition")Calls

[GET /projects/columns/{column\_id}](https://docs.github.com/en/rest/reference/projects#get-a-project-column)

`get_gist`( _id: str_) → Gist [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_gist "Permalink to this definition")Calls

[GET /gists/{id}](https://docs.github.com/en/rest/reference/gists)

`get_gists`( _since: Opt\[datetime\] = NotSet_) → PaginatedList\[Gist\] [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_gists "Permalink to this definition")Calls

[GET /gists/public](https://docs.github.com/en/rest/reference/gists)

`get_global_advisory`( _ghsa\_id: str_) → GlobalAdvisory [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_global_advisory "Permalink to this definition")Calls

[GET /advisories/{ghsa\_id}](https://docs.github.com/en/rest/security-advisories/global-advisories)

Parameters

**ghsa\_id** – string

Return type

[`github.GlobalAdvisory.GlobalAdvisory`](https://pygithub.readthedocs.io/en/stable/github_objects/GlobalAdvisory.html#github.GlobalAdvisory.GlobalAdvisory "github.GlobalAdvisory.GlobalAdvisory")

`get_global_advisories`( _type: Opt\[str\] = NotSet_, _ghsa\_id: Opt\[str\] = NotSet_, _cve\_id: Opt\[str\] = NotSet_, _ecosystem: Opt\[str\] = NotSet_, _severity: Opt\[str\] = NotSet_, _cwes: list\[Opt\[str\]\] \| Opt\[str\] = NotSet_, _is\_withdrawn: Opt\[bool\] = NotSet_, _affects: list\[str\] \| Opt\[str\] = NotSet_, _published: Opt\[str\] = NotSet_, _updated: Opt\[str\] = NotSet_, _modified: Opt\[str\] = NotSet_, _keywords: Opt\[str\] = NotSet_, _before: Opt\[str\] = NotSet_, _after: Opt\[str\] = NotSet_, _per\_page: Opt\[str\] = NotSet_, _sort: Opt\[str\] = NotSet_, _direction: Opt\[str\] = NotSet_) → PaginatedList\[GlobalAdvisory\] [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_global_advisories "Permalink to this definition")Calls

GET /advisories <https://docs.github.com/en/rest/security-advisories/global-advisories>

Parameters

- **type** – Optional string

- **ghsa\_id** – Optional string

- **cve\_id** – Optional string

- **ecosystem** – Optional string

- **severity** – Optional string

- **cwes** – Optional comma separated string or list of integer or string

- **is\_withdrawn** – Optional bool

- **affects** – Optional comma separated string or list of string

- **published** – Optional string

- **updated** – Optional string

- **modified** – Optional string

- **before** – Optional string

- **after** – Optional string

- **sort** – Optional string

- **direction** – Optional string


Return type

[`github.PaginatedList.PaginatedList`](https://pygithub.readthedocs.io/en/stable/utilities.html#github.PaginatedList.PaginatedList "github.PaginatedList.PaginatedList") of [`github.GlobalAdvisory.GlobalAdvisory`](https://pygithub.readthedocs.io/en/stable/github_objects/GlobalAdvisory.html#github.GlobalAdvisory.GlobalAdvisory "github.GlobalAdvisory.GlobalAdvisory")

`search_repositories`( _query: str_, _sort: Opt\[str\] = NotSet_, _order: Opt\[str\] = NotSet_, _\*\*qualifiers: Any_) → PaginatedList\[Repository\] [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.search_repositories "Permalink to this definition")Calls

[GET /search/repositories](https://docs.github.com/en/rest/reference/search)

Parameters

- **query** – string

- **sort** – string ('stars', 'forks', 'updated')

- **order** – string ('asc', 'desc')

- **qualifiers** – keyword dict query qualifiers


`search_users`( _query: str_, _sort: Opt\[str\] = NotSet_, _order: Opt\[str\] = NotSet_, _\*\*qualifiers: Any_) → PaginatedList\[NamedUser\] [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.search_users "Permalink to this definition")Calls

[GET /search/users](https://docs.github.com/en/rest/reference/search)

Parameters

- **query** – string

- **sort** – string ('followers', 'repositories', 'joined')

- **order** – string ('asc', 'desc')

- **qualifiers** – keyword dict query qualifiers


Return type

`PaginatedList` of [`github.NamedUser.NamedUser`](https://pygithub.readthedocs.io/en/stable/github_objects/NamedUser.html#github.NamedUser.NamedUser "github.NamedUser.NamedUser")

`search_issues`( _query: str_, _sort: Opt\[str\] = NotSet_, _order: Opt\[str\] = NotSet_, _\*\*qualifiers: Any_) → PaginatedList\[Issue\] [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.search_issues "Permalink to this definition")Calls

[GET /search/issues](https://docs.github.com/en/rest/reference/search)

Parameters

- **query** – string

- **sort** – string ('comments', 'created', 'updated')

- **order** – string ('asc', 'desc')

- **qualifiers** – keyword dict query qualifiers


Return type

`PaginatedList` of [`github.Issue.Issue`](https://pygithub.readthedocs.io/en/stable/github_objects/Issue.html#github.Issue.Issue "github.Issue.Issue")

`search_code`( _query: str_, _sort: Opt\[str\] = NotSet_, _order: Opt\[str\] = NotSet_, _highlight: bool = False_, _\*\*qualifiers: Any_) → PaginatedList\[ContentFile\] [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.search_code "Permalink to this definition")Calls

[GET /search/code](https://docs.github.com/en/rest/reference/search)

Parameters

- **query** – string

- **sort** – string ('indexed')

- **order** – string ('asc', 'desc')

- **highlight** – boolean (True, False)

- **qualifiers** – keyword dict query qualifiers


Return type

`PaginatedList` of [`github.ContentFile.ContentFile`](https://pygithub.readthedocs.io/en/stable/github_objects/ContentFile.html#github.ContentFile.ContentFile "github.ContentFile.ContentFile")

`search_commits`( _query: str_, _sort: Opt\[str\] = NotSet_, _order: Opt\[str\] = NotSet_, _\*\*qualifiers: Any_) → PaginatedList\[Commit\] [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.search_commits "Permalink to this definition")Calls

[GET /search/commits](https://docs.github.com/en/rest/reference/search)

Parameters

- **query** – string

- **sort** – string ('author-date', 'committer-date')

- **order** – string ('asc', 'desc')

- **qualifiers** – keyword dict query qualifiers


Return type

`PaginatedList` of [`github.Commit.Commit`](https://pygithub.readthedocs.io/en/stable/github_objects/Commit.html#github.Commit.Commit "github.Commit.Commit")

`search_topics`( _query: str_, _\*\*qualifiers: Any_) → PaginatedList\[Topic\] [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.search_topics "Permalink to this definition")Calls

[GET /search/topics](https://docs.github.com/en/rest/reference/search)

Parameters

- **query** – string

- **qualifiers** – keyword dict query qualifiers


Return type

`PaginatedList` of [`github.Topic.Topic`](https://pygithub.readthedocs.io/en/stable/github_objects/Topic.html#github.Topic.Topic "github.Topic.Topic")

`render_markdown`( _text: str_, _context: Opt\[Repository\] = NotSet_) → str [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.render_markdown "Permalink to this definition")Calls

[POST /markdown](https://docs.github.com/en/rest/reference/markdown)

Parameters

- **text** – string

- **context** – [`github.Repository.Repository`](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html#github.Repository.Repository "github.Repository.Repository")


Return type

string

`get_hook`( _name: str_) → github.HookDescription.HookDescription [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_hook "Permalink to this definition")Calls

[GET /hooks/{name}](https://docs.github.com/en/rest/reference/repos#webhooks)

`get_hooks`() → list\[HookDescription\] [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_hooks "Permalink to this definition")Calls

[GET /hooks](https://docs.github.com/en/rest/reference/repos#webhooks)

Return type

list of [`github.HookDescription.HookDescription`](https://pygithub.readthedocs.io/en/stable/github_objects/HookDescription.html#github.HookDescription.HookDescription "github.HookDescription.HookDescription")

`get_hook_delivery`( _hook\_id: int_, _delivery\_id: int_) → github.HookDelivery.HookDelivery [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_hook_delivery "Permalink to this definition")Calls

[GET /hooks/{hook\_id}/deliveries/{delivery\_id}](https://docs.github.com/en/rest/reference/repos#webhooks)

Parameters

- **hook\_id** – integer

- **delivery\_id** – integer


Return type

`HookDelivery`

`get_hook_deliveries`( _hook\_id: int_) → list\[HookDeliverySummary\] [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_hook_deliveries "Permalink to this definition")Calls

[GET /hooks/{hook\_id}/deliveries](https://docs.github.com/en/rest/reference/repos#webhooks)

Parameters

**hook\_id** – integer

Return type

list of `HookDeliverySummary`

`get_gitignore_templates`() → list\[str\] [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_gitignore_templates "Permalink to this definition")Calls

[GET /gitignore/templates](https://docs.github.com/en/rest/reference/gitignore)

`get_gitignore_template`( _name: str_) → GitignoreTemplate [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_gitignore_template "Permalink to this definition")Calls

[GET /gitignore/templates/{name}](https://docs.github.com/en/rest/reference/gitignore)

`get_emojis`() → dict\[str, str\] [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_emojis "Permalink to this definition")Calls

[GET /emojis](https://docs.github.com/en/rest/reference/emojis)

Return type

dictionary of type => url for emoji\`

`create_from_raw_data`( _klass: type\[TGithubObject\], raw\_data: dict\[str, Any\], headers: dict\[str, str \| int\] \| None = None_) → TGithubObject [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.create_from_raw_data "Permalink to this definition")

Creates an object from raw\_data previously obtained by `GithubObject.raw_data`, and optionally headers
previously obtained by `GithubObject.raw_headers`.

Parameters

- **klass** – the class of the object to create

- **raw\_data** – dict

- **headers** – dict


Return type

instance of class `klass`

`dump`( _obj: github.GithubObject.GithubObject_, _file: BinaryIO_, _protocol: int = 0_) → None [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.dump "Permalink to this definition")

Dumps (pickles) a PyGithub object to a file-like object. Some effort is made to not pickle sensitive
information like the Github credentials used in the [`Github`](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github "github.MainClass.Github") instance. But NO EFFORT is made to remove
sensitive information from the object's attributes.

Parameters

- **obj** – the object to pickle

- **file** – the file-like object to pickle to

- **protocol** – the [pickling protocol](https://python.readthedocs.io/en/latest/library/pickle.html#data-stream-format)


`load`( _f: BinaryIO_) → Any [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.load "Permalink to this definition")

Loads (unpickles) a PyGithub object from a file-like object.

Parameters

**f** – the file-like object to unpickle from

Returns

the unpickled object

`get_app`( _slug: Opt\[str\] = NotSet_) → GithubApp [¶](https://pygithub.readthedocs.io/en/stable/github.html#github.MainClass.Github.get_app "Permalink to this definition")Calls

[GET /apps/{slug}](https://docs.github.com/en/rest/reference/apps) or [GET /app](https://docs.github.com/en/rest/reference/apps)