- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- CommitComment
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/CommitComment.rst.txt)

* * *

# CommitComment [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CommitComment.html\#commitcomment "Permalink to this headline")

_class_ `github.CommitComment.` `CommitComment` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CommitComment.html#github.CommitComment.CommitComment "Permalink to this definition")

This class represents CommitComments.

The reference can be found here
[https://docs.github.com/en/rest/reference/repos#comments](https://docs.github.com/en/rest/reference/repos#comments)

The OpenAPI schema can be found at
\- /components/schemas/commit-comment

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


`delete`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CommitComment.html#github.CommitComment.CommitComment.delete "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/comments/{id}](https://docs.github.com/en/rest/reference/repos#comments)

Return type

None

`edit`( _body: str_) → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CommitComment.html#github.CommitComment.CommitComment.edit "Permalink to this definition")Calls

[PATCH /repos/{owner}/{repo}/comments/{id}](https://docs.github.com/en/rest/reference/repos#comments)

`get_reactions`() → PaginatedList\[Reaction\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CommitComment.html#github.CommitComment.CommitComment.get_reactions "Permalink to this definition")Calls

[GET /repos/{owner}/{repo}/comments/{id}/reactions](https://docs.github.com/en/rest/reference/reactions#list-reactions-for-a-commit-comment)

Returns

class

[`github.PaginatedList.PaginatedList`](https://pygithub.readthedocs.io/en/stable/utilities.html#github.PaginatedList.PaginatedList "github.PaginatedList.PaginatedList") of [`github.Reaction.Reaction`](https://pygithub.readthedocs.io/en/stable/github_objects/Reaction.html#github.Reaction.Reaction "github.Reaction.Reaction")

`create_reaction`( _reaction\_type: str_) → Reaction [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CommitComment.html#github.CommitComment.CommitComment.create_reaction "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/comments/{id}/reactions](https://docs.github.com/en/rest/reference/reactions#create-reaction-for-a-commit-comment)

`delete_reaction`( _reaction\_id: int_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CommitComment.html#github.CommitComment.CommitComment.delete_reaction "Permalink to this definition")Calls

[DELETE /repos/{owner}/{repo}/comments/{comment\_id}/reactions/{reaction\_id}](https://docs.github.com/en/rest/reference/reactions#delete-a-commit-comment-reaction)

Parameters

**reaction\_id** – integer

Return type

bool