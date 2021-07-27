# coding=utf-8
from django.db import models
from django.contrib import admin

# 放在哪里
class file_key_to_path(models.Model):
    key = models.TextField(unique=True)
    path = models.TextField(null=False)
    resource_key = models.TextField(null=False)
    reference = models.IntegerField(default=1)                      # 文件被哈希共享的次数 用于删除某用户的引用时减1
class file_key_to_path_decoration(admin.ModelAdmin):
    list_display = ('key', 'path', 'resource_key', 'reference')
    search_fields = ('key', 'path', 'resource_key', 'reference')

# 谁的文件
class file_key_to_user(models.Model):
    key = models.TextField(unique=True)
    userid = models.IntegerField(null=False)
class file_key_to_user_decoration(admin.ModelAdmin):
    list_display = ('key','userid')
    search_fields = ('key','userid')

# 重复利用
class file_hash_to_key(models.Model):
    hash = models.TextField(unique=True)
    key = models.TextField(null=False)
    reference = models.IntegerField(default=0)
class file_hash_to_key_decoration(admin.ModelAdmin):
    list_display = ('hash', 'key', 'reference')
    search_fields = ('hash', 'key', 'reference')
