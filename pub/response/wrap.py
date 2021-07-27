# coding=utf-8
from django.shortcuts import render,HttpResponse
from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect
import pub.settings as settings
import pub.response.error as error
import pub.tables.resources as resource_db
import pub.tables.template as template_db
import pub.strings as strings

from pub.tables.notice import notice

# fit in theme
def page(request, html_file_in_templates, parameters={},theme=settings.THEME):
    try:
        theme = str(theme)
        if theme != '':
            theme = theme + '/'

        parameters['nickname'] = request.session.get('nickname')

        parameters['headimg'] = request.session.get('headimg')

        parameters['userid'] = request.session.get('userid')

        # notice
        res = notice.objects.all() or []
        notice_volume = len(res)
        parameters['volume'] = notice_volume
        parameters['notices'] = {}
        for i in range(notice_volume):
            parameters['notices'][res[i].title] = res[i].content


        return render(request, theme + str(html_file_in_templates), parameters)
    except Exception as e:
        msg = '' if settings.RELEASE else e
        return error.page(request,701,'渲染错误', msg)

# ignore theme / login state / notice
def raw_page(request, html_file_in_templates, parameters={}):
    try:
        return render(request, str(html_file_in_templates), parameters)
    except Exception as e:
        msg = '' if settings.RELEASE else e
        return error.page(request,701,'渲染错误:'+html_file_in_templates,e)

# 带有添加api功能
def template_wrapper(request,key):
    try:
        api = template_db.template_info.objects.get(key=key).default
        data = {}
        data['api'] = api
        data['source'] = key
        data['location'] = strings.HTTP_OR_HTTPS + request.META['HTTP_HOST'] +  "/template_page/" + key
        data['title'] = key
        return render(request,settings.THEME + '/template-wrapper.html',data)
    except Exception as e:
        return error.page(request, 2, " 不存在该模板 "+str(e))


# 原生template
def template_raw_page(request, key):
    try:
        api = template_db.template_info.objects.get(key=key).default
        path = resource_db.resource_customed.objects.get(key=key).path
        return render(request, path, {'api': api})
    except Exception as e:
        return error.page(request, 2, " 不存在该模板 "+str(e))

def agent(request, title, destination_url_with_http_or_https,post_url=''):
    param = {}
    param['title'] = title
    param['location'] = destination_url_with_http_or_https + '/' + post_url
    return render(request,'url_wrapper.html',param)

def jump(url):
    return HttpResponseRedirect(url)             # 302

def jump_permanent(url):
    return HttpResponsePermanentRedirect(url)    # 301