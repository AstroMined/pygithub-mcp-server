- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- Gist
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/Gist.rst.txt)

* * *

# Gist [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Gist.html\#gist "Permalink to this headline")

_class_ `github.Gist.` `Gist` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Gist.html#github.Gist.Gist "Permalink to this definition")

This class represents Gists.

The reference can be found here
[https://docs.github.com/en/rest/reference/gists](https://docs.github.com/en/rest/reference/gists)

The OpenAPI schema can be found at
\- /components/schemas/base-gist
\- /components/schemas/gist-simple
\- /components/schemas/gist-simple/properties/fork\_of
\- /components/schemas/gist-simple/properties/forks/items

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


`create_comment`( _body: str_) → GistComment [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Gist.html#github.Gist.Gist.create_comment "Permalink to this definition")Calls

[POST /gists/{gist\_id}/comments](https://docs.github.com/en/rest/reference/gists#comments)

`create_fork`() → github.Gist.Gist [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Gist.html#github.Gist.Gist.create_fork "Permalink to this definition")Calls

[POST /gists/{id}/forks](https://docs.github.com/en/rest/reference/gists)

`delete`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Gist.html#github.Gist.Gist.delete "Permalink to this definition")Calls

[DELETE /gists/{id}](https://docs.github.com/en/rest/reference/gists)

`edit`( _description: Opt\[str\] = NotSet_, _files: Opt\[dict\[str_, _InputFileContent \| None\]\] = NotSet_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Gist.html#github.Gist.Gist.edit "Permalink to this definition")Calls

[PATCH /gists/{id}](https://docs.github.com/en/rest/reference/gists)

`get_comment`( _id: int_) → GistComment [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Gist.html#github.Gist.Gist.get_comment "Permalink to this definition")Calls

[GET /gists/{gist\_id}/comments/{id}](https://docs.github.com/en/rest/reference/gists#comments)

`get_comments`() → PaginatedList\[GistComment\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Gist.html#github.Gist.Gist.get_comments "Permalink to this definition")Calls

[GET /gists/{gist\_id}/comments](https://docs.github.com/en/rest/reference/gists#comments)

`is_starred`() → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Gist.html#github.Gist.Gist.is_starred "Permalink to this definition")Calls

[GET /gists/{id}/star](https://docs.github.com/en/rest/reference/gists)

`reset_starred`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Gist.html#github.Gist.Gist.reset_starred "Permalink to this definition")Calls

[DELETE /gists/{id}/star](https://docs.github.com/en/rest/reference/gists)

`set_starred`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Gist.html#github.Gist.Gist.set_starred "Permalink to this definition")Calls

[PUT /gists/{id}/star](https://docs.github.com/en/rest/reference/gists)