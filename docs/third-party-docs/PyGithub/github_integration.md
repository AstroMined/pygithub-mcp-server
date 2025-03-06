- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- Main class: GithubIntegration
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_integration.rst.txt)

* * *

# Main class: GithubIntegration [¶](https://pygithub.readthedocs.io/en/stable/github_integration.html\#main-class-githubintegration "Permalink to this headline")

_class_ `github.GithubIntegration.` `GithubIntegration`( _integration\_id: int \| str \| None = None_, _private\_key: str \| None = None_, _base\_url: str = 'https://api.github.com'_, _\*_, _timeout: int = 15_, _user\_agent: str = 'PyGithub/Python'_, _per\_page: int = 30_, _verify: bool \| str = True_, _retry: int \| Retry \| None = None_, _pool\_size: int \| None = None_, _seconds\_between\_requests: float \| None = 0.25_, _seconds\_between\_writes: float \| None = 1.0_, _jwt\_expiry: int = 300_, _jwt\_issued\_at: int = -60_, _jwt\_algorithm: str = 'RS256'_, _auth: AppAuth \| None = None_, _lazy: bool = False_) [¶](https://pygithub.readthedocs.io/en/stable/github_integration.html#github.GithubIntegration.GithubIntegration "Permalink to this definition")

Main class to obtain tokens for a GitHub integration.

Parameters

- **integration\_id** – int deprecated, use auth=github.Auth.AppAuth(…) instead

- **private\_key** – string deprecated, use auth=github.Auth.AppAuth(…) instead

- **base\_url** – string

- **timeout** – integer

- **user\_agent** – string

- **per\_page** – int

- **verify** – boolean or string

- **retry** – int or urllib3.util.retry.Retry object

- **pool\_size** – int

- **seconds\_between\_requests** – float

- **seconds\_between\_writes** – float

- **jwt\_expiry** – int deprecated, use auth=github.Auth.AppAuth(…) instead

- **jwt\_issued\_at** – int deprecated, use auth=github.Auth.AppAuth(…) instead

- **jwt\_algorithm** – string deprecated, use auth=github.Auth.AppAuth(…) instead

- **auth** – authentication method

- **lazy** – completable objects created from this instance are lazy,
as well as completable objects created from those, and so on


`withLazy`( _lazy: bool_) → github.GithubIntegration.GithubIntegration [¶](https://pygithub.readthedocs.io/en/stable/github_integration.html#github.GithubIntegration.GithubIntegration.withLazy "Permalink to this definition")

Create a GithubIntegration instance with identical configuration but the given lazy setting.

Parameters

**lazy** – completable objects created from this instance are lazy, as well as completable objects created
from those, and so on

Returns

new Github instance

`close`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_integration.html#github.GithubIntegration.GithubIntegration.close "Permalink to this definition")

Close connections to the server. Alternatively, use the
GithubIntegration object as a context manager:

```
with github.GithubIntegration(...) as gi:
  # do something

```

_property_ `requester` [¶](https://pygithub.readthedocs.io/en/stable/github_integration.html#github.GithubIntegration.GithubIntegration.requester "Permalink to this definition")

Return my Requester object.

For example, to make requests to API endpoints not yet supported by PyGitHub.

`create_jwt`( _expiration: int \| None = None_) → str [¶](https://pygithub.readthedocs.io/en/stable/github_integration.html#github.GithubIntegration.GithubIntegration.create_jwt "Permalink to this definition")

Create a signed JWT
[https://docs.github.com/en/developers/apps/building-github-apps/authenticating-with-github-apps#authenticating-as-a-github-app](https://docs.github.com/en/developers/apps/building-github-apps/authenticating-with-github-apps#authenticating-as-a-github-app)

`get_access_token`( _installation\_id: int_, _permissions: dict\[str_, _str\] \| None = None_) → InstallationAuthorization [¶](https://pygithub.readthedocs.io/en/stable/github_integration.html#github.GithubIntegration.GithubIntegration.get_access_token "Permalink to this definition")Calls

POST /app/installations/{installation\_id}/access\_tokens <https://docs.github.com/en/rest/apps/apps#create-an-installation-access-token-for-an-app>

`get_installation`( _owner: str_, _repo: str_) → github.Installation.Installation [¶](https://pygithub.readthedocs.io/en/stable/github_integration.html#github.GithubIntegration.GithubIntegration.get_installation "Permalink to this definition")

Deprecated by get\_repo\_installation.

[:calls:\`GET /repos/{owner}/{repo}/installation <https://docs.github.com/en/rest/reference/apps#get-a-repository-\\
installation-for-the-authenticated-app>\`](https://pygithub.readthedocs.io/en/stable/github_integration.html#id1) [:calls:\`GET /repos/{owner}/{repo}/installation <https://docs.github.com/en/rest/reference/apps#get-a-repository-\\
installation-for-the-authenticated-app>\`](https://pygithub.readthedocs.io/en/stable/github_integration.html#id3)

`get_installations`() → github.PaginatedList.PaginatedList\[github.Installation.Installation\]\[github.Installation.Installation\] [¶](https://pygithub.readthedocs.io/en/stable/github_integration.html#github.GithubIntegration.GithubIntegration.get_installations "Permalink to this definition")Calls

GET /app/installations < [https://docs.github.com/en/rest/reference/apps#list-installations-for-the-authenticated-app](https://docs.github.com/en/rest/reference/apps#list-installations-for-the-authenticated-app) >

`get_org_installation`( _org: str_) → github.Installation.Installation [¶](https://pygithub.readthedocs.io/en/stable/github_integration.html#github.GithubIntegration.GithubIntegration.get_org_installation "Permalink to this definition")Calls

GET /orgs/{org}/installation <https://docs.github.com/en/rest/apps/apps#get-an-organization-installation-for-the-authenticated-app>

`get_repo_installation`( _owner: str_, _repo: str_) → github.Installation.Installation [¶](https://pygithub.readthedocs.io/en/stable/github_integration.html#github.GithubIntegration.GithubIntegration.get_repo_installation "Permalink to this definition")Calls

GET /repos/{owner}/{repo}/installation <https://docs.github.com/en/rest/reference/apps#get-a-repository-installation-for-the-authenticated-app>

`get_user_installation`( _username: str_) → github.Installation.Installation [¶](https://pygithub.readthedocs.io/en/stable/github_integration.html#github.GithubIntegration.GithubIntegration.get_user_installation "Permalink to this definition")Calls

GET /users/{username}/installation <https://docs.github.com/en/rest/apps/apps#get-a-user-installation-for-the-authenticated-app>

`get_app_installation`( _installation\_id: int_) → github.Installation.Installation [¶](https://pygithub.readthedocs.io/en/stable/github_integration.html#github.GithubIntegration.GithubIntegration.get_app_installation "Permalink to this definition")Calls

GET /app/installations/{installation\_id} <https://docs.github.com/en/rest/apps/apps#get-an-installation-for-the-authenticated-app>

`get_app`() → github.GithubApp.GithubApp [¶](https://pygithub.readthedocs.io/en/stable/github_integration.html#github.GithubIntegration.GithubIntegration.get_app "Permalink to this definition")Calls

[GET /app](https://docs.github.com/en/rest/reference/apps#get-the-authenticated-app)