# coding=utf-8

from django import forms


class form_resource_iframe(forms.Form):
    key = forms.CharField()
    value = forms.CharField()
    #title = forms.CharField()

class form_resource_short_link(forms.Form):
    key = forms.CharField()
    value = forms.CharField()

class form_resource_custom_page(forms.Form):
    key = forms.CharField()
    html = forms.CharField()
class form_resource_custom_is_template(forms.Form):
    template = forms.CharField()
    api = forms.CharField()

class form_resource_template_page(forms.Form):
    key = forms.CharField()
    source = forms.CharField()
    api = forms.CharField()

class form_resource_resuful(forms.Form):
    key = forms.CharField()
    params = forms.CharField()

class form_resource_info(forms.Form):
    key = forms.CharField()
    title = forms.CharField()
    brief = forms.CharField()
    headimg = forms.CharField()

class form_resource_domain(forms.Form):
    domain = forms.CharField()

class form_resource_pdf(forms.Form):
    key = forms.CharField()
    path =forms.CharField()
    title = forms.CharField()
    msg = forms.CharField()

class form_bind_domain(forms.Form):
    domain = forms.CharField()
    token = forms.CharField()


# permission
class form_resource_readable(forms.Form):
    readable = forms.CharField()

class form_resource_writeable(forms.Form):
    writeable = forms.CharField()

class form_resource_modifable(forms.Form):
    modifiable = forms.CharField()

