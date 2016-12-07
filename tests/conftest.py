import pytest
from le_dash.es import ESResponse
from elasticsearch_dsl import result


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr("requests.sessions.Session.request")


@pytest.fixture()
def student_maker():
    def _student_maker(huid, first_name, mi, last_name, status='Registered'):
        return {
            'huid': huid,
            'first_name': first_name,
            'mi': mi,
            'last_name': last_name,
            'status': status
        }
    return _student_maker


@pytest.fixture()
def student_list_maker(student_maker):
    def _student_list_maker(*attr_list):
        return [student_maker(*x) for x in attr_list]
    return _student_list_maker


@pytest.fixture
def dummy_response():
    return {
      "_shards": {
        "failed": 0,
        "successful": 10,
        "total": 10
      },
      "hits": {
        "hits": [
        ],
        "max_score": 0.0,
        "total": 0
      },
      "aggregations": {},
      "timed_out": False,
      "took": 123
    }


@pytest.fixture()
def es_resp_maker(dummy_response):
    def _resp_maker(hits=[], aggregations={}):
        dummy_response['hits']['hits'] = hits
        dummy_response['aggregations'] = aggregations
        return ESResponse(result.Response(dummy_response))
    return _resp_maker


@pytest.fixture(autouse=True)
def no_searches(mocker, dummy_response):
    mocker.patch('elasticsearch_dsl.Search.execute',
                 return_value=result.Response(dummy_response))
