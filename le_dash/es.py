from django.conf import settings

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q


class ESResponse(object):

    def __init__(self, response):
        self.response = response

    def to_dict(self):
        return self.response.to_dict()


class ESQuery(object):

    def to_dict(self):
        return self.search.to_dict()

    def execute(self):
        resp = self.search.execute()
        return ESResponse(resp)


class UserActionQuery(ESQuery):

    def __init__(self):
        self.es = Elasticsearch(settings.ES_HOST)
        self.index = settings.ES_INDEX_PATTERNS['useractions']
        self.search = Search(using=self.es, index=self.index)


class LectureWatchQuery(UserActionQuery):

    def __init__(self, mpid, interval_inpoint='300', interval_timestamp='5m'):
        super(LectureWatchQuery, self).__init__()

        self.search = self.search \
            .query("match", mpid=mpid) \
            .filter(
                Q('term', is_live=0) &
                Q('term', **{'action.is_playing': True}) &
                Q('term', **{'action.type': 'HEARTBEAT'})
            )

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
