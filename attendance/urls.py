
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='attendance-index'),
    url(r'^series/(?P<series_id>\d{11})/$', views.series,
        name='attendance-series'),
    url(r'^lecture/(?P<mpid>[\w\-]{36})/$', views.lecture,
        name='attendance-lecture'),
    url(r'^student/(?P<huid>\w+)/$', views.student,
        name='attendance-student'),
    url(r'^data/(?P<mpid>[\w\-]{36})/$', views.data,
        name='attendance-data'),
    url(r'^summary/(?P<mpid>[\w\-]{36})/$', views.summary,
        name='attendance-summary'),
    url(r'^summarytable/(?P<mpid>[\w\-]{36})/$', views.summarytable,
        name='attendance-summarytable'),
    url(r'^detailed/(?P<mpid>[\w\-]{36})/$', views.detailed,
        name='attendance-detailed')
]
