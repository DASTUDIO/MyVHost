# coding=utf-8
from django import forms

class api_query(forms.Form):
    act = forms.CharField()

class api_key(forms.Form):
    key = forms.CharField()

class api_value(forms.Form):
    value = forms.CharField()

class api_token(forms.Form):
    token = forms.CharField()

class api_callback(forms.Form):
    callback = forms.CharField();