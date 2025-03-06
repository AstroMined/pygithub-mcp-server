- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- GitReleaseAsset
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/GitReleaseAsset.rst.txt)

* * *

# GitReleaseAsset [¶](https://pygithub.readthedocs.io/en/stable/github_objects/GitReleaseAsset.html\#gitreleaseasset "Permalink to this headline")

_class_ `github.GitReleaseAsset.` `GitReleaseAsset` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/GitReleaseAsset.html#github.GitReleaseAsset.GitReleaseAsset "Permalink to this definition")

This class represents GitReleaseAssets.

The reference can be found here
[https://docs.github.com/en/rest/reference/repos#releases](https://docs.github.com/en/rest/reference/repos#releases)

The OpenAPI schema can be found at
\- /components/schemas/release-asset

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


`delete_asset`() → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/GitReleaseAsset.html#github.GitReleaseAsset.GitReleaseAsset.delete_asset "Permalink to this definition")

Delete asset from the release.

`download_asset`( _path: None \| str = None_, _chunk\_size: int \| None = 1_) → tuple\[int, dict\[str, Any\], Iterator\] \| None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/GitReleaseAsset.html#github.GitReleaseAsset.GitReleaseAsset.download_asset "Permalink to this definition")

Download asset to the path or return an iterator for the stream.

`update_asset`( _name: str_, _label: str = ''_) → github.GitReleaseAsset.GitReleaseAsset [¶](https://pygithub.readthedocs.io/en/stable/github_objects/GitReleaseAsset.html#github.GitReleaseAsset.GitReleaseAsset.update_asset "Permalink to this definition")

Update asset metadata.