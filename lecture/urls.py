
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='lecture-index'),
    url(r'^(?P<mpid>[\w\-]{36})/$', views.lecture, name='lecture'),
    url(r'^data/(?P<mpid>[\w\-]{36})/$', views.data, name='lecture-data'),
    url(r'^histogram/(?P<mpid>[\w\-]{36})/$', views.histogram,
        name='lecture-histogram'),
]
