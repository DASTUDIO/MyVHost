from django import forms


class form_card_title(forms.Form):
    title = forms.CharField()

class form_card_brief(forms.Form):
    brief = forms.CharField()

class form_card_headimg(forms.Form):
    icon = forms.CharField()