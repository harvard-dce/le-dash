from . import es


def test_lecture_watch_query_const():
    q_dict = es.LectureWatchQuery('foo').to_dict()
    assert q_dict['query']['bool']['must'][0]['match']['mpid'] == 'foo'

    q_dict = es.LectureWatchQuery('foo', interval_inpoint=999).to_dict()
    assert q_dict['aggs']['by_inpoint']['histogram']['interval'] == '999'

    q_dict = es.LectureWatchQuery('foo', interval_timestamp='99d').to_dict()
    # use of .get() is just to avoid over-long line
    assert q_dict['aggs']['by_inpoint']['aggs']['by_user'] \
        .get('aggs')['by_period']['date_histogram']['interval'] == '99d'
