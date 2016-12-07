from datetime import datetime
from le_dash.es import Episode
from le_dash.rollcall import Student
from mock import Mock


def test_series_attendance_view(client, mocker, student_list_maker):
    student_list = student_list_maker(
        ('12345', 'Abigail', 'Q', 'Adams'),
        ('23456', 'Corin', '', 'Tucker'),
        ('34567', 'Serena', 'S', 'Williams')
    )
    watched = [3, 9, 13]
    mock_attendance = []
    for student in student_list:
        mock_attendance.append({
            'student': Student(student),
            'lectures_watched': watched.pop(0)
        })
    mocker.patch('le_dash.rollcall.series_attendance',
                 return_value=mock_attendance)
    mock_series = Mock(id='20170110207',
                       course_name='Foo Studies',
                       total_lectures=20
                       )
    mocker.patch('le_dash.es.Series', return_value=mock_series)

    response = client.get('/attendance/series/20170110207/')
    assert b'Foo Studies' in response.content
    assert b'<td>Serena S Williams</td>' in response.content
    assert b'<td>9 of 20</td>' in response.content


def test_series_no_slash_redirect(client):

    response = client.get('/attendance/series/20170110207')
    assert response.status_code == 301


def test_series_404(client):

    response = client.get('/attendance/series/201701102xx/')
    assert response.status_code == 404


def test_lecture(client, mocker, student_list_maker):

    ep = Episode({
        'series': '20170110207',
        'title': 'Lecture 11',
        'mpid': 'ea00b6b4-713a-48e2-9b3d-500504aa7615',
        'course': 'Baz 101',
        'duration': 101010101,
        'start': datetime.now()
    })
    mocker.patch('le_dash.es.Episode.findone', return_value=ep)

    student_list = student_list_maker(
        ('45678', 'Paul', 'S', 'Rudd'),
        ('67890', 'Twilight', 'P', 'Sparkle'),
        ('837465', 'Chief', 'C', 'Burns')
    )
    scores = [33, 89, 66]
    mock_attendance = []
    for student in student_list:
        mock_attendance.append({
            'student': Student(student),
            'score': scores.pop(0)
        })
    mocker.patch('le_dash.rollcall.lecture_attendance',
                 return_value=mock_attendance)

    response = client.get(
        '/attendance/lecture/ea00b6b4-713a-48e2-9b3d-500504aa7615/'
    )
    assert b'Baz 101' in response.content
    assert b'Lecture 11' in response.content
    assert b'<td>Twilight P Sparkle</td>' in response.content
    assert b'<td>837465</td>' in response.content
    assert b'<td>66</td>' in response.content


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
