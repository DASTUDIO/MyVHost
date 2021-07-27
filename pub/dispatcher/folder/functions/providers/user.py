# coding=utf-8

import time
import pub.response.error as error
import pub.settings as s

import pub.tables.resources as resource
import pub.tables.template as template
import pub.tables.comments as comments
import pub.tables.user as user

import pub.response.json as j
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import pub.tables.user as user
import pub.tables.map.domain as d
import pub.response.wrap as w

from pub.forms.search import form_search_keyword,form_search_user
from pub.forms.user_comments import form_comments,form_comments_page,form_add_comment

import pub.permission.user as p_user


# User Provider
def user_provider(request,folder,userid):
    try:
        data = {}
        res = user.auth_user.objects.get(id=userid)
        data['u_nickname'] = res.nickname
        data['u_headimg'] = res.headimg
        data['u_id'] = res.id


        info_res = user.user_info.objects.get(userid=userid)
        data['brief'] = info_res.brief
        data['position'] = info_res.position
        data['friend_url'] = info_res.friend_url
        data['active'] = info_res.active

        return w.page(request,'user.html',data)
    except Exception as e:
        return error.page(request, 404, "该人无法显示", "该名片还未开通" if s.RELEASE else "该名片还未开通"+str(e))
