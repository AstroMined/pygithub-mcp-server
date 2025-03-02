- »
- [Examples](https://pygithub.readthedocs.io/en/stable/examples.html) »
- Milestone
- [View page source](https://pygithub.readthedocs.io/en/stable/_sources/examples/Milestone.rst.txt)

* * *

# Milestone [¶](https://pygithub.readthedocs.io/en/stable/examples/Milestone.html\#milestone "Permalink to this headline")

## Get Milestone list [¶](https://pygithub.readthedocs.io/en/stable/examples/Milestone.html\#get-milestone-list "Permalink to this headline")

```
>>> repo = g.get_repo('PyGithub/PyGithub')
>>> open_milestones = repo.get_milestones(state='open')
>>> for milestone in open_milestones:
...    print(milestone)
...
Milestone(number=1)
Milestone(number=2)

```

## Get Milestone [¶](https://pygithub.readthedocs.io/en/stable/examples/Milestone.html\#get-milestone "Permalink to this headline")

```
>>> repo = g.get_repo('PyGithub/PyGithub')
>>> repo.get_milestone(number=1)
Milestone(number=1)

```

## Create Milestone [¶](https://pygithub.readthedocs.io/en/stable/examples/Milestone.html\#create-milestone "Permalink to this headline")

```
>>> repo = g.get_repo('PyGithub/PyGithub')
>>> repo.create_milestone(title='New Milestone')
Milestone(number=1)

```

## Create Milestone with State and Description [¶](https://pygithub.readthedocs.io/en/stable/examples/Milestone.html\#create-milestone-with-state-and-description "Permalink to this headline")

```
>>> repo = g.get_repo('PyGithub/PyGithub')
>>> repo.create_milestone(title='New Milestone', state='open', description='Milestone description')
Milestone(number=1)

```