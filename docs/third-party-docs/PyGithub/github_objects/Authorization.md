- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- Authorization
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/Authorization.rst.txt)

* * *

# Authorization [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Authorization.html\#authorization "Permalink to this headline")

_class_ `github.Authorization.` `Authorization` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Authorization.html#github.Authorization.Authorization "Permalink to this definition")

This class represents Authorizations.

The reference can be found here
[https://docs.github.com/en/enterprise-server@3.0/rest/reference/oauth-authorizations](https://docs.github.com/en/enterprise-server@3.0/rest/reference/oauth-authorizations)

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


_property_ `created_at` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Authorization.html#github.Authorization.Authorization.created_at "Permalink to this definition")Type

datetime.datetime

`delete`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Authorization.html#github.Authorization.Authorization.delete "Permalink to this definition")Calls

[DELETE /authorizations/{id}](https://docs.github.com/en/developers/apps/authorizing-oauth-apps)

`edit`( _scopes: Opt\[list\[str\]\] = NotSet_, _add\_scopes: Opt\[list\[str\]\] = NotSet_, _remove\_scopes: Opt\[list\[str\]\] = NotSet_, _note: Opt\[str\] = NotSet_, _note\_url: Opt\[str\] = NotSet_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Authorization.html#github.Authorization.Authorization.edit "Permalink to this definition")Calls

[PATCH /authorizations/{id}](https://docs.github.com/en/developers/apps/authorizing-oauth-apps)

Parameters

- **scopes** – list of string

- **add\_scopes** – list of string

- **remove\_scopes** – list of string

- **note** – string

- **note\_url** – string


Return type

None