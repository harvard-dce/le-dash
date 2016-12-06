import six
import requests
from django.conf import settings
from collections import namedtuple

if six.PY2:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin

StudentInfo = namedtuple(
    'StudentInfo',
    ['huid', 'first_name', 'mi', 'last_name']
)


def banner_req(url, params):
    params['fmt'] = 'json'
    resp = requests.get(url, params)
    resp.raise_for_status()
    return resp.json()


def get_student_list(series_id, registered=True, raw=False):
    url = urljoin(settings.BANNER_BASE_URL, '__get_classlist.php')
    params = {
        'term': series_id[:6],
        'crn': series_id[6:]
    }
    students = banner_req(url, params)
    try:
        for node in students["students"]["student"]:
            if registered and "Registered" != node['status']:
                continue
            if raw:
                yield node
            else:
                s = StudentInfo._make(node[f] for f in StudentInfo._fields)
                yield s
    except KeyError:  # No results
        pass
