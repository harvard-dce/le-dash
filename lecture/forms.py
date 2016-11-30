from django.forms import CharField
from django.forms import Form


class MpidForm(Form):
    mpid = CharField(label='media package id', max_length=36)
