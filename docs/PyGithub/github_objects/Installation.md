- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- Installation
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/Installation.rst.txt)

* * *

# Installation [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Installation.html\#installation "Permalink to this headline")

_class_ `github.Installation.` `Installation` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Installation.html#github.Installation.Installation "Permalink to this definition")

This class represents Installations.

The reference can be found here
[https://docs.github.com/en/rest/reference/apps#installations](https://docs.github.com/en/rest/reference/apps#installations)

The OpenAPI schema can be found at
\- /components/schemas/installation

_property_ `requester` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Installation.html#github.Installation.Installation.requester "Permalink to this definition")

Return my Requester object.

For example, to make requests to API endpoints not yet supported by PyGitHub.

`get_repos`() → github.PaginatedList.PaginatedList\[github.Repository.Repository\]\[github.Repository.Repository\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Installation.html#github.Installation.Installation.get_repos "Permalink to this definition")Calls

[GET /installation/repositories](https://docs.github.com/en/rest/reference/integrations/installations#list-repositories)