from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from le_dash.es import LectureWatchQuery

from .forms import MpidForm


def index(request):
    if request.method == 'POST':
        form = MpidForm(request.POST)
        if form.is_valid():
            mpid = form.cleaned_data['mpid'].strip()
            return HttpResponseRedirect(reverse('lecture', args=(mpid, )))
    else:
        form = MpidForm()

    return render(request, 'lecture/index.html', {'form': form})


def lecture(request, mpid):
    return HttpResponse("lecture: %s" % mpid)


def data(request, mpid):
    q = LectureWatchQuery(mpid)
    resp = q.execute()
    return JsonResponse(resp.to_dict())


def histogram(request, mpid):
    # Need to fill in course_name, lecture number, etc
    context = {'mpid': mpid}
    return render(request, 'lecture/histogram.html', context)
