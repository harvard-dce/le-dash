from django.http import HttpResponse
from django.shortcuts import render
from le_dash import rollcall


def index(request):
    return render(request, 'attendance/index.html')


def series(request, series_id):
    students = rollcall.series(series_id)
    context = {
        'series_id': series_id,
        'attendance': students
    }
    return render(request, 'attendance/series.html', context)


def lecture(request, mpid):
    students = rollcall.lecture(mpid)
    context = {
        'mpid': mpid,
        'attendance': students
    }
    return render(request, 'attendance/lecture.html', context)


def student(request, huid):
    return HttpResponse("student: %s" % huid)
