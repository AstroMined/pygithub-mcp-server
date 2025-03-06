- »
- Introduction
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/introduction.rst.txt)

* * *

# Introduction [¶](https://pygithub.readthedocs.io/en/stable/introduction.html\#introduction "Permalink to this headline")

PyGithub is a Python library to use the [Github API v3](http://developer.github.com/v3).
With it, you can manage your [Github](http://github.com/) resources (repositories, user profiles, organizations, etc.) from Python scripts.

Should you have any question, any remark, or if you find a bug,
or if there is something you can do with the API but not with PyGithub,
please [open an issue](https://github.com/PyGithub/PyGithub/issues).

## (Very short) tutorial [¶](https://pygithub.readthedocs.io/en/stable/introduction.html\#very-short-tutorial "Permalink to this headline")

First create a Github instance:

```
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

```
for repo in g.get_user().get_repos():
    print(repo.name)
    repo.edit(has_wiki=False)
    # to see all the available attributes and methods
    print(dir(repo))

```

To close connections after use:

```
g.close()

```

## Download and install [¶](https://pygithub.readthedocs.io/en/stable/introduction.html\#download-and-install "Permalink to this headline")

This package is in the [Python Package Index](http://pypi.python.org/pypi/PyGithub), so `pip install PyGithub` should
be enough. You can also clone it on [Github](http://github.com/PyGithub/PyGithub).

## Licensing [¶](https://pygithub.readthedocs.io/en/stable/introduction.html\#licensing "Permalink to this headline")

PyGithub is distributed under the GNU Lesser General Public Licence.
See files COPYING and COPYING.LESSER, as requested by [GNU](http://www.gnu.org/licenses/gpl-howto.html).

## What next? [¶](https://pygithub.readthedocs.io/en/stable/introduction.html\#what-next "Permalink to this headline")

You need to use a Github API and wonder which class implements it? [Reference of APIs](https://pygithub.readthedocs.io/en/latest/apis.html).

You want all the details about PyGithub classes? [Reference of Classes](https://pygithub.readthedocs.io/en/latest/github_objects.html).

## Projects using PyGithub [¶](https://pygithub.readthedocs.io/en/stable/introduction.html\#projects-using-pygithub "Permalink to this headline")

( [Open an issue](https://github.com/PyGithub/PyGithub/issues) if you want to be listed here, I'll be glad to add your project)

- [Github-iCalendar](http://danielpocock.com/github-issues-as-an-icalendar-feed) returns all of your Github issues and pull requests as a list of tasks / VTODO items in iCalendar format.

- [DevAssistant](http://devassistant.org/)

- [Upverter](https://upverter.com/) is a web-based schematic capture and PCB layout tool for people who design electronics. Designers can attach a Github project to an Upverter project.

- [Notifico](http://n.tkte.ch/) receives messages (such as commits and issues) from services and scripts and delivers them to IRC channels. It can import/sync from Github.

- [Tratihubis](http://pypi.python.org/pypi/tratihubis/) converts Trac tickets to Github issues

- [https://github.com/fga-gpp-mds/2018.1-Cardinals](https://github.com/fga-gpp-mds/2018.1-Cardinals) \- website that shows metrics for any public repository (issues, commits, pull requests etc)

- [https://github.com/CMB/cligh](https://github.com/CMB/cligh)

- [https://github.com/natduca/quickopen](https://github.com/natduca/quickopen) uses PyGithub to automatically create issues

- [https://gist.github.com/3433798](https://gist.github.com/3433798)

- [https://github.com/zsiciarz/aquila-dsp.org](https://github.com/zsiciarz/aquila-dsp.org)

- [https://github.com/robcowie/virtualenvwrapper.github](https://github.com/robcowie/virtualenvwrapper.github)

- [https://github.com/kokosing/git-gifi](https://github.com/kokosing/git-gifi) \- Git and github enhancements to git.

- [https://github.com/csurfer/gitsuggest](https://github.com/csurfer/gitsuggest) \- A tool to suggest github repositories based on the repositories you have shown interest in

- [https://github.com/gomesfernanda/some-github-metrics](https://github.com/gomesfernanda/some-github-metrics) \- Python functions for relevant metrics on GitHub repositories

- [https://github.com/SOM-Research/Gitana](https://github.com/SOM-Research/Gitana) \- a SQL-based Project Activity Inspector

- [https://github.com/plus3it/satsuki](https://github.com/plus3it/satsuki) \- Automate GitHub releases and uploading binary release assets

- [check-in](https://github.com/webknjaz/check-in) — Python CLI distribution that allows user to use GitHub Checks API as a bot.

- [https://github.com/hasii2011/gittodoistclone](https://github.com/hasii2011/gittodoistclone) \- Convert GitHub issues to Todoist tasks


## They talk about PyGithub [¶](https://pygithub.readthedocs.io/en/stable/introduction.html\#they-talk-about-pygithub "Permalink to this headline")

- [http://stackoverflow.com/questions/10625190/most-suitable-python-library-for-github-api-v3](http://stackoverflow.com/questions/10625190/most-suitable-python-library-for-github-api-v3)

- [http://stackoverflow.com/questions/12379637/django-social-auth-github-authentication](http://stackoverflow.com/questions/12379637/django-social-auth-github-authentication)

- [http://www.freebsd.org/cgi/cvsweb.cgi/ports/devel/py-pygithub/](http://www.freebsd.org/cgi/cvsweb.cgi/ports/devel/py-pygithub/)

- [https://bugzilla.redhat.com/show\_bug.cgi?id=910565](https://bugzilla.redhat.com/show_bug.cgi?id=910565)