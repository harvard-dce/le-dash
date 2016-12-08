import hashlib
from django.conf import settings

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from django.core.cache import cache


class ESResponse(object):
    def __init__(self, response):
        self.response = response

    def to_dict(self):
        return self.response.to_dict()

    @property
    def hits(self):
        return self.response.hits


class ESQuery(object):
    def __init__(self):
        self.es = Elasticsearch(settings.ES_HOST)
        self.search = Search(using=self.es, index=self.index)

    def to_dict(self):
        return self.search.to_dict()

    def execute(self):
        key = hashlib.md5("{0}".format(self.to_dict()))
        try:  # Do not crash if cache is missing
            resp = cache.get(key)
            if not resp:
                resp = self.search.execute()
                if resp.hits > 0:   # only cache good results
                    cache.set(key, resp)
        except:
            resp = self.search.execute()
        return ESResponse(resp)


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
            name='by_user',
            agg_type='terms',
            field='huid'
        )
        self.search.aggs['by_inpoint']['by_user'].bucket(
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

    def __init__(self, mpid):
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
            agg_type='terms',
            field='action.inpoint',
            size=0
        )


class SeriesWatchQuery(UserActionQuery):
    """
        Listing all the episodes in the series and the number of students
        who watched them
    """

    def __init__(self, seriesid):
        super(SeriesWatchQuery, self).__init__()

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
            return Episode(resp.hits[0])
        return

    @staticmethod
    def findall(**kwargs):
        q = EpisodeQuery(**kwargs)
        resp = q.execute()
        return [Episode(x) for x in resp.hits]

    def __init__(self, doc):
        self.doc = doc

    def __getattr__(self, item):
        if item in self.doc:
            return self.doc[item]
        raise AttributeError()
