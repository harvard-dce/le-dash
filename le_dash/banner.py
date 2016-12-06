import six
import requests
from django.conf import settings

if six.PY2:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin


def banner_req(url, params):
    params['fmt'] = 'json'
    resp = requests.get(url, params)
    resp.raise_for_status()
    return resp.json()


def get_student_list(series_id, registered=True):
    url = urljoin(settings.BANNER_BASE_URL, '__get_classlist.php')
    params = {
        'term': series_id[:6],
        'crn': series_id[6:]
    }
    student_data = banner_req(url, params)
    students = student_data['students'].get('student', [])

    # protect against single-item result which is structured as a dict
    # rathern than a list of dicts
    if isinstance(students, dict):
        students = [students]

    if registered:
        students = [x for x in students if x['status'] == 'Registered']

    return students
