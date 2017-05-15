from django.shortcuts import render

from banner import get_current_course_list, get_current_term
from . import __version__


def home(request):
    term = get_current_term()
    courses = get_current_course_list(term)
    context = {
        'courses': courses,
        'term': term
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html', {'version': __version__})
