import pytest


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
