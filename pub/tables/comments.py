from django.db import models
from django.contrib import admin


class user_comments(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.IntegerField()
    publisherid = models.IntegerField()
    content = models.TextField()
    likes = models.IntegerField(default=0)
    created=models.IntegerField()
class user_comments_decoration(admin.ModelAdmin):
    list_display = ('id', 'userid', 'publisherid', 'content', 'likes')
    search_fields = ('id', 'userid', 'publisherid', 'content', 'likes')


class user_comments_likes_map(models.Model):
    comment_id = models.IntegerField()
    publisher = models.IntegerField()
class user_comments_likes_map_decoration(admin.ModelAdmin):
    list_display = ('comment_id', 'publisher')
    search_fields = ('comment_id', 'publisher')

