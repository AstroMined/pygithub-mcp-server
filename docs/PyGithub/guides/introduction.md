# Introduction

PyGithub is a Python library to use the [Github API v3](http://developer.github.com/v3).
With it, you can manage your [Github](http://github.com/) resources (repositories, user profiles, organizations, etc.) from Python scripts.

Should you have any question, any remark, or if you find a bug,
or if there is something you can do with the API but not with PyGithub,
please [open an issue](https://github.com/PyGithub/PyGithub/issues).

## (Very short) tutorial

First create a Github instance:

```python
from github import Github

# Authentication is defined via github.Auth
from github import Auth

# using an access token
auth = Auth.Token("access_token")

# Public Web Github
g = Github(auth=auth)

# Github Enterprise with custom hostname
g = Github(auth=auth, base_url="https://{hostname}/api/v3")
```

Then play with your Github objects:

```python
for repo in g.get_user().get_repos():
    print(repo.name)
    repo.edit(has_wiki=False)
    # to see all the available attributes and methods
    print(dir(repo))
```

To close connections after use:

```python
g.close()
```

## Download and install

This package is in the [Python Package Index](http://pypi.python.org/pypi/PyGithub), so `pip install PyGithub` should
be enough. You can also clone it on [Github](http://github.com/PyGithub/PyGithub).

## Licensing

PyGithub is distributed under the GNU Lesser General Public Licence.
See files COPYING and COPYING.LESSER, as requested by [GNU](http://www.gnu.org/licenses/gpl-howto.html).

## What next?

You need to use a Github API and wonder which class implements it? [Reference of APIs](https://pygithub.readthedocs.io/en/latest/apis.html).

You want all the details about PyGithub classes? [Reference of Classes](https://pygithub.readthedocs.io/en/latest/github_objects.html).

## Projects using PyGithub

- [Github-iCalendar](http://danielpocock.com/github-issues-as-an-icalendar-feed) - Returns all of your Github issues and pull requests as a list of tasks / VTODO items in iCalendar format
- [DevAssistant](http://devassistant.org/)
- [Upverter](https://upverter.com/) - Web-based schematic capture and PCB layout tool
- [Notifico](http://n.tkte.ch/) - Receives messages from services and delivers them to IRC channels
- [Tratihubis](http://pypi.python.org/pypi/tratihubis/) - Converts Trac tickets to Github issues
- [Cardinals](https://github.com/fga-gpp-mds/2018.1-Cardinals) - Website that shows metrics for any public repository
- [Cligh](https://github.com/CMB/cligh)
- [Quickopen](https://github.com/natduca/quickopen)
- [Git-gifi](https://github.com/kokosing/git-gifi) - Git and github enhancements
- [Gitsuggest](https://github.com/csurfer/gitsuggest) - Tool to suggest github repositories
- [GitHub Metrics](https://github.com/gomesfernanda/some-github-metrics) - Python functions for relevant metrics
- [Gitana](https://github.com/SOM-Research/Gitana) - SQL-based Project Activity Inspector
- [Satsuki](https://github.com/plus3it/satsuki) - Automate GitHub releases
- [Check-in](https://github.com/webknjaz/check-in) - CLI for GitHub Checks API
- [GitTodoistClone](https://github.com/hasii2011/gittodoistclone) - Convert GitHub issues to Todoist tasks
