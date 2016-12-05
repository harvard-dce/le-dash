from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from le_dash.es import LectureWatchQuery, episode_lookup

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
    episode = episode_lookup(mpid=mpid)
    context = {'mpid': mpid, 'episode': episode}
    return render(request, 'lecture/lecture.html', context)


def data(request, mpid):
    q = LectureWatchQuery(mpid)
    resp = q.execute()
    return JsonResponse(resp.to_dict())
