import six
import hashlib
import requests
from django.conf import settings
from django.core.cache import cache

if six.PY2:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin


def banner_req(url, params):

    cache_key = hashlib.md5(
        "{0} {1}".format(url, params).encode('utf-8')
    ).hexdigest()

    result = cache.get(cache_key)
    if result:
        return result

    params['fmt'] = 'json'
    resp = requests.get(url, params)
    resp.raise_for_status()
    result = resp.json()

    cache.set(cache_key, result)
    return result


def get_student_list(series_id, registered=True):
    url = urljoin(settings.BANNER_BASE_URL, '__get_classlist.php')
    params = {
        'term': series_id[:6],
        'crn': series_id[6:]
    }
    student_data = banner_req(url, params)
    students = student_data['students'].get('student', [])

    # protect against single-item result which is structured as a dict
    # rather than a list of dicts
    if isinstance(students, dict):
        students = [students]

    if registered:
        students = [x for x in students if x['status'] == 'Registered']

    return students
