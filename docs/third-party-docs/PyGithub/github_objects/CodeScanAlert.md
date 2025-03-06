- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- CodeScanAlert
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/CodeScanAlert.rst.txt)

* * *

# CodeScanAlert [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CodeScanAlert.html\#codescanalert "Permalink to this headline")

_class_ `github.CodeScanAlert.` `CodeScanAlert` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CodeScanAlert.html#github.CodeScanAlert.CodeScanAlert "Permalink to this definition")

This class represents alerts from code scanning.

The reference can be found here
[https://docs.github.com/en/rest/reference/code-scanning](https://docs.github.com/en/rest/reference/code-scanning).

`get_instances`() → github.PaginatedList.PaginatedList\[github.CodeScanAlertInstance.CodeScanAlertInstance\]\[github.CodeScanAlertInstance.CodeScanAlertInstance\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/CodeScanAlert.html#github.CodeScanAlert.CodeScanAlert.get_instances "Permalink to this definition")

Get instances.

Calls

GET on the URL for instances as provided by Github.