# coding=utf-8
import pub.dispatcher.file.file as file

from .functions.pages import *
#from .functions.provider import *
from .functions.providers.content import content_provider
from .functions.providers.template import template_provider
from .functions.providers.search import search_provider
from .functions.providers.user import user_provider
from .functions.providers.comment import user_comment_provider,user_comment_add,user_comment_delete,user_comment_likes_add

from .functions.ajax import *

from .functions.add_custom import add_resource_custom
from .functions.add_template import add_resource_templated
from .functions.add_link import add_resource_link
from .functions.add_restful import add_resource_restful
from .functions.add_iframe import add_resource_iframe
from .functions.settings import settings_set_profile
from .functions.search import search
from .functions.delete import delete_resource

import pub.response.wrap as wrapper
import pub.client.login as login
import pub.client.auth_handler as auth_handler
import pub.client.auth_url_handler as auth_url_handler
import pub.settings as s
import pub.client.auth.weixin as wx
import pub.client.auth.alipay as alipay
import pub.client.auth.github as github

from pub.functions.sms import send_verification

from pub.functions.token import digit_token


from django.shortcuts import render,HttpResponse
# 名片显示人（可选是否显示） 、 扫码刷脸，有效冗余检测、安全密码、手机绑定
def wx_ck(r,f,p):
    signature = r.GET.get('signature')
    timestamp = r.GET.get('timestamp')
    nonce = r.GET.get('nonce')
    echostr = r.GET.get('echostr')
    token = "abcd"  # 请按照公众平台官网\基本配置中信息填写
    return HttpResponse(echostr)

map = {}

def cast(url_key, path):
    global map
    map.update({url_key:path})

try:
    from .cache import do
    do()
except:
    pass
finally:
    cast('weixin2', wx_ck)
    cast(s.UPLOAD_URL, lambda request, folder, post_url: file.upload(request, post_url))
    cast('af', add_resource_iframe)
    cast('al', add_resource_link)
    cast('ac', add_resource_custom)
    cast('at', add_resource_templated)
    cast('aap', add_resource_restful)
    cast('ap', add_pdf)

    cast('api', add_api)
    cast('url', add_link)
    cast('add', add_page)
    cast('addc', add_page_code )
    cast('console', add_console)
    cast('src', add_template)

    #cast('pdf',add_pdf)
    #cast('api_comment',add_comment_api)

    # 微名片
    cast('profile', setting_profile)
    cast('save_profile',settings_set_profile)


    cast('index', lambda r, f, p: wrapper.page(r, 'news.html'))
    cast('settings',lambda  r,f,p:wrapper.page(r,'settings.html'))

    cast('login', login.login)
    cast('logout',login.logout)

    # auth
    cast('auth_img',auth_handler.get_auth_url)
    cast('auth',auth_url_handler.handler)
    # cast('auth_github',github.handle_callback)
    # cast('auth_wx',wx.get_code_callback)
    # cast('auth_alipay', alipay.get_code_callback)

    cast('my_header',lambda  r,f,p:j.dic({'useragent':r.META['HTTP_USER_AGENT']}))

    # providers
    cast('user', user_provider)
    cast('search_provider', search_provider)
    cast('content_provider', lambda r,f,p:content_provider(r.GET.get('page')))
    cast('template_provider', lambda r,f,p:template_provider(r.GET.get('page')))


    cast('user_comment_provider', user_comment_provider)
    cast('user_comment_add', user_comment_add)

    cast('user_comment_likes_add', user_comment_likes_add)
    cast('user_comment_delete', user_comment_delete)


    cast('url_verify',verify_key)
    cast('domain_verify',verify_domain)

    cast('page_preview',lambda r,f,p:wrapper.page(r,'page_preview.html'))

    cast('template_page', lambda r,f,p:wrapper.template_raw_page(r, p))
    cast('template',lambda r, f, p: wrapper.template_wrapper(r, p))


    cast('bind_domain',bind_domain)
    cast('do_bind_domain',do_bind_domain)

    cast('search', search)

    #cast('533422123455553342213551',emergency_code)
    cast('page', lambda  r,f,p:wrapper.page(r,p))

    cast('del',delete_resource)

    cast('tsms', lambda r,f,p:j.err(send_verification('18201995520',str(digit_token(6)),'utf-8')))



def dispatch(request,folder,post_url):

    try:
        return map[folder](request, folder, post_url)
    except Exception as ee:
        msg = '' if s.RELEASE else str(ee)
        return error.page(request, 404, '无效的URL', '' if s.RELEASE else 'WRONG FOLDER : /' + folder + '/' + post_url + ':' + msg)

