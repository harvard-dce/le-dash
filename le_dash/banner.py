import hashlib
import logging

import requests
import six
from django.conf import settings
from django.core.cache import cache

if six.PY2:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin

logger = logging.getLogger(__name__)


def banner_req(url, params={}):
    #  md5 is cheaper than urlunparse/urlencode params
    get_url = hashlib.md5("{0}".format(params))
    params['fmt'] = 'json'
    try:
        result = cache.get(get_url)
        if result:
            return result
    except:
        logger.error("Caching is broken")
    resp = requests.get(url, params)
    resp.raise_for_status()
    result = resp.json()
    try:
        cache.set(get_url, result)
    except:
        pass
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


def get_current_term():
    url = urljoin(settings.BANNER_BASE_URL, "__get_current_termcode.php")
    term = banner_req(url)
    if isinstance(term, dict):
        return term["term_code"]
    return None


def get_current_course_list(termcode=None):
    if not termcode:
        termcode = get_current_term()
    url = urljoin(settings.BANNER_BASE_URL, "__get_courses_by_term.php")
    params = {
        'term': termcode,
    }
    courses_data = banner_req(url, params)
    if courses_data:
        courses = courses_data['courses'].get('course', [])
        if isinstance(courses, dict):
            courses = [courses]
        for x in courses:
            x["fullcrn"] = termcode + x["crn"]
        return courses
    return []
