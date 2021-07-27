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

from pub.forms.permission import form_permission_modifiable,form_permission_readable,form_permission_token,form_permission_writeable

import pub.tables.map.domain as d

import pub.permission.decorator as permission



#@permission.require_login
def add_resource_restful(r,f,p):

    if not verify.can_create(r,s.RESOURCE_TYPE_RESTFUL_API):
        return j.dic({'error': '没有权限执行此操作'}, 'utf-8')

    try:
        if r.method != 'POST':
            return j.dic({'error': '无效的参数'}, 'utf-8')
        form = kv.form_resource_resuful(r.POST)

        if not form.is_valid():
            return j.dic({'error': '无效的参数'}, 'utf-8')


        key = form.cleaned_data['key']

        xparams = form.cleaned_data['params']


        if key in s.RESOURCE_PROTECTION_KEY:
            raise Exception( 'url: ' + key + ' is protected.')

        if not verify.is_valid_key(r,s.RESOURCE_TYPE_RESTFUL_API):
            return j.dic({'error': '已存在该URL'}, 'utf-8')

        # permissions record
        f_read = form_permission_readable(r.POST)
        f_write = form_permission_writeable(r.POST)
        f_modify = form_permission_modifiable(r.POST)
        f_token = form_permission_token(r.POST)

        if not (f_read.is_valid() and f_write.is_valid() and f_modify.is_valid()):
            return j.dic({'error': '没有配置权限信息'}, 'utf-8')

        _token = ''

        if f_token.is_valid():
            _token = f_token.cleaned_data['token']

        resource.resource_permission.objects.create(key=key,
                                                    readable=f_read.cleaned_data['readable'],
                                                    writeable=f_write.cleaned_data['writeable'],
                                                    modifiable=f_modify.cleaned_data['modifiable'],
                                                    token=_token)

        # resource record
        resource.resource_type.objects.create(key=key, type=s.RESOURCE_TYPE_RESTFUL_API)
        resource.resource_restful.objects.create(key=key)

        # owner record
        userid = r.session.get('userid')
        resource.resource_to_user.objects.create(key=key, userid=userid)


        if xparams !='':

            try:
                json_dic = json.loads(str(xparams))
            except:
                raise Exception('params error : params json excepted')

            for item,value in json_dic.items():
                try:
                    i = resource.resource_restful_item.objects.filter(key=key,item=item)
                    if len(i)==0:
                        raise Exception()

                    i[0].item = item
                    i[0].value = value
                    i[0].save()
                except:
                    resource.resource_restful_item.objects.create(key=key, item=item, value=value)

        verify.did_create(r,s.RESOURCE_TYPE_RESTFUL_API)

        return j.dic({'success': 'success'})

    except Exception as e:

        return j.dic({'error': '' if s.RELEASE else str(e)},'utf-8')
