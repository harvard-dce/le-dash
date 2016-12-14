
from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.index, name='attendance-index'),
    url(r'^series/(?P<series_id>\d{11})/$', views.series,
        name='attendance-series'),
    url(r'^lectures/(?P<series_id>\d{11})/$', views.lectures,
        name='attendance-lectures'),

    url(r'^lecture/(?P<mpid>[\w\-]{36})/$', views.lecture,
        name='attendance-lecture'),
    url(r'^data/(?P<mpid>[\w\-]{36})/$', views.data,
        name='attendance-data'),
    url(r'^summary/(?P<mpid>[\w\-]{36})/$', views.summary,
        name='attendance-summary'),
    url(r'^summarytable/(?P<mpid>[\w\-]{36})/$', views.summarytable,
        name='attendance-summarytable'),
    url(r'^detailed/(?P<mpid>[\w\-]{36})/$', views.detailed,
        name='attendance-detailed'),
    url(r'^series_student_data/(?P<series_id>\d{11})/$',
        views.series_student_data,
        name='attendance-series-student-data'),
]
