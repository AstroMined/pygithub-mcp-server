- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- Environment
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/Environment.rst.txt)

* * *

# Environment [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Environment.html\#environment "Permalink to this headline")

_class_ `github.Environment.` `Environment` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Environment.html#github.Environment.Environment "Permalink to this definition")

This class represents Environment.

The reference can be found here
[https://docs.github.com/en/rest/reference/deployments#environments](https://docs.github.com/en/rest/reference/deployments#environments)

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


_property_ `environments_url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Environment.html#github.Environment.Environment.environments_url "Permalink to this definition")Type

string

_property_ `url` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Environment.html#github.Environment.Environment.url "Permalink to this definition")Type

string

`get_public_key`() → github.PublicKey.PublicKey [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Environment.html#github.Environment.Environment.get_public_key "Permalink to this definition")Calls

[GET /repositories/{repository\_id}/environments/{environment\_name}/secrets/public-key](https://docs.github.com/en/rest/reference#get-a-repository-public-key)

Return type

`PublicKey`

`create_secret`( _secret\_name: str_, _unencrypted\_value: str_) → github.Secret.Secret [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Environment.html#github.Environment.Environment.create_secret "Permalink to this definition")Calls

[PUT /repositories/{repository\_id}/environments/{environment\_name}/secrets/{secret\_name}](https://docs.github.com/en/rest/secrets#get-a-repository-secret)

`get_secrets`() → github.PaginatedList.PaginatedList\[github.Secret.Secret\]\[github.Secret.Secret\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Environment.html#github.Environment.Environment.get_secrets "Permalink to this definition")

Gets all repository secrets.

`get_secret`( _secret\_name: str_) → github.Secret.Secret [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Environment.html#github.Environment.Environment.get_secret "Permalink to this definition")Calls

'GET /repositories/{repository\_id}/environments/{environment\_name}/secrets/{secret\_name} < [https://docs.github.com/en/rest/secrets#get-an-organization-secret](https://docs.github.com/en/rest/secrets#get-an-organization-secret) >\`\_

`create_variable`( _variable\_name: str_, _value: str_) → github.Variable.Variable [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Environment.html#github.Environment.Environment.create_variable "Permalink to this definition")Calls

[POST /repositories/{repository\_id}/environments/{environment\_name}/variables/{variable\_name}](https://docs.github.com/en/rest/variables#create-a-repository-variable)

`get_variables`() → github.PaginatedList.PaginatedList\[github.Variable.Variable\]\[github.Variable.Variable\] [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Environment.html#github.Environment.Environment.get_variables "Permalink to this definition")

Gets all repository variables :rtype: `PaginatedList` of `Variable`

`get_variable`( _variable\_name: str_) → github.Variable.Variable [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Environment.html#github.Environment.Environment.get_variable "Permalink to this definition")Calls

'GET /orgs/{org}/variables/{variable\_name} < [https://docs.github.com/en/rest/variables#get-an-organization-variable](https://docs.github.com/en/rest/variables#get-an-organization-variable) >\`\_

Parameters

**variable\_name** – string

Return type

[Variable](https://pygithub.readthedocs.io/en/stable/github_objects/Variable.html#github.Variable.Variable "github.Variable.Variable")

`delete_secret`( _secret\_name: str_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Environment.html#github.Environment.Environment.delete_secret "Permalink to this definition")Calls

[DELETE /repositories/{repository\_id}/environments/{environment\_name}/secrets/{secret\_name}](https://docs.github.com/en/rest/reference#delete-a-repository-secret)

Parameters

**secret\_name** – string

Return type

bool

`delete_variable`( _variable\_name: str_) → bool [¶](https://pygithub.readthedocs.io/en/stable/github_objects/Environment.html#github.Environment.Environment.delete_variable "Permalink to this definition")Calls

[DELETE /repositories/{repository\_id}/environments/{environment\_name}/variables/{variable\_name}](https://docs.github.com/en/rest/reference#delete-a-repository-variable)

Parameters

**variable\_name** – string

Return type

bool