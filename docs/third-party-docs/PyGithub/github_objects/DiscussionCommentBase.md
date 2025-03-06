- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- DiscussionCommentBase
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/DiscussionCommentBase.rst.txt)

* * *

# DiscussionCommentBase [¶](https://pygithub.readthedocs.io/en/stable/github_objects/DiscussionCommentBase.html\#discussioncommentbase "Permalink to this headline")

_class_ `github.DiscussionCommentBase.` `DiscussionCommentBase` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/DiscussionCommentBase.html#github.DiscussionCommentBase.DiscussionCommentBase "Permalink to this definition")

This class represents a the shared attributes between RepositoryDiscussionComment and TeamDiscussionComment
[https://docs.github.com/en/graphql/reference/objects#discussioncomment](https://docs.github.com/en/graphql/reference/objects#discussioncomment) [https://docs.github.com/de/rest/teams/discussion-comments](https://docs.github.com/de/rest/teams/discussion-comments)

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