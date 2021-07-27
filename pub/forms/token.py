# coding=utf-8

from django import forms

class form_token(forms.Form):
    token = forms.CharField()