import six
import requests
from django.conf import settings
from collections import namedtuple


if six.PY3:
    from xml.etree import ElementTree as etree
    from urllib.parse import urljoin
else:
    import lxml.etree as etree
    from urlparse import urljoin


StudentInfo = namedtuple(
    'StudentInfo',
    ['huid', 'first_name', 'mi', 'last_name']
)


def get_student_list(series_id):
    url = urljoin(settings.BANNER_BASE_URL, '__get_classlist.php')
    params = {
        'term': series_id[:6],
        'crn': series_id[6:]
    }
    resp = requests.get(url, params)
    xml = etree.fromstring(resp.content)
    for node in xml.iterfind('*/student'):
        s = StudentInfo._make(node.findtext(f) for f in StudentInfo._fields)
        yield s
