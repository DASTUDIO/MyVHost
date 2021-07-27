#coding=utf-8

import pub.response.error as e
import pub.settings as settings

from pub.tables.resources import *

from pub.dispatcher.resource.functions.tools import resource_functions_crypto,resource_functions_token
from pub.dispatcher.resource.functions.customed import get_customed
from pub.dispatcher.resource.functions.templated import get_templated
from pub.dispatcher.resource.functions.iframe import get_iframe
from pub.dispatcher.resource.functions.link import get_short_link
from pub.dispatcher.resource.functions.restful import get_restful_api

import pub.client.auth.github as github

import pub.permission.resource as permission

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
    cast('token', resource_functions_token)
    cast('crypto',resource_functions_crypto)
    cast('auth_github',github.handle_callback)

def dispatch(request,url_key):

    try:                                                        # 为了测试表里的函数能不能用
        if url_key in map:
            return map[url_key](request, url_key)
        else:
            raise LookupError('key not register')               # 为了跳到except里
    except:
        try:
            _type = resource_type.objects.get(key=url_key).type

            # permission
            #if not permission.can_read(request,url_key):
                #return e.page(request, 400 ,'您需要权限来访问此页面', url_key + '->' + _type)

            # dispatch
            if _type == s.RESOURCE_TYPE_CUSTOMED:
                return get_customed(request, url_key)

            if _type == s.RESOURCE_TYPE_TEMPLATED:
                return get_templated(request, url_key)

            if _type == s.RESOURCE_TYPE_RESTFUL_API:
                return get_restful_api(request, url_key)

            if _type == s.RESOURCE_TYPE_SHORT_LINK:
                return get_short_link(request, url_key)

            if _type == s.RESOURCE_TYPE_IFRAME:
                return get_iframe(request, url_key)

            return e.page(request, 404 ,'未知的页面类型', url_key + '->' + _type)
        except:
            return e.page(request, 404,'无效的URL','WRONG RESOURCE' if not settings.RELEASE else '' + url_key)




