from django import forms

class form_comments(forms.Form):
    userid = forms.CharField()

class form_comments_page(forms.Form):
    page = forms.CharField()

class form_add_comment(forms.Form):
    userid = forms.CharField()
    content = forms.CharField()