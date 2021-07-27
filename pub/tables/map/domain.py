# coding=utf-8
from django.db import models
from django.contrib import admin


class domain_to_key(models.Model):
    domain = models.TextField(null=False)
    url = models.TextField(null=False) # 域名后的目录解析
    key = models.TextField(null=False)
class domain_to_key_decoration(admin.ModelAdmin):
    list_display = ('domain','url','key')
    search_fields = ('domain','url','key')

class domain_to_user(models.Model):
    domain = models.TextField(unique=True)
    user = models.IntegerField(default=-1)
    token = models.TextField()
class domain_to_user_decoration(admin.ModelAdmin):
    list_display = ('domain','user')
    search_fields = ('domain','user')
