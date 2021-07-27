#coding=utf-8

import pub.response.error as e
import pub.settings as settings
import pub.response.wrap as wrap

from pub.tables.resources import *

import pub.permission.resource as permission

from pub.forms.token import form_token

def get_customed(request, url_key):

    # permission
    token = ''
    if request.GET or request.POST:
        if request.GET:
            request_content = request.GET
        else:
            request_content = request.POST
        tk = form_token(request_content)

        if tk.is_valid():
            token = tk.cleaned_data['token']

    if not permission.can_read(request, url_key, token):
        return wrap.page(request, 'error_crypto.html')

    # dispatch
    try:
        resource = resource_customed.objects.get(key=url_key)

        path = resource.path

        return wrap.raw_page(request, path)
    except:
        if settings.RELEASE:
            resource_type.objects.filter(key=url_key).delete()

        return e.page(request,404, '找不到该资源 ', 'resource not found db:'if not settings.RELEASE else '' +'\'' + path + '\'')


