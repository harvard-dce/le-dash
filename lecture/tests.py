import pytest


@pytest.fixture(autouse=True)
def urlconf_setting(settings):
    settings.ROOT_URLCONF = 'lecture.urls'


def test_lecture(client):

    response = client.get('/ea00b6b4-713a-48e2-9b3d-500504aa7615/')
    assert response.content == b'lecture: ea00b6b4-713a-48e2-9b3d-500504aa7615'

    response = client.get('/ea00b6b4-713a-48e2-9b3d-500504aa7615-99/')
    assert response.status_code == 404
