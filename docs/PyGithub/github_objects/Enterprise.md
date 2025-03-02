- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- Enterprise
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/Enterprise.rst.txt)

* * *

# Enterprise [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Enterprise.html\#enterprise "Permalink to this headline")

_class_ `github.Enterprise.` `Enterprise` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Enterprise.html#github.Enterprise.Enterprise "Permalink to this definition")

This class represents Enterprises.

Such objects do not exist in the Github API, so this class merely collects all endpoints the start with
/enterprises/{enterprise}/. See methods below for specific endpoints and docs.
[https://docs.github.com/en/enterprise-cloud@latest/rest/enterprise-admin?apiVersion=2022-11-28](https://docs.github.com/en/enterprise-cloud@latest/rest/enterprise-admin?apiVersion=2022-11-28)

`get_consumed_licenses`() → github.EnterpriseConsumedLicenses.EnterpriseConsumedLicenses [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Enterprise.html#github.Enterprise.Enterprise.get_consumed_licenses "Permalink to this definition")Calls

[GET /enterprises/{enterprise}/consumed-licenses](https://docs.github.com/en/enterprise-cloud@latest/rest/enterprise-admin/license#list-enterprise-consumed-licenses)