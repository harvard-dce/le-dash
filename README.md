# le-dash
Django Project for DCE Learning Engineering Dashboard Apps

[![Build Status](https://travis-ci.org/harvard-dce/le-dash.svg?branch=project-setup)](https://travis-ci.org/harvard-dce/le-dash)
[![Code Health](https://landscape.io/github/harvard-dce/le-dash/jluker-es-query/landscape.svg?style=flat)](https://landscape.io/github/harvard-dce/le-dash/jluker-es-query)

## Getting started

1. clone the repo
1. `pip install -r requirements/dev.txt`
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
