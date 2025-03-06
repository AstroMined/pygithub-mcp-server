- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- ApplicationOAuth
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/ApplicationOAuth.rst.txt)

* * *

# ApplicationOAuth [¶](https://pygithub.readthedocs.io/en/stable/github_objects/ApplicationOAuth.html\#applicationoauth "Permalink to this headline")

_class_ `github.ApplicationOAuth.` `ApplicationOAuth` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/ApplicationOAuth.html#github.ApplicationOAuth.ApplicationOAuth "Permalink to this definition")

This class is used for identifying and authorizing users for Github Apps.

The reference can be found at
[https://docs.github.com/en/developers/apps/building-github-apps/identifying-and-authorizing-users-for-github-apps](https://docs.github.com/en/developers/apps/building-github-apps/identifying-and-authorizing-users-for-github-apps)

`get_login_url`( _redirect\_uri: str \| None = None_, _state: str \| None = None_, _login: str \| None = None_) → str [¶](https://pygithub.readthedocs.io/en/stable/github_objects/ApplicationOAuth.html#github.ApplicationOAuth.ApplicationOAuth.get_login_url "Permalink to this definition")

Return the URL you need to redirect a user to in order to authorize your App.

`get_access_token`( _code: str_, _state: str \| None = None_) → AccessToken [¶](https://pygithub.readthedocs.io/en/stable/github_objects/ApplicationOAuth.html#github.ApplicationOAuth.ApplicationOAuth.get_access_token "Permalink to this definition")Calls

[POST /login/oauth/access\_token](https://docs.github.com/en/developers/apps/identifying-and-authorizing-users-for-github-apps)

`refresh_access_token`( _refresh\_token: str_) → AccessToken [¶](https://pygithub.readthedocs.io/en/stable/github_objects/ApplicationOAuth.html#github.ApplicationOAuth.ApplicationOAuth.refresh_access_token "Permalink to this definition")Calls

[POST /login/oauth/access\_token](https://docs.github.com/en/developers/apps/identifying-and-authorizing-users-for-github-apps)

Parameters

**refresh\_token** – string