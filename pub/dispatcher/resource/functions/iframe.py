#coding=utf-8

import pub.response.error as e
import pub.settings as settings
import pub.response.wrap as wrap

from pub.tables.resources import *

import pub.permission.resource as permission


def get_iframe(request, url_key):

    # permission
    if not permission.can_read(request, url_key):
        return e.page(request, 400, '您需要权限来访问此页面', url_key)

    try:
        resource = resource_iframe.objects.get(key=url_key)

        title = resource.title

        if title == '':
            title = settings.DEFAULT_IFRAME_TITLE
        location = resource.value

        return wrap.agent(request, title, location)

    except Exception as ee:

        if settings.RELEASE:
            resource_type.objects.filter(key=url_key).delete()

        return e.page(request,404,'找不到该资源',url_key+str(ee) if not settings.RELEASE else '')

