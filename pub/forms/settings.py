# coding=utf-8

from django import forms

class form_settings_profile(forms.Form):

    real_name = forms.CharField()
    id_code = forms.CharField()
    phone = forms.CharField()
    email = forms.CharField()

    position = forms.CharField()
    friend_url = forms.CharField()
    brief = forms.CharField()