from django.http import HttpResponse


def series(request, series_id):
    return HttpResponse("series: %s" % series_id)


def lecture(request, mpid):
    return HttpResponse("lecture: %s" % mpid)


def student(request, huid):
    return HttpResponse("student: %s" % huid)
