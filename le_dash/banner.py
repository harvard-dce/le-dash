import json
import requests
from django.conf import settings
from collections import namedtuple

import sys
major, minor, micro, releaselevel, serial = sys.version_info
if major == 2:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin

StudentInfo = namedtuple(
    'StudentInfo',
    ['huid', 'first_name', 'mi', 'last_name']
)


def get_student_list(series_id, registered=True):
    url = urljoin(settings.BANNER_BASE_URL, '__get_classlist.php')
    params = {
        'fmt': "json",
        'term': series_id[:6],
        'crn': series_id[6:]
    }
    resp = requests.get(url, params)
    students = json.loads(resp.content)
    try:
        for node in students["students"]["student"]:
            if registered and "Registered" != node['status']:
                continue
            s = StudentInfo._make(node[f] for f in StudentInfo._fields)
            yield s
    except KeyError:  # No results
        pass


def get_student_list_raw(series_id, registered=True):
    url = urljoin(settings.BANNER_BASE_URL, '__get_classlist.php')
    params = {
        'fmt': "json",
        'term': series_id[:6],
        'crn': series_id[6:]
    }
    resp = requests.get(url, params)
    students = json.loads(resp.content)
    try:
        for node in students["students"]["student"]:
            if registered and "Registered" != node['status']:
                continue
            yield node
    except KeyError:  # No results
        pass


def get_course_info(series_id):
    url = urljoin(settings.BANNER_BASE_URL, '__get_course_details.php')
    params = {
        'fmt': "json",
        'term': series_id[:6],
        'crn': series_id[6:]
    }
    resp = requests.get(url, params)
    course_info = json.loads(resp.content)
    return course_info
