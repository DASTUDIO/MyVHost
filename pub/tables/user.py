# coding=utf-8
import pub.settings as s
from django.db import models
from django.contrib import admin

provider_list = \
    (
        (s.AUTH_PROVIDER_ALIPAY,'Alipay'),
        (s.AUTH_PROVIDER_WEIXIN,'Weixin'),
        (s.AUTH_PROVIDER_GITHUB,'Github')
    )

permission_type = \
    (
        (s.RESOURCE_TYPE_CUSTOMED,'customed'),
        (s.RESOURCE_TYPE_TEMPLATED,'templated'),
        (s.RESOURCE_TYPE_RESTFUL_API,'api'),
        (s.RESOURCE_TYPE_IFRAME,'iframe'),
        (s.RESOURCE_TYPE_SHORT_LINK,'link')
    )

# 第三方认证用户
class auth_user(models.Model):
    id = models.AutoField(primary_key=True)
    openid = models.TextField(null=False)
    nickname = models.TextField(null=False)
    headimg = models.TextField(null=False)
    authprovider = models.IntegerField(choices=provider_list,null=False)
    balance = models.FloatField(null=True,blank=True)
class auth_user_decoration(admin.ModelAdmin):
    list_display = ('id','nickname','authprovider','openid','balance')
    search_fields = ('id','nickname','authprovider','openid','balance')

# 用户创建资源权限
class user_permission(models.Model):
    user_id = models.IntegerField(null=False)
    type = models.IntegerField(choices=permission_type,default=s.RESOURCE_TYPE_CUSTOMED)
    volume = models.IntegerField()
class user_permission_decoration(admin.ModelAdmin):
    list_display = ('user_id','type','volume')
    search_fields = ('user_id','type','volume')


# 名片信息
class user_info(models.Model):

    # auth_user id
    userid = models.IntegerField(unique=True)

    # 职位
    position = models.TextField()
    # 活跃度
    active = models.IntegerField()
    # 好友链接
    friend_url = models.TextField()
    # 简介
    brief = models.TextField()

    # 真名
    real_name = models.TextField()
    # 身份证号
    id_code = models.TextField()
    # 手机
    phone = models.TextField()
    # 邮箱
    email = models.TextField()


class user_info_decoration(admin.ModelAdmin):
    list_display = ('userid', 'position', 'active', 'brief', 'friend_url', 'real_name', 'id_code', 'phone', 'email')
    search_fields = ('userid', 'position', 'active', 'brief', 'friend_url')

