from collections import namedtuple


def test_series(client, mocker, student_list_maker):

    student_list = student_list_maker(
        ('12345', 'Abigail', 'Q', 'Adams'),
        ('23456', 'Corin', '', 'Tucker'),
        ('34567', 'Serena', 'S', 'Williams')
    )
    mocker.patch('le_dash.rollcall.get_student_list',
                 return_value=student_list)

    response = client.get('/attendance/series/20170110207/')
    assert b'report for series 20170110207' in response.content
    assert b'<td>Serena S Williams</td>' in response.content


def test_series_no_slash_redirect(client):

    response = client.get('/attendance/series/20170110207')
    assert response.status_code == 301


def test_series_404(client):

    response = client.get('/attendance/series/201701102xx/')
    assert response.status_code == 404


def test_lecture(client, mocker, student_list_maker):

    student_list = student_list_maker(
        ('45678', 'Paul', 'S', 'Rudd'),
        ('67890', 'Twilight', 'P', 'Sparkle'),
        ('837465', 'Chief', 'C', 'Burns')
    )
    mocker.patch('le_dash.rollcall.get_student_list',
                 return_value=student_list)

    fake_episode = namedtuple('FakeEpisode', 'series')._make(('foo',))
    mocker.patch('le_dash.rollcall.Episode.findone', return_value=fake_episode)

    response = client.get(
        '/attendance/lecture/ea00b6b4-713a-48e2-9b3d-500504aa7615/'
    )
    assert b'report for lecture ea00b6b4-713a-48e2-9b3d-500504aa7615' \
           in response.content
    assert b'<td>Twilight P Sparkle</td>' in response.content
    assert b'<td>837465</td>' in response.content


def test_lecture_404(client):

    response = client.get(
        '/attendance/lecture/ea00b6b4-713a-48e2-9b3d-500504aa7615-99/'
    )
    assert response.status_code == 404


def test_student(client):

    response = client.get('/attendance/student/55555555/')
    assert response.content == b'student: 55555555'

    response = client.get('/attendance/student/abcd1234/')
    assert response.content == b'student: abcd1234'

    response = client.get('/attendance/student/anonymous/')
    assert response.content == b'student: anonymous'

    response = client.get('/attendance/student/foo-123345/')
    assert response.status_code == 404
