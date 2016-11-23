from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from le_dash.es import LectureWatchQuery


def index(request):
    return render(request, 'lecture/index.html')


def lecture(request, mpid):
    return HttpResponse("lecture: %s" % mpid)


def data(request, mpid):
    q = LectureWatchQuery(mpid)
    resp = q.execute()
    return JsonResponse(resp.to_dict())
