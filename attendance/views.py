from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from le_dash import rollcall, banner
from le_dash.es import StudentWatchQuery, SeriesWatchQuery, episode_lookup

from .forms import SeriesForm


def index(request):
    if request.method == 'POST':
        form = SeriesForm(request.POST)
        if form.is_valid():
            series_id = form.cleaned_data['series_id'].strip()
            return HttpResponseRedirect(reverse(
                'attendance-series', args=(series_id,)))
    else:
        form = SeriesForm()

    return render(request, 'attendance/index.html', {'form': form})


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


def series_student_data(request, series_id):
    students = [student for student in banner.get_student_list_raw(series_id)]
    return JsonResponse({"students": students})


def data(request, mpid):
    q = StudentWatchQuery(mpid)
    resp = q.execute()
    results = resp.to_dict()

    episode = episode_lookup(mpid=mpid)
    if episode:
        students = [student for student in
                    banner.get_student_list_raw(episode.series)]
        results["students"] = students

    return JsonResponse(results)


def summary(request, mpid):
    episode = episode_lookup(mpid=mpid)
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
    episode = episode_lookup(mpid=mpid)
    if episode:
        context = {'mpid': mpid,
                   'title': episode.title,
                   'course_name': episode.course,
                   'series': episode.series}
    else:
        context = {'mpid': mpid}
    return render(request, 'attendance/detailed.html', context)


def summarytable(request, mpid):
    students = rollcall.LectureAttendanceByAllStudents(mpid).all_scores()
    try:
        episode = episode_lookup(mpid=mpid)
        context = {'students': students,
                   'title': episode.title,
                   'course_name': episode.course,
                   'series': episode.series,
                   'mpid': mpid}
    except:
        context = {'students': students, 'mpid': mpid}
    return render(request, 'attendance/student-summary-table.html', context)


def series_viewing_data(request, series_id):
    q = SeriesWatchQuery(series_id)
    resp = q.execute()
    return JsonResponse(resp.to_dict())


def series_viewing(request, series_id):
    # Need to fill in course_name, lecture title, etc
    course_info = banner.get_course_info(series_id)
    if course_info:
        context = {'series_id': series_id,
                   'course_name': course_info['course_name'],
                   'course_title': course_info['course_title']}
    else:
        context = {'series_id': series_id}
    return render(request, 'attendance/series_viewing.html', context)
