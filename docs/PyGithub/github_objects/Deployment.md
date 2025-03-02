- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- Deployment
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/Deployment.rst.txt)

* * *

# Deployment [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Deployment.html\#deployment "Permalink to this headline")

_class_ `github.Deployment.` `Deployment` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Deployment.html#github.Deployment.Deployment "Permalink to this definition")

This class represents Deployments.

The reference can be found here
[https://docs.github.com/en/rest/reference/repos#deployments](https://docs.github.com/en/rest/reference/repos#deployments)

The OpenAPI schema can be found at
\- /components/schemas/deployment
\- /components/schemas/deployment-simple

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


`get_statuses`() → github.PaginatedList.PaginatedList\[github.DeploymentStatus.DeploymentStatus\]\[github.DeploymentStatus.DeploymentStatus\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Deployment.html#github.Deployment.Deployment.get_statuses "Permalink to this definition")Calls

[GET /repos/{owner}/deployments/{deployment\_id}/statuses](https://docs.github.com/en/rest/reference/repos#list-deployments)

`get_status`( _id\_: int_) → github.DeploymentStatus.DeploymentStatus [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Deployment.html#github.Deployment.Deployment.get_status "Permalink to this definition")Calls

[GET /repos/{owner}/deployments/{deployment\_id}/statuses/{status\_id}](https://docs.github.com/en/rest/reference/repos#get-a-deployment)

`create_status`( _state: str_, _target\_url: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _description: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _environment: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _environment\_url: Union\[str_, _github.GithubObject.\_NotSetType\] = NotSet_, _auto\_inactive: Union\[bool_, _github.GithubObject.\_NotSetType\] = NotSet_) → github.DeploymentStatus.DeploymentStatus [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Deployment.html#github.Deployment.Deployment.create_status "Permalink to this definition")Calls

[POST /repos/{owner}/{repo}/deployments/{deployment\_id}/statuses](https://docs.github.com/en/rest/reference/repos#create-a-deployment-status)