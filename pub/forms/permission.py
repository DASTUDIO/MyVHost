from django import forms

class form_permission_readable(forms.Form):
    readable = forms.CharField()

class form_permission_writeable(forms.Form):
    writeable = forms.CharField()

class form_permission_modifiable(forms.Form):
    modifiable = forms.CharField()

class form_permission_token(forms.Form):
    token = forms.CharField()