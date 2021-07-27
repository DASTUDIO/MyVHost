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

import pub.permission.resource as r_permission

from pub.permission.user import has_domain

from pub.forms.permission import form_permission_readable,form_permission_token

@permission.require_login
def add_resource_templated(r,f,p):

    if not verify.can_create(r,s.RESOURCE_TYPE_TEMPLATED):
        return j.dic({'error': '没有权限执行此操作'},'utf-8')

    # POST verify
    try:
        if r.method != 'POST':
            return j.dic({'error': '无效的参数'},'utf-8')
        form = kv.form_resource_template_page(r.POST)

        if not form.is_valid():
            return j.dic({'error': '无效的参数'},'utf-8')

        # key source api form
        key = form.cleaned_data['key']
        source = form.cleaned_data['source']
        api = form.cleaned_data['api']

        if not api[0:5] == "https":
            return j.dic({'error': 'api必须为https协议url'}, 'utf-8')

        if not verify.is_valid_key(key, s.RESOURCE_TYPE_TEMPLATED):
            return j.dic({'error': '已存在该URL'}, 'utf-8')

        # domain form
        hasDomain = kv.form_resource_domain(r.POST)

        d_domain = ""
        d_url = ""
        if hasDomain.is_valid():
            d_domain = hasDomain.cleaned_data['domain']

            try:
                devide = d_domain.index("/")
                d_url = d_domain[devide + 1:]
                d_domain = d_domain[0:devide]
            except:
                pass
            finally:
                if not (has_domain(r, d_domain)):
                    return j.dic({'error': '该域名未与当前用户绑定，若已绑定请稍后再试'}, 'utf-8')

        # permission form
        f_read = form_permission_readable(r.POST)
        f_token = form_permission_token(r.POST)

        if not f_read.is_valid():
            return j.dic({'error': '没有配置权限信息'}, 'utf-8')

        _token = ''

        if f_token.is_valid():
            _token = f_token.cleaned_data['token']


        # resource record
        resource.resource_type.objects.create(key=key, type=s.RESOURCE_TYPE_TEMPLATED)
        resource.resource_templated.objects.create(key=key, source=source,api=api)

        # owner record
        userid = r.session.get('userid')
        resource.resource_to_user.objects.create(key=key, userid=userid)

        # domain record
        if hasDomain.is_valid():
            try:
                d_res = d.domain_to_key.objects.get(domain=d_domain, url=d_url)
                d_res.delete()
                raise Exception()
            except:
                d.domain_to_key.objects.create(key=key, url=d_url, domain=d_domain)

        # permission record
        verify.set_permission(key=key,
                              readable=f_read.cleaned_data['readable'],
                              writeable=s.ACCESSIBILITY_PRIVATE,
                              modifiable=s.ACCESSIBILITY_PRIVATE,
                              token=_token)

        verify.did_create(r,s.RESOURCE_TYPE_TEMPLATED)
        return j.dic({'success': 'ok'},'utf-8')
    except Exception as e:
        return j.dic({'error': '站内url已被占用'}, 'utf-8')
