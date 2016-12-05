
from django import template
from datetime import timedelta

register = template.Library()


@register.filter(name='video_length')
def video_length(value):
    td = timedelta(seconds=round(value / 1000.0))
    return str(td)
