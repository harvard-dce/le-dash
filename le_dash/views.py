from django.shortcuts import render
from le_dash import __version__


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html', {'version': __version__})
