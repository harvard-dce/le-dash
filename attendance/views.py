from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from le_dash import rollcall, banner
from le_dash.es import Episode, SeriesViewingQuery, \
    StudentSummaryWatchQuery

from .forms import SeriesForm


def index(request):
    if request.method == 'POST':
        form = SeriesForm(request.POST)
        if form.is_valid():
            series_id = form.cleaned_data['series_id'].strip()
            display = form.cleaned_data['display'].strip()
            if display == "table":
                return HttpResponseRedirect(reverse(
                    'attendance-series', args=(series_id,)))
            else:
                return HttpResponseRedirect(reverse(
                    'attendance-series-viewing', args=(series_id,)))
    else:
        form = SeriesForm()

    return render(request, 'attendance/index.html', {'form': form})


def series(request, series_id):
    series = rollcall.Series(series_id)
    attendance = rollcall.series_attendance(series)
    context = {
        'series': series,
        'attendance': attendance,
        'total_students': len(attendance)
    }
    return render(request, 'attendance/series.html', context)


def lecture(request, mpid):
    episode = Episode.findone(mpid=mpid)
    attendance = rollcall.lecture_attendance(episode.mpid)
    context = {
        'mpid': mpid,
        'episode': episode,
        'attendance': attendance
    }
    return render(request, 'attendance/lecture.html', context)


def lectures(request, series_id):
    series = rollcall.Series(series_id)
    lectures_watched = rollcall.series_lectures(series)
    context = {
        'series': series,
        'lectures': lectures_watched,
        'total_students': len(series.students)
    }
    return render(request, 'attendance/lectures.html', context)


def lectures_data(request, series_id):
    q = SeriesViewingQuery(series_id)
    resp = q.execute()
    results = resp.to_dict()
    episodes_dump = Episode.findall(series=series_id, size=999)
    if episodes_dump:
        episodes = [{"mpid": episode.mpid,
                     "title": episode.title,
                     "type": episode.type,
                     "duration": episode.duration}
                    for episode in episodes_dump]
        results["episodes"] = episodes

    return JsonResponse(results)



def student(request, huid):
    return HttpResponse("student: %s" % huid)


def series_student_data(request, series_id):
    student_data = banner.get_student_list(series_id)
    return JsonResponse({"students": student_data})


def data(request, mpid):
    q = StudentSummaryWatchQuery(mpid)
    resp = q.execute()
    results = resp.to_dict()

    episode = Episode.findone(mpid=mpid)
    if episode:
        student_data = banner.get_student_list(episode.series)
        results['students'] = student_data

    return JsonResponse(results)


def summary(request, mpid):
    episode = Episode.findone(mpid=mpid)
    if episode:
        context = {'mpid': mpid,
                   'title': episode.title,
                   'course_name': episode.course,
                   'series': episode.series,
                   }
    else:
        context = {'mpid': mpid}
    return render(request, 'attendance/summary.html', context)


def detailed(request, mpid):
    episode = Episode.findone(mpid=mpid)
    context = {'episode': episode}
    return render(request, 'attendance/detailed.html', context)


def summarytable(request, mpid):
    students = rollcall.LectureAttendanceByAllStudents(mpid).all_scores()
    try:
        episode = Episode.findone(mpid=mpid)
        context = {'students': students,
                   'title': episode.title,
                   'course_name': episode.course,
                   'series': episode.series,
                   'mpid': mpid}
    except:
        context = {'students': students, 'mpid': mpid}
    return render(request, 'attendance/student-summary-table.html', context)



