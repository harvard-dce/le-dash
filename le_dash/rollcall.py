from __future__ import division

from math import ceil
from six import string_types
from le_dash.banner import get_student_list
from le_dash.es import Episode, StudentWatchQuery, StudentSeriesWatchQuery

ATTENDANCE_INTERVAL_INPOINT = 180
ATTENDANCE_WATCHED_THRESHOLD = 50


def series_attendance(series_id):
    students = [Student(x) for x in get_student_list(series_id)]
    attendance = SeriesAttendance.from_series_id(series_id)
    student_attendance = []
    for student in students:
        lectures_watched = attendance.lectures_watched(student.huid)
        student_attendance.append({
            'student': student,
            'lectures_watched': lectures_watched
        })
    return sorted(
        student_attendance,
        key=lambda x: getattr(x['student'], 'last_name')
    )


def lecture_attendance(mpid, sort_key='student.last_name'):
    episode = Episode.findone(mpid=mpid)
    students = [Student(x) for x in get_student_list(episode.series)]
    attendance = LectureAttendance.from_episode(episode)
    student_attendance = []
    for student in students:
        score = attendance.watch_score(student.huid)
        student_attendance.append({
            'student': student,
            'score': score
        })
    return sorted(
        student_attendance,
        key=lambda x: getattr(x['student'], 'last_name')
    )


class Student(object):

    def __init__(self, student_dict):
        self.student_dict = student_dict

    def __getattr__(self, item):
        if item in self.student_dict:
            return self.student_dict[item]
        raise AttributeError()

    @property
    def name(self):
        return ' '.join([
            x for x in [
                getattr(self, y) for y in [
                    'first_name', 'mi', 'last_name'
                ]
            ] if len(x)
        ])

    @property
    def mi(self):
        if isinstance(self.student_dict['mi'], string_types):
            return self.student_dict['mi']
        return ''


class SeriesAttendance(object):

    @classmethod
    def from_series_id(cls, series_id):
        q = StudentSeriesWatchQuery(series_id, ATTENDANCE_INTERVAL_INPOINT)
        resp = q.execute()
        return cls(series_id, resp)

    def __init__(self, series_id, es_resp=None):
        self.series_id = series_id
        self.es_resp = es_resp
        self.episodes = dict(
            (x.mpid, x) for x in Episode.findall(series=series_id)
        )

    def lectures_watched(self, huid):
        watched = 0
        for ep in self.episodes.values():
            inpoint_buckets = self.es_resp.get_agg_buckets(
                'by_inpoint',
                [('by_huid', huid), ('by_mpid', ep.mpid)]
            )
            if inpoint_buckets is None:
                continue
            total_intervals = ceil(
                ep.seconds / ATTENDANCE_INTERVAL_INPOINT
            )
            watch_score = int(100.0 * (len(inpoint_buckets) / total_intervals))
            if watch_score >= ATTENDANCE_WATCHED_THRESHOLD:
                watched += 1
        return watched


class LectureAttendance(object):

    @classmethod
    def from_episode(cls, episode):
        q = StudentWatchQuery(episode.mpid, ATTENDANCE_INTERVAL_INPOINT)
        es_resp = q.execute()
        return cls(episode, es_resp)

    def __init__(self, episode, es_resp=None):
        self.episode = episode
        self.es_resp = es_resp

    def watch_score(self, huid):
        inpoint_buckets = self.es_resp.get_agg_buckets(
            'by_inpoint',
            [('by_huid', huid)]
        )
        if inpoint_buckets is None:
            return 0

        total_intervals = ceil(
            self.episode.seconds / ATTENDANCE_INTERVAL_INPOINT
        )

        return int(100.0 * (len(inpoint_buckets) / total_intervals))


class LectureAttendanceByAllStudents(object):

    def __init__(self, mpid):
        self.mpid = mpid
        self.results = dict()
        self._generate_score()

    def _generate_score(self):
        """ returns an associate array of student and % watched """
        result = StudentWatchQuery(self.mpid).execute().to_dict()
        duration = result['hits']['hits'][0]['_source']['episode']['duration']
        duration /= 1000
        viewings = result['aggregations']['by_huid']['buckets']
        for viewing in viewings:
            student = viewing["key"]
            views = viewing["by_inpoint"]["buckets"]
            sorted_inpoints = sorted(views, key=lambda x: int(x["key"]))
            lastv = 0
            viewed = 0
            for inpoint in sorted_inpoints:
                inpt = int(inpoint["key"])
                # is gap between inpoints, more than 2x 30 seconds
                if (inpt - lastv) > 60:
                    # Assume student watched 60 seconds
                    viewed = viewed + 60
                else:
                    viewed = viewed + (inpt - lastv)    # Close the gap
                lastv = inpt
            self.results[str(student)] = 100.0 * viewed/duration

    def all_scores(self):
        return self.results

    def student_scores(self, student):
        try:
            return self.results[student]
        except:
            return None
