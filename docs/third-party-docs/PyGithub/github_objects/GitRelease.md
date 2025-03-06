- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- GitRelease
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/GitRelease.rst.txt)

* * *

# GitRelease [¶](https://pygithub.readthedocs.io/en/stable/github_objects/GitRelease.html\#gitrelease "Permalink to this headline")

_class_ `github.GitRelease.` `GitRelease` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/GitRelease.html#github.GitRelease.GitRelease "Permalink to this definition")

This class represents GitReleases.

The reference can be found here
[https://docs.github.com/en/rest/reference/repos#releases](https://docs.github.com/en/rest/reference/repos#releases)

The OpenAPI schema can be found at
\- /components/schemas/basic-error
\- /components/schemas/release

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


`delete_release`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/GitRelease.html#github.GitRelease.GitRelease.delete_release "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/releases/{release\_id}](https://docs.github.com/en/rest/releases/releases?apiVersion=2022-11-28#delete-a-release)

`update_release`( _name: str_, _message: str_, _draft: bool = False_, _prerelease: bool = False_, _tag\_name: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _target\_commitish: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _make\_latest: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _discussion\_category\_name: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_) → github.GitRelease.GitRelease [¶](https://pygithub.readthedocs.io/en/stable/github_objects/GitRelease.html#github.GitRelease.GitRelease.update_release "Permalink to this definition")Calls

[PATCH /repos/{owner}/{repo}/releases/{release\_id}](https://docs.github.com/en/rest/releases/releases?apiVersion=2022-11-28#update-a-release)

`upload_asset`( _path: str_, _label: str = ''_, _content\_type: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _name: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_) → github.GitReleaseAsset.GitReleaseAsset [¶](https://pygithub.readthedocs.io/en/stable/github_objects/GitRelease.html#github.GitRelease.GitRelease.upload_asset "Permalink to this definition")Calls

[POST https://<upload\_url>/repos/{owner}/{repo}/releases/{release\_id}/assets](https://docs.github.com/en/rest/releases/assets?apiVersion=2022-11-28#upload-a-release-assett)

`upload_asset_from_memory`( _file\_like: BinaryIO_, _file\_size: int_, _name: str_, _content\_type: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _label: str = ''_) → github.GitReleaseAsset.GitReleaseAsset [¶](https://pygithub.readthedocs.io/en/stable/github_objects/GitRelease.html#github.GitRelease.GitRelease.upload_asset_from_memory "Permalink to this definition")

Uploads an asset.

Unlike `upload_asset()` this method allows you to pass in a file-like object to upload.
Note that this method is more strict and requires you to specify the `name`, since there's no file name to infer these from.
:calls: [POST https://<upload\_url>/repos/{owner}/{repo}/releases/{release\_id}/assets](https://docs.github.com/en/rest/reference/repos#upload-a-release-asset)
:param file\_like: binary file-like object, such as those returned by `open("file_name", "rb")`. At the very minimum, this object must implement `read()`.
:param file\_size: int, size in bytes of `file_like`

`get_assets`() → github.PaginatedList.PaginatedList\[github.GitReleaseAsset.GitReleaseAsset\]\[github.GitReleaseAsset.GitReleaseAsset\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/GitRelease.html#github.GitRelease.GitRelease.get_assets "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/releases/{release\_id}/assets](https://docs.github.com/en/rest/releases/assets?apiVersion=2022-11-28#get-a-release-asset)