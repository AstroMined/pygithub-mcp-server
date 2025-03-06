- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- Notification
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/Notification.rst.txt)

* * *

# Notification [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Notification.html\#notification "Permalink to this headline")

_class_ `github.Notification.` `Notification` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Notification.html#github.Notification.Notification "Permalink to this definition")

This class represents Notifications.

The reference can be found here
[https://docs.github.com/en/rest/reference/activity#notifications](https://docs.github.com/en/rest/reference/activity#notifications)

The OpenAPI schema can be found at
\- /components/schemas/thread

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


`mark_as_read`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Notification.html#github.Notification.Notification.mark_as_read "Permalink to this definition")Calls

[PATCH /notifications/threads/{id}](https://docs.github.com/en/rest/reference/activity#notifications)

`mark_as_done`() → None [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Notification.html#github.Notification.Notification.mark_as_done "Permalink to this definition")Calls

[DELETE /notifications/threads/{id}](https://docs.github.com/en/rest/reference/activity#notifications)