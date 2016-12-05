from datetime import datetime
from le_dash.es import Episode


def test_lecture(client, mocker):

    ep = Episode({
        'mpid': 'ea00b6b4-713a-48e2-9b3d-500504aa7615',
        'course': 'Foo 101',
        'title': 'Lecture 39',
        'duration': 10000099,
        'series': '20170156789',
        'start': datetime.now()
    })
    mocker.patch('lecture.views.episode_lookup', return_value=ep)

    response = client.get('/lecture/ea00b6b4-713a-48e2-9b3d-500504aa7615/')
    assert b'Foo 101' in response.content
    assert b'2:46:40' in response.content


def test_lecture_404(client):

    response = client.get('/lecture/ea00b6b4-713a-48e2-9b3d-500504aa7615-99/')
    assert response.status_code == 404
