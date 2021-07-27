from django import forms

class sms_code(forms.Form):
    code = forms.CharField()