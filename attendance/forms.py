from django.forms import CharField, ChoiceField
from django.forms import Form


class SeriesForm(Form):
    series_id = CharField(label='series id', max_length=11)
    CHOICES = (
        ('table', 'Table'),
        ('graph', 'Graph'),
    )
    display = ChoiceField(choices=CHOICES, required=True,
                          label='Display', initial='graph')
