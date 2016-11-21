# le-dash
Django Project for DCE Learning Engineering Dashboard Apps

[![Build Status](https://travis-ci.org/harvard-dce/le-dash.svg?branch=project-setup)](https://travis-ci.org/harvard-dce/le-dash)

## Getting started

1. clone the repo
1. `pip install -r requirements/dev.txt`
1. `cp example.env .env` and update:
    1. set `SECRET_KEY` to anything
    1. set `DJANGO_SETTINGS_MODULE` to `le_dash.settings.dev`
1. run the tests: `./manage.py test` or `tox`
1. create an empty local settings module: `touch le_dash/settings/local.py`
1. setup the db: `./manage.py migrate`
1. run the dev server: `./manage.py runserver` or `gunicorn le_dash.wsgi`
