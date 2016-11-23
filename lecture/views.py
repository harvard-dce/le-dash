from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'lecture/index.html')


def lecture(request, mpid):
    return HttpResponse("lecture: %s" % mpid)
