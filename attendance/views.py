from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from le_dash import rollcall
from le_dash.es import StudentWatchQuery


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


def data(request, mpid):
    q = StudentWatchQuery(mpid)
    resp = q.execute()
    return JsonResponse(resp.to_dict())


def summary(request, mpid):
    context = {'mpid': mpid}
    return render(request, 'attendance/summary.html', context)


def detailed(request, mpid):
    context = {'mpid': mpid}
    return render(request, 'attendance/detailed.html', context)


def summarytable(request, mpid):
    students = rollcall.LectureAttendanceByAllStudents(mpid).all_scores()
    context = {'students': students, 'mpid': mpid}
    return render(request, 'attendance/student-summary-table.html', context)
