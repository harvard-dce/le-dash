import random
from operator import attrgetter
from le_dash.banner import get_student_list
from le_dash.es import episode_lookup


def series(series_id, sort_key='student.last_name'):
    student_itr = get_student_list(series_id)
    attendance = [SeriesAttendance(series_id, x) for x in student_itr]
    return sorted(attendance, key=attrgetter(sort_key))


def lecture(mpid, sort_key='student.last_name'):
    episode = episode_lookup(mpid=mpid)
    student_itr = get_student_list(episode.series)
    attendance = [LectureAttendance(mpid, x) for x in student_itr]
    return sorted(attendance, key=attrgetter(sort_key))


class Attendance(object):

    @property
    def score(self):
        if not hasattr(self, '_score'):
            self._score = self.generate_score()
        return self._score

    @property
    def name(self):
        return ' '.join([
            x for x in [
                getattr(self.student, y) for y in [
                    'first_name', 'mi', 'last_name'
                ]
            ] if len(x)
        ])

    @property
    def huid(self):
        return self.student.huid


class SeriesAttendance(Attendance):

    def __init__(self, series_id, student):
        self.series_id = series_id
        self.student = student

    def generate_score(self):
        return random.randint(0, 100)


class LectureAttendance(Attendance):

    def __init__(self, mpid, student):
        self.mpid = mpid
        self.student = student

    def generate_score(self):
        return random.randint(0, 100)
