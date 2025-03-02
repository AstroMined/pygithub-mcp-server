- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- EnterpriseConsumedLicenses
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/EnterpriseConsumedLicenses.rst.txt)

* * *

# EnterpriseConsumedLicenses [¶](https://pygithub.readthedocs.io/en/stable/github_objects/EnterpriseConsumedLicenses.html\#enterpriseconsumedlicenses "Permalink to this headline")

_class_ `github.EnterpriseConsumedLicenses.` `EnterpriseConsumedLicenses` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/EnterpriseConsumedLicenses.html#github.EnterpriseConsumedLicenses.EnterpriseConsumedLicenses "Permalink to this definition")

This class represents license consumed by enterprises.

The reference can be found here
[https://docs.github.com/en/enterprise-cloud@latest/rest/enterprise-admin/license#list-enterprise-consumed-licenses](https://docs.github.com/en/enterprise-cloud@latest/rest/enterprise-admin/license#list-enterprise-consumed-licenses)

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


`get_users`() → github.PaginatedList.PaginatedList\[github.NamedEnterpriseUser.NamedEnterpriseUser\]\[github.NamedEnterpriseUser.NamedEnterpriseUser\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/EnterpriseConsumedLicenses.html#github.EnterpriseConsumedLicenses.EnterpriseConsumedLicenses.get_users "Permalink to this definition")Calls

[GET /enterprises/{enterprise}/consumed-licenses](https://docs.github.com/en/enterprise-cloud@latest/rest/enterprise-admin/license#list-enterprise-consumed-licenses)