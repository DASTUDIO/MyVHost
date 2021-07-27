# coding=utf-8
import pub.response.error as error
import pub.settings as s
import os
import time
import json
import pub.tables.resources as resource
import pub.forms.add as kv
import pub.functions.token as token
import pub.permission.resource as verify
import pub.response.json as j

import pub.tables.map.domain as d

import pub.permission.decorator as permission
from pub.forms.permission import form_permission_readable,form_permission_token

import pub.permission.resource as r_permission

@permission.require_login
def add_resource_link(r,f,p):

    if not verify.can_create(r,s.RESOURCE_TYPE_SHORT_LINK):
        return j.dic({'error': '没有权限执行此操作'},'utf-8')

    try:
        if r.method != 'POST':
            return j.dic({'error':'无效的参数'},'utf-8')
        form = kv.form_resource_short_link(r.POST)

        if not form.is_valid():
            return j.dic({'error':'无效的参数'},'utf-8')

        key = form.cleaned_data['key']
        value = form.cleaned_data['value']

        if not verify.is_valid_key(key,s.RESOURCE_TYPE_SHORT_LINK):
            return j.dic({'error':'已存在该URL'},'utf-8')

        # permission form
        f_read = form_permission_readable(r.POST)
        f_token = form_permission_token(r.POST)

        if not f_read.is_valid():
            return j.dic({'error': '没有配置权限信息'}, 'utf-8')

        _token = ''

        if f_token.is_valid():
            _token = f_token.cleaned_data['token']

        # record
        resource.resource_type.objects.create(key=key, type=s.RESOURCE_TYPE_SHORT_LINK)
        resource.resource_link.objects.create(key=key, value=value)

        # owner
        userid = r.session.get('userid')
        resource.resource_to_user.objects.create(key=key, userid=userid)

        verify.did_create(r,s.RESOURCE_TYPE_SHORT_LINK)

        # permission
        verify.set_permission(key=key,
                              readable=f_read.cleaned_data['readable'],
                              writeable=s.ACCESSIBILITY_PRIVATE,
                              modifiable=s.ACCESSIBILITY_PRIVATE,
                              token=_token)

        # domain
        hasDomain = kv.form_resource_domain(r.POST)

        if hasDomain.is_valid():
            domain = hasDomain.cleaned_data['domain']
            url = ""
            try:
                devide = domain.index("/")
                url = domain[devide + 1:]
                domain = domain[0:devide]
            except:
                pass

            d.domain_to_key.objects.create(key=key, url=url, domain=domain)

        return j.dic({'success':'success'})
    except:
        return j.dic({'error':'已存在该URL'},'utf-8')