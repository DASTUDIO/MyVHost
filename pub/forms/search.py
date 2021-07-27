from django import forms

class form_search_user(forms.Form):
    userid = forms.CharField()

class form_search_keyword(forms.Form):
    keyword = forms.CharField()