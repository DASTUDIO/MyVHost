# coding=utf-8


from django.db import models
from django.contrib import admin
import pub.settings as s


type_list = \
    (
        (s.RESOURCE_TYPE_CUSTOMED, 'Customed'),
        (s.RESOURCE_TYPE_TEMPLATED, 'Templated'),
        (s.RESOURCE_TYPE_RESTFUL_API, 'Restful API'),
        (s.RESOURCE_TYPE_SHORT_LINK, 'Short Link'),
        (s.RESOURCE_TYPE_IFRAME,'iFrame')
    )

state_list = \
    (
        (s.RESOURCE_STATE_PLAY,'Play'),
        (s.RESOURCE_STATE_PAUSE,'Pause'),
        (s.RESOURCE_STATE_STOP,'Stop'),
        (s.RESOURCE_STATE_PREPARE_TO_DELETE,'Prepare to delete')
    )

accessibility_list = \
    (
        (s.ACCESSIBILITY_PUBLIC, 'Every one'),
        (s.ACCESSIBILITY_LOGIN, 'Logged only'),
        (s.ACCESSIBILITY_PRIVATE, 'Owner only'),
        (s.ACCESSIBILITY_TOKEN, 'Token'),
        (s.ACCESSIBILITY_LOGIN_OR_TOKEN, 'Logged or token')
    )


# Type
class resource_type(models.Model):
    key = models.TextField(unique=True)
    type = models.IntegerField(choices=type_list, default=s.RESOURCE_TYPE_CUSTOMED)
class resource_type_decoration(admin.ModelAdmin):
    list_display = ('key','type')
    search_fields = ('key','type')


# State
class resource_state(models.Model):
    key = models.TextField(unique=True)
    state = models.IntegerField(choices=state_list,default=s.RESOURCE_STATE_PLAY)
class resource_state_decoration(admin.ModelAdmin):
    list_display = ('key','state')
    search_fields = ('key','state')


# Permission
class resource_permission(models.Model):
    key = models.TextField(unique=True)
    readable = models.IntegerField(choices=accessibility_list,default=s.ACCESSIBILITY_PUBLIC)
    writeable = models.IntegerField(choices=accessibility_list,default=s.ACCESSIBILITY_PRIVATE)
    modifiable = models.IntegerField(choices=accessibility_list,default=s.ACCESSIBILITY_PRIVATE)
    permitteduser = models.IntegerField()
    token = models.TextField()
class resource_permission_decoration(admin.ModelAdmin):
    list_display = ('key','readable','writeable','modifiable')
    search_fields = ('key','readable','writeable','modifiable')

# resource customed
class resource_customed(models.Model):
    key = models.TextField(unique=True)                               # url_key
    path = models.TextField(null=False)                               # 保存的html模板的文件名
class resource_customed_decoration(admin.ModelAdmin):
    list_display = ('key','path')
    search_fields = ('key','path')

# template
class template(models.Model):
    key = models.TextField(null=False)  # custom key
    default = models.TextField()
    #price = models.FloatField()
class template_decoration(admin.ModelAdmin):
    list_display = ('key',"default")
    search_fields = ('key',"default")

# resource jump
class resource_link(models.Model):
    key = models.TextField(unique=True)
    value = models.TextField()
class resource_link_decoration(admin.ModelAdmin):
    list_display = ('key','value')
    search_fields = ('key','value')

# resource iframe
class resource_iframe(models.Model):
    key = models.TextField(unique=True)
    value = models.TextField(null=False)
    title = models.TextField()
class resource_iframe_decoration(admin.ModelAdmin):
    list_display = ('key','value','title')
    search_fields = ('key','value','title')

# resource templated
class resource_templated(models.Model):
    key = models.TextField(unique=True)
    source = models.TextField(null=False)      # 另一个custom resource
    api = models.TextField(null=False)
class resource_templated_decoration(admin.ModelAdmin):
    list_display = ('key','source','api')
    search_fields = ('key','source','api')

# resource restful api
class resource_restful(models.Model):
    key = models.TextField(unique=True)
    name = models.TextField()                           # 名称
    volume = models.IntegerField(default=-1)                      # 目前有多少item
    capability = models.IntegerField(default=-1)                  # 能放多少item
    #readable = models.IntegerField(choices=accessibility_list, default=s.ACCESSIBILITY_PUBLIC)
    #writeable = models.IntegerField(choices=accessibility_list, default=s.ACCESSIBILITY_PRIVATE) # if can not modify then add only
    #modifiable = models.IntegerField(choices=accessibility_list, default=s.ACCESSIBILITY_PRIVATE) # del and modify
    token = models.TextField()
class resource_restful_decoration(admin.ModelAdmin):
    list_display = ('key',)
    search_fields = ('key',)
class resource_restful_item(models.Model):
    key = models.TextField(null=False)                  # resource 的 key
    item = models.TextField(null=False)                 # item 的 key
    value = models.TextField()                          # item 的 值
    readable = models.IntegerField(choices=accessibility_list, default=s.ACCESSIBILITY_PUBLIC)
    writeable = models.IntegerField(choices=accessibility_list, default=s.ACCESSIBILITY_PRIVATE)
    modifiable = models.IntegerField(choices=accessibility_list, default=s.ACCESSIBILITY_PRIVATE)
    token = models.TextField()
    owner = models.TextField()                          # logged modify&del
class resource_restful_item_decoration(admin.ModelAdmin):
    list_display = ('key','item','value')
    search_fields = ('key','item','value')

# resource pdf
class resource_pdf(models.Model):
    key = models.TextField(null=False)
    path = models.TextField(null=False)
    title = models.TextField()
    msg = models.TextField()
class resource_pdf_decoration(admin.ModelAdmin):
    list_display = ('key','path','title','msg')
    search_fields = ('key','path','title','msg')

# resource to user
class resource_to_user(models.Model):
    key = models.TextField(unique=True)
    userid = models.IntegerField()
class resource_to_user_decoration(admin.ModelAdmin):
    list_display = ('key','userid')
    search_fields = ('key','userid')

# resource permission
class resource_permission(models.Model):
    key = models.TextField(unique=True)
    readable = models.IntegerField(choices=accessibility_list, default=s.ACCESSIBILITY_PUBLIC)
    writeable = models.IntegerField(choices=accessibility_list, default=s.ACCESSIBILITY_PRIVATE)
    modifiable = models.IntegerField(choices=accessibility_list, default=s.ACCESSIBILITY_PRIVATE)
    token = models.TextField()
class resource_permission_decoration(admin.ModelAdmin):
    list_display = ('key', 'readable', 'writeable', 'modifiable','token')
    search_fields = ('key', 'readable', 'writeable', 'modifiable','token')

# resource info @@@(customed & templated only)
class resource_info(models.Model):
    key = models.TextField(primary_key=True)
    title = models.TextField()
    brief = models.TextField()
    headimg = models.TextField()

    created = models.IntegerField()
    modified = models.IntegerField()

    class Meta:
        ordering = ('-created',)
class resource_info_decoration(admin.ModelAdmin):
    list_display = ('key','title','brief','headimg')
    search_fields =  ('key','title','brief','headimg')