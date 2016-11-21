from django.http import HttpResponse


def lecture(request, mpid):
    return HttpResponse("lecture: %s" % mpid)
