from django.db import models
from django.contrib import admin

class notice(models.Model):
    title = models.TextField()
    content = models.TextField()
class notice_decoration(admin.ModelAdmin):
    list_display = ('title', 'content')
    search_fields = ('title', 'content')