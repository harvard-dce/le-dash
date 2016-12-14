
from django import template
from datetime import timedelta
import arrow
from arrow.parser import ParserError

register = template.Library()


@register.filter(name='video_length')
def video_length(value):
    td = timedelta(seconds=round(value / 1000.0))
    return str(td)

@register.filter(name='episode_date')
def episode_date(value):
    try:
        return arrow.get(value).format('MMMM DD, YYYY, HH:mm:ss')
    except ParserError:
        return ''

