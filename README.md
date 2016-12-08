# le-dash
Django Project for DCE Learning Engineering Dashboard Apps

[![Build Status](https://travis-ci.org/harvard-dce/le-dash.svg?branch=project-setup)](https://travis-ci.org/harvard-dce/le-dash)
[![Code Health](https://landscape.io/github/harvard-dce/le-dash/jluker-es-query/landscape.svg?style=flat)](https://landscape.io/github/harvard-dce/le-dash/jluker-es-query)

## Getting started

1. clone the repo
1. `pip install -r requirements/dev.txt`
1. install and start redis
    eg:  sudo apt-get install redis-server
1. `cp example.env .env` and update:
    1. set `SECRET_KEY` to anything
    1. set `DJANGO_SETTINGS_MODULE` to `le_dash.settings.dev`
    1. set `ES_HOST` to the host:port combo of your elasticsearch instance
    1. set `BANNER_BASE_URL` to the banner data endpoint url
1. run the tests: `./manage.py test` or `tox`
1. create an empty local settings module: `touch le_dash/settings/local.py`
1. setup the db: `./manage.py migrate`
1. run the dev server: `./manage.py runserver` or `gunicorn le_dash.wsgi`
1. run `./manage.py show_urls` to see a list of the available url patterns

## Development

The current branch for deployment is `master`. We are not yet using deployment
tags, but will most likely at some point when we get to an actual v0.1.0 release.

For the time being, simple changes to the README or dev/testing setup can be 
pushed directly to master at the developer's discretion. All other development
changes, features, etc., should be done in a branch, and when completed pushed
github and a pull request submitted so that other developers are aware of the 
changes and can review/approve.

Basic workflow should follow the github flow model,
https://guides.github.com/introduction/flow/, with some additional steps that
relate to our testing and travis-ci setup. For keeping development branches
in sync with master we use the *rebasing* strategy as opposed to *merging*. This
is explained very well at https://www.atlassian.com/git/tutorials/merging-vs-rebasing,
which should be required reading.

Do your work in a local development branch. Push that branch to github whenever
you want. You can push each change incrementally, or use `git amend` to continually
update a single commit. If using `git amend` you must include the 
`--force-with-lease` options when pushing. Use `git rebase -i` and the `squash` or
`fixup` flags to combine related commits.

Example:

1. Get your local master up-to-date: `git checkout master; git pull origin master`
1. Create your dev branch: `git checkout -b my-dev-branch`
1. Do some work and `git commit` the changes
1. Make sure your dev branch includes any upstream changes in master that may 
   have occurred during the previous step
    1. `git checkout master`
    1. `git pull origin master`
    1. `git checkout my-dev-branch`
    1. `git rebase master`
    1. cleanup any conflicts. consult with other developers if this gets hairy.
1. Push the branch to github: `git push origin my-dev-branch`
1. If you're ready for the changes to be reviewed create a pull request on github
1. Repeat the previous few steps if more development is required.
1. Interactively rebase your own commits to consolidate them into one or more
   logical changes: `git rebase -i HEAD~n` where `n` is the number of commits
   back in the history that you want to collapse. The point of this is to get rid 
   of any *"fixing typo"*  or *"oops whitespace!"* commits.
1. Continue pushing the branch to github as appropriate. Use `git push --force-with-lease`
   for cases where you've rebased locally and modified the commit history of
   your dev branch. There's no need to create new branches or pull requests. Github
   will automatically update any existing pull request that originates from that branch.
   
   
## Testing

This project uses `pytest`, `flake8`, `tox`, and Travis-CI for testing, syntax
checking, and continuous integration. You should make a habit of running `tox` 
and dealing with any tests or `flake8` style/syntax errors prior to pushing a
dev branch to github. You should **definitely** do this before creating a pull
request.

Travis-CI will automatically build and test *any* branch that gets pushed to, so
expect to see a failure email if you broke something, even if it's just a branch
you're still working on.

On occasion a new python package requirement might be added to `requirements.txt`.
When this happens, `tox` might complain about missing dependencies. Add the `-r`
flag in this case, e.g., `tox -r`, to force tox to recreate it's virtualenvs.o

If you're using Pycharm, it allows you to easily create run configurations for all
of these tools. Go to "Run" -> "Edit Configurations...", click the "+" sign in 
the top-left corner of the dialog and choose "Tox", or "Python tests" -> "py.test"
to create a new configuration. For example, I recommend you create a `tox` 
configuration that exercises only the `flake8` environment. That way you can easily
click from the `flake8` warning to the precise line of code it's complaining about.

### Cacheing

The caching layer uses redis and  django-redis-cache to cache responses from banner and elasticsearch. 

Defaul redis host:port is the standard `localhost:6379`. To use a different host:port set
`REDIS_LOCATION` in your `.env`

To disable cacheing set `DISABLE_CACHE=1` in your `.env`

To Test that redis is running, type in the shell and wait for reply:

    $ redis-cli ping
    PONG

