- »
- [Reference](https://pygithub.readthedocs.io/en/stable/reference.html) »
- [Github objects](https://pygithub.readthedocs.io/en/stable/github_objects.html) »
- RateLimit
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/github_objects/RateLimit.rst.txt)

* * *

# RateLimit [¶](https://pygithub.readthedocs.io/en/stable/github_objects/RateLimit.html\#ratelimit "Permalink to this headline")

_class_ `github.RateLimit.` `RateLimit` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/RateLimit.html#github.RateLimit.RateLimit "Permalink to this definition")

This class represents RateLimits.

The reference can be found here
[https://docs.github.com/en/rest/reference/rate-limit](https://docs.github.com/en/rest/reference/rate-limit)

The OpenAPI schema can be found at
\- /components/schemas/rate-limit-overview/properties/resources

_property_ `actions_runner_registration` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/RateLimit.html#github.RateLimit.RateLimit.actions_runner_registration "Permalink to this definition")

Rate limit for registering self-hosted runners in GitHub Actions.

_property_ `code_scanning_upload` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/RateLimit.html#github.RateLimit.RateLimit.code_scanning_upload "Permalink to this definition")

Rate limit for uploading SARIF results to code scanning.

_property_ `code_search` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/RateLimit.html#github.RateLimit.RateLimit.code_search "Permalink to this definition")

Rate limit for the REST API for searching code.

_property_ `core` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/RateLimit.html#github.RateLimit.RateLimit.core "Permalink to this definition")

Rate limit for the non-search-related API.

_property_ `dependency_snapshots` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/RateLimit.html#github.RateLimit.RateLimit.dependency_snapshots "Permalink to this definition")

Rate limit for submitting snapshots to the dependency graph.

_property_ `graphql` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/RateLimit.html#github.RateLimit.RateLimit.graphql "Permalink to this definition")

(Experimental) Rate limit for GraphQL API, use with caution.

_property_ `integration_manifest` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/RateLimit.html#github.RateLimit.RateLimit.integration_manifest "Permalink to this definition")

Rate limit for POST /app-manifests/{code}/conversions operation.

_property_ `search` [¶](https://pygithub.readthedocs.io/en/stable/github_objects/RateLimit.html#github.RateLimit.RateLimit.search "Permalink to this definition")

Rate limit for the Search API.