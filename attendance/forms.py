from django.forms import CharField
from django.forms import Form


class SeriesForm(Form):
    series_id = CharField(label='series id', max_length=11)
