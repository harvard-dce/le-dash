from le_dash.rollcall import SeriesAttendance, LectureAttendance
from le_dash.es import Episode
from mock import patch


def test_lectures_watched_by_huid(mocker, es_resp_maker):
    eps = [
        Episode({'mpid': '123-abc', 'duration': 360000}),
        Episode({'mpid': '456-efg', 'duration': 540000})
    ]
    mocker.patch('le_dash.es.Episode.findall', return_value=eps)

    # lectures_watched() only counts up the # of inpoint buckets so
    # actual 'key' and 'doc_count' values don't matter
    agg_data = {
        'by_huid': {
            'buckets': [
                {
                    # student watched 100% of 1st lecture, 66% of 2nd
                    'key': '12121212',
                    'by_mpid': {
                        'buckets': [
                            {
                                'key': '123-abc',
                                'by_inpoint': {
                                    'buckets': [1, 2]
                                }
                            },
                            {
                                'key': '456-efg',
                                'by_inpoint': {
                                    'buckets': [1, 2]
                                }
                            }
                        ]
                    }
                },
                {
                    # student watched 50% of 1st lecture, 33% of 2nd
                    'key': '99999999',
                    'by_mpid': {
                        'buckets': [
                            {
                                'key': '123-abc',
                                'by_inpoint': {
                                    'buckets': [1]
                                }
                            },
                            {
                                'key': '456-efg',
                                'by_inpoint': {
                                    'buckets': [1]
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }
    es_resp = es_resp_maker(aggregations=agg_data)
    sa = SeriesAttendance('1000000099', es_resp)

    # default ATTENDANCE_WATCHED_THRESHOLD is 50%
    assert sa.lectures_watched('12121212') == 2
    assert sa.lectures_watched('99999999') == 1

    with patch('le_dash.rollcall.ATTENDANCE_WATCHED_THRESHOLD', 70):
        assert sa.lectures_watched('12121212') == 1
        assert sa.lectures_watched('99999999') == 0


def test_watch_score_by_huid(mocker, es_resp_maker):
    episode = Episode({'mpid': '456-efg', 'duration': 1800000})
    agg_data = {
        'by_huid': {
            'buckets': [
                {
                    # student watched 70% of the lecture
                    'key': '12121212',
                    'by_inpoint': {
                        'buckets': [1, 2, 3, 4, 5, 6, 7]
                    }
                },
                {
                    # student watched 40%
                    'key': '99999999',
                    'by_inpoint': {
                        'buckets': [1, 2, 3, 4]
                    }
                }
            ]
        }
    }
    es_resp = es_resp_maker(aggregations=agg_data)
    la = LectureAttendance(episode, es_resp)
    assert la.watch_score('12121212') == 70
    assert la.watch_score('99999999') == 40
