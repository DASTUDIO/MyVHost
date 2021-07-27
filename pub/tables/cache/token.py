# coding=utf-8
from django.db import models
from django.contrib import admin

class token(models.Model):
    key = models.TextField(unique=True)
    value = models.TextField()
class token_decoration(admin.ModelAdmin):
    list_display = ('key','value')
    search_fields = ('key','value')