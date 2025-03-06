- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- ContentFile
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/ContentFile.rst.txt)

* * *

# ContentFile [¶](https://pygithub.readthedocs.io/en/stable/github_objects/ContentFile.html\#contentfile "Permalink to this headline")

_class_ `github.ContentFile.` `ContentFile` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/ContentFile.html#github.ContentFile.ContentFile "Permalink to this definition")

This class represents ContentFiles.

The reference can be found here
[https://docs.github.com/en/rest/reference/repos#contents](https://docs.github.com/en/rest/reference/repos#contents)

The OpenAPI schema can be found at
\- /components/schemas/code-search-result-item
\- /components/schemas/content-directory
\- /components/schemas/content-file
\- /components/schemas/content-submodule
\- /components/schemas/content-symlink
\- /components/schemas/file-commit
\- /components/schemas/license-content

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