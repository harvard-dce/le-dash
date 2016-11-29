import pytest


@pytest.fixture(autouse=True)
def urlconf_setting(settings):
    settings.ROOT_URLCONF = 'attendance.urls'


def test_series(client):

    response = client.get('/series/20170110207/')
    assert response.content == b'series: 20170110207'

    response = client.get('/series/20170110207')
    assert response.status_code == 301

    response = client.get('/series/201701102xx/')
    assert response.status_code == 404


def test_lecture(client):

    response = client.get('/lecture/ea00b6b4-713a-48e2-9b3d-500504aa7615/')
    assert response.content == b'lecture: ea00b6b4-713a-48e2-9b3d-500504aa7615'

    response = client.get('/lecture/ea00b6b4-713a-48e2-9b3d-500504aa7615-99/')
    assert response.status_code == 404


def test_student(client):

    response = client.get('/student/55555555/')
    assert response.content == b'student: 55555555'

    response = client.get('/student/abcd1234/')
    assert response.content == b'student: abcd1234'

    response = client.get('/student/anonymous/')
    assert response.content == b'student: anonymous'

    response = client.get('/student/foo-123345/')
    assert response.status_code == 404
