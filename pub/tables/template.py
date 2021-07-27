from django.db import models
from django.contrib import admin


class template_info(models.Model):
    key = models.TextField(primary_key=True)
    title = models.TextField()
    brief = models.TextField()
    headimg = models.TextField()
    default = models.TextField()

    created = models.IntegerField()
    modified = models.IntegerField()

    class Meta:
        ordering = ('-created',)
class template_info_decoration(admin.ModelAdmin):
    list_display = ('key','title','brief','headimg','default' )
    search_fields =  ('key','title','brief','headimg','default')