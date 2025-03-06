- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- Migration
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/Migration.rst.txt)

* * *

# Migration [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Migration.html\#migration "Permalink to this headline")

_class_ `github.Migration.` `Migration` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Migration.html#github.Migration.Migration "Permalink to this definition")

This class represents Migrations.

The reference can be found here
[https://docs.github.com/en/rest/reference/migrations](https://docs.github.com/en/rest/reference/migrations)

The OpenAPI schema can be found at
\- /components/schemas/migration

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


`get_status`() → str [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Migration.html#github.Migration.Migration.get_status "Permalink to this definition")Calls

[GET /user/migrations/{migration\_id}](https://docs.github.com/en/rest/reference/migrations)

`get_archive_url`() → str [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Migration.html#github.Migration.Migration.get_archive_url "Permalink to this definition")Calls

[GET /user/migrations/{migration\_id}/archive](https://docs.github.com/en/rest/reference/migrations)

`delete`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Migration.html#github.Migration.Migration.delete "Permalink to this definition")Calls

[DELETE /user/migrations/{migration\_id}/archive](https://docs.github.com/en/rest/reference/migrations)

`unlock_repo`( _repo\_name: str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Migration.html#github.Migration.Migration.unlock_repo "Permalink to this definition")Calls

[DELETE /user/migrations/{migration\_id}/repos/{repo\_name}/lock](https://docs.github.com/en/rest/reference/migrations)