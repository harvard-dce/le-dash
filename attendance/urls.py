
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^series/(?P<series_id>\d{11})/$', views.series,
        name='attendance-series'),
    url(r'^lecture/(?P<mpid>[\w\-]{36})/$', views.lecture,
        name='attendance-lecture'),
    url(r'^student/(?P<huid>\w+)/$', views.student,
        name='attendance-student')
]
