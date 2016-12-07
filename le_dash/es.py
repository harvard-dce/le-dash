from django.conf import settings

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q


class ESResponse(object):
    def __init__(self, response):
        self.response = response

    def to_dict(self):
        return self.response.to_dict()

    @property
    def hits(self):
        return self.response.hits

    @property
    def aggregations(self):
        return self.response.aggregations

    def get_agg_buckets(self, agg_name, agg_path=[], agg_node=None):

        if agg_node is None:
            agg_node = self.aggregations

        if len(agg_path):
            path_name, path_key = agg_path.pop(0)
            current_node = getattr(agg_node, path_name)

            try:
                bucket = next(
                    b for b in current_node.buckets if b['key'] == path_key
                )
            except StopIteration:
                return None

            return self.get_agg_buckets(agg_name, agg_path, bucket)
        else:
            return getattr(agg_node, agg_name).buckets


class ESQuery(object):
    def __init__(self):
        self.es = Elasticsearch(settings.ES_HOST)
        self.search = Search(using=self.es, index=self.index)

    def to_dict(self):
        return self.search.to_dict()

    def execute(self):
        resp = self.search.execute()
        self.resp = ESResponse(resp)
        return self.resp


class EpisodeQuery(ESQuery):
    def __init__(self, size=None, **kwargs):
        self.index = settings.ES_INDEX_PATTERNS['episodes']
        super(EpisodeQuery, self).__init__()

        if size is not None:
            self.search = self.search.extra(size=size)

        for field, value in kwargs.items():
            self.search = self.search.query("match", **{field: value})


class UserActionQuery(ESQuery):
    def __init__(self):
        self.index = settings.ES_INDEX_PATTERNS['useractions']
        super(UserActionQuery, self).__init__()


class LectureWatchQuery(UserActionQuery):
    def __init__(self, mpid, interval_inpoint='300', interval_timestamp='5m'):
        super(LectureWatchQuery, self).__init__()

        self.search = self.search \
            .query("match", mpid=mpid) \
            .filter(
                Q('term', is_live=0) &
                Q('term', **{'action.is_playing': True}) &
                Q('term', **{'action.type': 'HEARTBEAT'}))

        self.search = self.search.extra(size=0)

        self.search.aggs.bucket(
            name='by_inpoint',
            agg_type='histogram',
            field='action.inpoint',
            interval=str(interval_inpoint)
        )
        self.search.aggs['by_inpoint'].bucket(
            name='by_huid',
            agg_type='terms',
            field='huid'
        )
        self.search.aggs['by_inpoint']['by_huid'].bucket(
            name='by_period',
            agg_type='date_histogram',
            field='@timestamp',
            interval=str(interval_timestamp),
            format="yyyy-MM-dd HH:mm:ss",
            min_doc_count=1
        )


class StudentWatchQuery(UserActionQuery):
    """
        All the distinct inpoints from each student for a mpid, each inpoint
        means (30-60s) of video, this is used in conjunction with javascript
        to calculate amount of footage watched
    """

    def __init__(self, mpid, interval_inpoint):
        super(StudentWatchQuery, self).__init__()

        self.search = self.search \
            .query("match", mpid=mpid) \
            .filter(
                Q('term', is_live=0) &
                Q('term', **{'action.is_playing': True}) &
                Q('term', **{'action.type': 'HEARTBEAT'}))

        self.search = self.search.extra(size=1)

        self.search.aggs.bucket(
            name='by_huid',
            agg_type='terms',
            field='huid',
            size=0
        )
        self.search.aggs['by_huid'].bucket(
            name='by_inpoint',
            agg_type='histogram',
            field='action.inpoint',
            interval=str(interval_inpoint),
            min_doc_count=1
        )


class StudentSummaryWatchQuery(UserActionQuery):
    """
        All the distinct inpoints from each student for a mpid, each inpoint
        means (30-60s) of video, this is used in conjunction with javascript
        to calculate amount of footage watched
    """

    def __init__(self, mpid):
        super(StudentSummaryWatchQuery, self).__init__()

        self.search = self.search \
            .query("match", mpid=mpid) \
            .filter(
                Q('term', is_live=0) &
                Q('term', **{'action.is_playing': True}) &
                Q('term', **{'action.type': 'HEARTBEAT'}))

        self.search = self.search.extra(size=1)

        self.search.aggs.bucket(
            name='by_huid',
            agg_type='terms',
            field='huid',
            size=0
        )
        self.search.aggs['by_huid'].bucket(
            name='by_inpoint',
            agg_type='terms',
            field='action.inpoint',
            size=0
        )


class StudentSeriesWatchQuery(UserActionQuery):
    """
        Listing all the episodes in the series and the number of students
        who watched them
    """

    def __init__(self, series_id, interval_inpoint):
        super(StudentSeriesWatchQuery, self).__init__()

        self.search = self.search \
            .query("match", **{'episode.series': series_id}) \
            .filter(
                Q('term', is_live=0) &
                Q('term', **{'action.is_playing': True}) &
                Q('term', **{'action.type': 'HEARTBEAT'}))

        self.search = self.search.extra(size=0)

        self.search.aggs.bucket(
            name='by_huid',
            agg_type='terms',
            field='huid',
            size=0
        )
        self.search.aggs['by_huid'].bucket(
            name='by_mpid',
            agg_type='terms',
            field='mpid',
            size=0
        )
        self.search.aggs['by_huid']['by_mpid'].bucket(
            name='by_inpoint',
            agg_type='histogram',
            field='action.inpoint',
            interval=str(interval_inpoint),
            min_doc_count=1
        )


class SeriesViewingQuery(UserActionQuery):
    """
        Listing all the episodes in the series and the number of students
        who watched them
    """

    def __init__(self, seriesid):
        super(SeriesViewingQuery, self).__init__()

        self.search = self.search \
            .query("match", **{'episode.series': seriesid}) \
            .filter(
                Q('term', is_live=0) &
                Q('term', **{'action.is_playing': True}) &
                Q('term', **{'action.type': 'HEARTBEAT'}))

        self.search = self.search.extra(size=0)

        self.search.aggs.bucket(
            name='by_mpid',
            agg_type='terms',
            field='mpid',
            size=0
        )
        self.search.aggs['by_mpid'].bucket(
            name='by_huid',
            agg_type='terms',
            field='huid',
            size=0
        )


class Episode(object):

    @staticmethod
    def findone(**kwargs):
        q = EpisodeQuery(size=1, **kwargs)
        resp = q.execute()
        if resp.hits.total:
            return Episode(resp.hits[0].to_dict())
        return

    @staticmethod
    def findall(**kwargs):
        q = EpisodeQuery(**kwargs)
        resp = q.execute()
        return [Episode(x.to_dict()) for x in resp.hits]

    def __init__(self, doc):
        self.doc = doc

    def __getattr__(self, item):
        if item in self.doc:
            return self.doc[item]
        raise AttributeError()

    @property
    def seconds(self):
        return int(self.duration / 1000)


class Series(object):

    def __init__(self, series_id):
        self.id = series_id
        self.episodes = Episode.findall(series=series_id)

    def total_lectures(self):
        return len(self.episodes)

    def course_name(self):
        return self.episodes[0].course
