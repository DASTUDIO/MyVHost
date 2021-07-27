# coding=utf-8

import pub.response.error as error
import pub.settings as s

import pub.tables.resources as resource
import pub.forms.add as kv
import pub.functions.token as token
import pub.permission.resource as verify
import pub.response.json as j
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import pub.tables.user as user
import pub.tables.map.domain as d
import pub.response.wrap as w

from urllib.parse import urlparse
from socket import gethostbyname
import pub.permission.decorator as permission

import pub.permission.user as user_permission

@permission.require_login
def verify_key(request,floder,key):

    if not key:
        return j.dic({'error':'未填写URL'},'utf-8')

    if(verify.is_valid_key(key,-1)):
        return j.dic({"valid":"可用的URL"},'utf-8')
    else:
        return __error_key_already_exist(request)

@permission.require_login
def verify_domain(request,folder,key):
    try:
        userid = request.session.get('userid')

        key = 'http://'+ key

        domain = str(urlparse(key).hostname)

        ip = str(gethostbyname(domain))

        if ip in s.IP:
            try:
                d.domain_to_key.objects.get(domain=domain, url=key[len(domain)+8:])
                return j.dic({'error':'已存在记录'},'utf-8')
            except:
                try:

                    res = d.domain_to_user.objects.get(domain=domain, user=userid)

                    if not res.token == '':

                        _domain = 'http://' + res.token + '.' + domain

                        domain = str(urlparse(_domain).hostname)

                        ip = str(gethostbyname(domain))

                        if ip == s.DOMAIN_VERIFY_IP:

                            res.token = ''

                            res.save()

                            return j.dic({'success':'可以使用'},'utf-8')
                        else:
                            return j.err('请将'+res.token+'.'+res.domain+'以CNAME方式解析至verify.本服务器完成所有权验证','utf-8')
                    else:
                        return j.dic({'success':'可以使用'},'utf-8')

                except:
                    return j.err("已解析，但未绑定至当前用户. <a href='/bind_domain/' target='_blank'>去绑定</a>",'utf-8')
        return j.err('请将该域名CNAME解析至本服务器','utf-8')
    except:
        return j.err('请将该域名CNAME解析至本服务器','utf-8')

@permission.require_login
def bind_domain(r,f,p):
    return w.page(r,'bind-domain.html',{'token':str(token.alpha_token(15))})

@permission.require_login
def do_bind_domain(r,f,p):
    if not r.POST:
        return j.dic({'error': '无效的参数'}, 'utf-8')

    form_data = kv.form_bind_domain(r.POST)

    if not form_data.is_valid():
        return j.dic({'error':'无效的参数'},'utf-8')

    _domain = form_data.cleaned_data['domain']

    _user =  r.session.get('userid')

    _token = form_data.cleaned_data['token']

    try:
        res = d.domain_to_user.objects.get(domain=_domain)
        if res.token == '':
            return j.err('该域名已经被绑定过','utf-8')
        else:
            res.delete()
            raise Exception()
    except:

        try:

            record = d.domain_to_user.objects.create(domain=_domain, user=_user, token=_token)

            _domain = 'http://' + _token + '.' + _domain

            domain = str(urlparse(_domain).hostname)

            ip = str(gethostbyname(domain))

            if ip == s.DOMAIN_VERIFY_IP:
                record.token = ''
                record.save()
                return j.dic({'success':'绑定成功'},'utf-8')

            return j.dic({'error':'提交成功，解析尚未生效请稍等一段时间'},'utf-8')

        except:
            return j.dic({'error':'提交成功，解析尚未生效请稍等一段时间'},'utf-8')

def __error_key_already_exist(request):

    return j.dic({'error':'已存在该URL'},'utf-8')

