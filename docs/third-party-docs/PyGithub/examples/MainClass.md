- »
- [Examples](https://pygithub.readthedocs.io/en/stable/examples.html) »
- Main Class
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/examples/MainClass.rst.txt)

* * *

# Main Class [¶](https://pygithub.readthedocs.io/en/stable/examples/MainClass.html\#main-class "Permalink to this headline")

This is the main class.

## Get current user [¶](https://pygithub.readthedocs.io/en/stable/examples/MainClass.html\#get-current-user "Permalink to this headline")

```
>>> user = g.get_user()
>>> user.login
u'sfdye'

```

## Get user by name [¶](https://pygithub.readthedocs.io/en/stable/examples/MainClass.html\#get-user-by-name "Permalink to this headline")

```
>>> user = g.get_user("sfdye")
>>> user.name
u'Wan Liuyang'

```

## Get repository by name [¶](https://pygithub.readthedocs.io/en/stable/examples/MainClass.html\#get-repository-by-name "Permalink to this headline")

```
>>> repo = g.get_repo("PyGithub/PyGithub")
>>> repo.name
u'PyGithub'

```

## Get organization by name [¶](https://pygithub.readthedocs.io/en/stable/examples/MainClass.html\#get-organization-by-name "Permalink to this headline")

```
>>> org = g.get_organization("PyGithub")
>>> org.login
u'PyGithub'

```

## Get enterprise consumed licenses by name [¶](https://pygithub.readthedocs.io/en/stable/examples/MainClass.html\#get-enterprise-consumed-licenses-by-name "Permalink to this headline")

```
>>> enterprise = g.get_enterprise_consumed_licenses("PyGithub")
>>> enterprise_consumed_licenses = enterprise.get_enterprise_consumed_licenses()
>>> enterprise_consumed_licenses.total_seats_consumed
5000

```

## Search repositories by language [¶](https://pygithub.readthedocs.io/en/stable/examples/MainClass.html\#search-repositories-by-language "Permalink to this headline")

```
>>> repositories = g.search_repositories(query='language:python')
>>> for repo in repositories:
...    print(repo)
...
Repository(full_name="vinta/awesome-python")
Repository(full_name="donnemartin/system-design-primer")
Repository(full_name="toddmotto/public-apis")
Repository(full_name="rg3/youtube-dl")
Repository(full_name="tensorflow/models")
Repository(full_name="django/django")

```

## Search repositories based on number of issues with good-first-issue [¶](https://pygithub.readthedocs.io/en/stable/examples/MainClass.html\#search-repositories-based-on-number-of-issues-with-good-first-issue "Permalink to this headline")

```
>>> repositories = g.search_repositories(query='good-first-issues:>3')
>>> for repo in repositories:
...    print(repo)
...
Repository(full_name="vuejs/vue")
Repository(full_name="facebook/react")
Repository(full_name="facebook/react-native")
Repository(full_name="electron/electron")
Repository(full_name="Microsoft/vscode")

```