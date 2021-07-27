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



# User Card Comment Provier

def user_comment_provider(r, p, f):

    if r.GET or r.POST:
        if r.GET:
            request_content = r.GET
        else:
            request_content = r.POST

        f_comments = form_comments(request_content)

        if not f_comments.is_valid():
            return j.dic({'error': '参数不正确'}, 'utf-8')

        userid = f_comments.cleaned_data['userid']

        result = []

        res = comments.user_comments.objects.filter(userid=userid).order_by('-created')

        # pages
        _page = 0

        f_pages = form_comments_page(request_content)

        if f_pages.is_valid():
            page=f_pages.cleaned_data['page']
            try:
                _page = int(page)
            except:
                pass

        res = res[_page*3:_page*3+3]

        for item in res:
            it = {
                'id':item.id,
                'content':item.content,
                'likes':item.likes
            }
            try:
                user_res = user.auth_user.objects.get(id=item.publisherid)
                user_nickname = user_res.nickname
                user_headimg = user_res.headimg
                it['user_link'] = '/user/' + str(item.publisherid)
                it['user_headimg'] = user_headimg
                it['user_nickname'] = user_nickname

                user_info_res = user.user_info.objects.get(userid=item.publisherid)
                it['user_position'] = user_info_res.position
            except:
                pass

            result.append(it)

        return j.dic({'success': result}, 'utf-8')

    else:
        return j.dic({'error': '无参数'}, 'utf-8')

def user_comment_add(r, f, p):

    if not p_user.is_logged(r):
        return j.dic({'error': '需要登录才可以留言'}, 'utf-8')

    publisherid = r.session.get('userid')

    if r.GET or r.POST:
        if r.GET:
            request_content = r.GET
        else:
            request_content = r.POST

        # 获取参数

        f_add_commenet = form_add_comment(request_content)

        if not f_add_commenet.is_valid():
            return j.dic({'error': '参数不正确'}, 'utf-8')

        userid = f_add_commenet.cleaned_data['userid']


        content = f_add_commenet.cleaned_data['content']

        # 用户是否有效

        try:
            user.auth_user.objects.get(id=userid)
        except:
            return j.dic({'error': '该用户不存在'}, 'utf-8')

        # 添加

        comments.user_comments.objects.create(userid=userid,
                                publisherid=publisherid,
                                content=content,
                                created=int(time.time()))

        return j.dic({'success': 'ok'}, 'utf-8')
    else:
        return j.dic({'error': '无参数'}, 'utf-8')


def user_comment_likes_add(r,f,p):

    if not p_user.is_logged(r):
        return j.dic({'error': '需要登录才可以赞'}, 'utf-8')

    try:
        comments.user_comments_likes_map.objects.get(publisher=r.session.get('userid'), comment_id=p)
        return j.dic({'error': '你已经赞过了'}, 'utf-8')
    except:
        try:
            comments.user_comments_likes_map.objects.create(publisher=r.session.get('userid'), comment_id=p)
            res = comments.user_comments.objects.get(id=p)
            res.likes += 1
            res.save()
            return j.dic({'success': res.likes}, 'utf-8')
        except Exception as eee:
            return j.dic({'error': '出错了' if s.RELEASE else str(eee)}, 'utf-8')

def user_comment_delete(r,f,p):

    if not p_user.is_logged(r):
        return j.dic({'error': '需要登录才可以操作'}, 'utf-8')

    try:
        userid = r.session.get('userid')

        ownerid = str(comments.user_comments.objects.get(id=p).userid)

        if userid != ownerid:
            return j.dic({'error': '只可以删除自己收到的评论哦'}, 'utf-8')

        # 删除赞数据
        res = comments.user_comments_likes_map.objects.filter(comment_id=p)
        for item in res:
            item.delete()

        # 删除留言
        comments.user_comments.objects.get(id=p).delete()

        return j.dic({'success': 'ok'}, 'utf-8')
    except Exception as eee:
        return j.dic({'error': '出错了' if s.RELEASE else str(eee)}, 'utf-8')