#coding=utf-8

import pub.response.error as e
import pub.settings as settings
import pub.response.wrap as wrap

from pub.tables.resources import *



import pub.permission.resource as permission

from pub.forms.token import form_token

def get_templated(request, url_key):

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
        return e.page(request, 400, '您需要权限来访问此页面', url_key)

    # dispatch
    try:
        r = resource_templated.objects.get(key=url_key)

        source = r.source

        api = r.api

        s = resource_customed.objects.get(key=source)

        path = s.path

        params = {'api':api}

        return wrap.raw_page(request, path, params)

    except Exception as ee:

        if settings.RELEASE:
            resource_templated.objects.filter(key=url_key).delete()

        return e.page(request, 404,'找不到该资源',url_key+str(ee) if not settings.RELEASE else '')
