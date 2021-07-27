# coding=utf-8
from django import forms as f

class reg(f.Form):
    username = f.CharField()
    password = f.CharField()
    phone = f.CharField()