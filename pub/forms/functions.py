# coding=utf-8
from django import forms


class functions_resource_token(forms.Form):
    type = forms.CharField()
    length = forms.IntegerField()

class functions_resource_crypto(forms.Form):
    act = forms.CharField()
    data = forms.CharField()

class functions_resource_crypto_pwd(forms.Form):
    password = forms.CharField()

class functions_resource_crypto_noise(forms.Form):
    noise = forms.CharField()

class functions_resource_crypto_digit(forms.Form):
    digit = forms.CharField()
