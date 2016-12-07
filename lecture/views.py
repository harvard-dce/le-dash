from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from le_dash.es import LectureWatchQuery, Episode

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
    episode = Episode.findone(mpid=mpid)
    context = {
        'mpid': mpid,
        'episode': episode,
        'chart_title': 'Lecture Histogram',
        'chart_description':
            'Number of Times a Section of the Video Has '
            'Been Watched (Resolution is 5 Minutes)'}
    return render(request, 'lecture/lecture.html', context)


def data(request, mpid):
    q = LectureWatchQuery(mpid)
    resp = q.execute()
    return JsonResponse(resp.to_dict())
