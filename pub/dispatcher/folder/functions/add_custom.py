# coding=utf-8

import pub.settings as s
import os
import time
import pub.tables.resources as resource
import pub.tables.template as template

import pub.forms.add as kv
import pub.functions.token as token

import pub.permission.decorator as permission
import pub.permission.resource as verify
from pub.permission.user import has_domain

import pub.response.json as j

import pub.tables.map.domain as d



from pub.forms.card import form_card_brief,form_card_headimg,form_card_title
from pub.forms.permission import form_permission_readable,form_permission_token



@permission.require_login
def add_resource_custom(r,f,p):

    if not verify.can_create(r,s.RESOURCE_TYPE_CUSTOMED):
        return j.dic({'error':'您已达到可最大创建数量，需要增加请充值名额'},'utf-8')

    try:
        # POST verify / key & html
        if r.method != 'POST':
            return j.dic({'error':'无效的参数'},'utf-8')

        form = kv.form_resource_custom_page(r.POST)

        if not form.is_valid():
            return j.dic({'error':'无效的参数'},'utf-8')

        # key & html form
        key = form.cleaned_data['key']
        html = form.cleaned_data['html']
        if not verify.is_valid_key(key,s.RESOURCE_TYPE_CUSTOMED):
            return j.dic({'error':'已存在该URL'},'utf-8')

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

                # Debug
                # try:
                #     d.domain_to_key.objects.get(domain=d_domain, url=d_url)
                #     return j.dic({'error': '找到了该域名'}, 'utf-8')
                # except Exception as eee:
                #     return j.dic({'error': str(eee)}, 'utf-8')


        # permission form
        f_read = form_permission_readable(r.POST)
        f_token = form_permission_token(r.POST)

        if not f_read.is_valid():
            return j.dic({'error': '没有配置权限信息'}, 'utf-8')

        _token = ''

        if f_token.is_valid():
            _token = f_token.cleaned_data['token']

        # card form
        f_title = form_card_title(r.POST)
        f_brief = form_card_brief(r.POST)
        f_headimg = form_card_headimg(r.POST)

        card_title = f_title.cleaned_data['title'] if f_title.is_valid() else ''
        card_brief = f_brief.cleaned_data['brief'] if f_brief.is_valid() else ''
        card_icon = f_headimg.cleaned_data['icon'] if f_headimg.is_valid() else ''

        # template form
        isTemplate = kv.form_resource_custom_is_template(r.POST)

        if isTemplate.is_valid():
            if not f_title.is_valid():
                return j.dic({'error': '模板必填卡片信息'}, 'utf-8')


        # write file
        filename = __gen_random_name()
        gen_path = os.path.join(s.CUSTOMED_HTML_PATH,filename)

        file = open(gen_path,'w+',encoding='utf-8')
        file.write(html)
        file.close()

        wrap_path = gen_path[len(s.TEMPLATE_PATH)+1:]

        # resource record
        resource.resource_type.objects.create(key=key, type=s.RESOURCE_TYPE_CUSTOMED)
        resource.resource_customed.objects.create(key=key,path=wrap_path)

        # owner record
        _userid = r.session.get('userid')
        resource.resource_to_user.objects.create(key=key, userid=_userid)

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

        # card record
        try:
            res = resource.resource_info.objects.get(key=key)
            res.delete()
            raise Exception()
        except:
            if f_title.is_valid():
                if not isTemplate.is_valid():
                    resource.resource_info.objects.create(key=key,
                                                          title=card_title,
                                                          brief=card_brief,
                                                          headimg=card_icon,
                                                          created=int(time.time()),
                                                          modified=int(time.time()))
                else:
                    template.template_info.objects.create(key=key,
                                                          title=card_title,
                                                          brief=card_brief,
                                                          headimg=card_icon,
                                                          default=isTemplate.cleaned_data['api'],
                                                          created=int(time.time()),
                                                          modified=int(time.time()))

        # user can create sub 1
        verify.did_create(r, s.RESOURCE_TYPE_CUSTOMED)

        res = {'success': 'success'}

        return j.dic(res, 'utf-8')
    except Exception as ee:
        return j.custom(str(ee), 'utf-8')

def __gen_random_name():
    filename = str(int(time.time())) + token.alpha_token(7)
    if os.path.isfile(os.path.join(s.CUSTOMED_HTML_PATH, filename)):
        return __gen_random_name()
    else:
        return filename
