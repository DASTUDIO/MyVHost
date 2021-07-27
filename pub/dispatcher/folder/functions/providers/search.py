# coding=utf-8

import time
import pub.response.error as error
import pub.settings as s

import pub.tables.resources as resource
import pub.tables.template as template
import pub.tables.comments as comments
import pub.tables.user as user

import pub.response.json as j
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import pub.tables.user as user
import pub.tables.map.domain as d
import pub.response.wrap as w

from pub.forms.search import form_search_keyword,form_search_user
from pub.forms.user_comments import form_comments,form_comments_page,form_add_comment

import pub.permission.user as p_user



# Search Provider
def search_provider(r,f,p):

    if r.GET or r.POST:
        if r.GET:
            request_content = r.GET
        else:
            request_content = r.POST

        f_user = form_search_user(request_content)

        f_keyword = form_search_keyword(request_content)

        result = []

        if f_user.is_valid():
            # user stuff
            res = resource.resource_to_user.objects.filter(userid=f_user.cleaned_data['userid'])
            for item in reversed(res):
                try:
                    r = resource.resource_info.objects.get(key=item.key)
                    result.append({
                        'title': __fix_row(r.title),
                        'brief': __fix_row(r.brief),
                        'headimg': r.headimg,
                        'url': '/' + r.key,
                        'key': r.key
                    })
                except:
                    pass
                try:
                    t = template.template_info.objects.get(key=item.key)
                    result.append({
                        'title': __fix_row(t.title),
                        'brief': __fix_row(t.brief),
                        'headimg': t.headimg,
                        'url': '/template/' + t.key,
                        'key': t.key
                    })
                except:
                    pass

        elif f_keyword.is_valid():
            keyword = f_keyword.cleaned_data['keyword']

            res = resource.resource_info.objects.filter(title__icontains=keyword)
            for item in reversed(res):
                it={
                    'title': __fix_row(item.title),
                    'brief': __fix_row(item.brief),
                    'headimg': item.headimg,
                    'url': '/' + item.key,
                    'key': item.key
                }

                try:
                    userid = resource.resource_to_user.objects.get(key=item.key).userid
                    user_headimg = user.auth_user.objects.get(id=userid).headimg
                    it['user_link'] = '/user/'+str(userid)
                    it['user_headimg'] = user_headimg
                except:
                    pass

                result.append(it)

            res = template.template_info.objects.filter(title__icontains=keyword)

            for item in reversed(res):
                it = {
                    'title': __fix_row(item.title),
                    'brief': __fix_row(item.brief),
                    'headimg': item.headimg,
                    'url': '/template/' + item.key,
                    'key': item.key
                }

                try:
                    userid = resource.resource_to_user.objects.get(key=item.key).userid
                    user_headimg = user.auth_user.objects.get(id=userid).headimg
                    it['user_link'] = '/user/'+str(userid)
                    it['user_headimg'] = user_headimg
                except:
                    pass

                result.append(it)

        else:
            return j.dic({'error': '参数不正确2'}, 'utf-8')

        return j.dic({'success': result}, 'utf-8')
    else:
        return j.dic({'error': '无参数'}, 'utf-8')
#解决前端 像 qwerqwreqwerqwer 这样的 没有分词的英文 不换行的问题
def __fix_row(content):
    if len(content) > s.CARD_ROW_LENGTH and content.encode('UTF-8').isalpha() and content.find(' ') == -1:
        return content[0:s.CARD_ROW_LENGTH] + '...'
    return content
