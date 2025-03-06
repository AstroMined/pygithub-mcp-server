- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- GitRef
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/GitRef.rst.txt)

* * *

# GitRef [¶](https://pygithub.readthedocs.io/en/stable/github_objects/GitRef.html\#gitref "Permalink to this headline")

_class_ `github.GitRef.` `GitRef` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/GitRef.html#github.GitRef.GitRef "Permalink to this definition")

This class represents GitRefs.

The reference can be found here
[https://docs.github.com/en/rest/reference/git#references](https://docs.github.com/en/rest/reference/git#references)

The OpenAPI schema can be found at
\- /components/schemas/git-ref

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


`delete`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/GitRef.html#github.GitRef.GitRef.delete "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/git/refs/{ref}](https://docs.github.com/en/rest/reference/git#references)

`edit`( _sha: str_, _force: Union\[bool_, _github.GithubObject.\_NotSetType\] = NotSet_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/GitRef.html#github.GitRef.GitRef.edit "Permalink to this definition")Calls

[PATCH /repos/{owner}/{repo}/git/refs/{ref}](https://docs.github.com/en/rest/reference/git#references)