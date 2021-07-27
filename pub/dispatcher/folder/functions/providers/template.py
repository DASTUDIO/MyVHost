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


# Template Provider
def template_provider(page):
    try:
        data = {'state':'error'}
        res = template.template_info.objects.all()
        pag = Paginator(res,s.TEMPLATE_PAGE_SIZE)
        data['volume'] = pag.count

        try:
            contents = pag.page(page)
        except PageNotAnInteger:
            contents = pag.page(1)
        except EmptyPage:
            contents = pag.page(pag.num_pages)
        data['content'] = []

        for item in contents:

            # fetch
            u_res = resource.resource_to_user.objects.get(key=item.key)

            userid = u_res.userid

            # fetch
            u_info = user.auth_user.objects.get(id=userid)

            nickname = u_info.nickname

            user_link = "/user/" + str(userid)

            it = {'title': __fix_row(item.title),
                  'brief': __fix_row(item.brief),
                  'headimg': item.headimg,
                  'key': item.key,

                  'user_link' : user_link,
                  'nickname': nickname,
                  }

            try:
                it['domain'] = d.domain_to_key.objects.get(key=item.key).domain
            except:
                pass

            data['content'].append(it)

        data['state'] = 'success'
        return j.dic(data,'utf-8')
    except Exception as e:
        return j.err('' if s.RELEASE else e)
#解决前端 像 qwerqwreqwerqwer 这样的 没有分词的英文 不换行的问题
def __fix_row(content):
    if len(content) > s.CARD_ROW_LENGTH and content.encode('UTF-8').isalpha() and content.find(' ') == -1:
        return content[0:s.CARD_ROW_LENGTH] + '...'
    return content