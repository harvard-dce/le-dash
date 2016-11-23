from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'attendance/index.html')


def series(request, series_id):
    return HttpResponse("series: %s" % series_id)


def lecture(request, mpid):
    return HttpResponse("lecture: %s" % mpid)


def student(request, huid):
    return HttpResponse("student: %s" % huid)
