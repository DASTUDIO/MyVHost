# coding=utf-8
import pub.settings as s
from django.db import models
from django.contrib import admin

cache_type =\
    (
        (s.CACHE_TYPE_LOGIN, 'Login'),
        (s.CACHE_TYPE_TOKEN, 'Token')
    )

class cache_suspend(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField(choices=cache_type,null=False)
    key = models.TextField(null=False)
    value = models.TextField()
class cache_suspend_decoration(admin.ModelAdmin):
    list_display = ('id','type','key','value')
    search_fields = ('id','type','key','value')