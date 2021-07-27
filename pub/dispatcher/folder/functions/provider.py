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

# 本文件留作备份 业务再providers文件夹里

# Content Provider
def content_provider(page):
    try:
        data = {'state':'error'}
        res = resource.resource_info.objects.all()
        pag = Paginator(res,s.PAGE_SIZE)
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

            user_headimg = u_info.headimg

            nickname = u_info.nickname

            user_link = "/user/" + str(userid)

            it = {'title': __fix_row(item.title),
                  'brief': __fix_row(item.brief),
                  'headimg': item.headimg,
                  'key': item.key,
                  'user_headimg' : user_headimg,
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


# User Provider
def user_provider(request,folder,userid):
    try:
        data = {}
        res = user.auth_user.objects.get(id=userid)
        data['u_nickname'] = res.nickname
        data['u_headimg'] = res.headimg
        data['u_id'] = res.id


        info_res = user.user_info.objects.get(userid=userid)
        data['brief'] = info_res.brief
        data['position'] = info_res.position
        data['friend_url'] = info_res.friend_url
        data['active'] = info_res.active

        return w.page(request,'user.html',data)
    except Exception as e:
        return error.page(request, 404, "该人无法显示", "该名片还未开通" if s.RELEASE else "该名片还未开通"+str(e))


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