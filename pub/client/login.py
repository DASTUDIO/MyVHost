# coding=utf-8

import time
import pub.functions.token as token
import pub.response.json as j
from pub.tables.cache.suspend import *
from pub.tables.user import *
import pub.response.error as err
import pub.settings as s


# 登录成功后 由外部调用
def set_cache(key,value):
    try:
        h = cache_suspend.objects.filter(type=s.CACHE_TYPE_LOGIN_SESSION_TO_USER, key=key)

        if len(h) == 0:
            raise Exception('这个session不存在')

        h[0].value = value
        h[0].save()

    except Exception as e:
        return j.err(str(e), 'utf-8')

# 主动登录ajax
def login(request, folder, post_url):

    #_counter()

    session = request.session.get(s.SESSION_LOGIN)

    if session:
        try:
            # 验证session是否登录 不存在数据库内会抛异常（过期清除） 未登录也是存在的
            result = check_session(request, session)
        except:
            # 保险起见 清除一下
            clean_cache(session)

            # 给request.session添加id 并添加数据库
            create_session_cache(request)

            return j.dic({'state': 'error', 'session': session})
    else:
        create_session_cache(request)
        return j.dic({'state': 'error', 'session': session})

    return j.dic(result)

# 主动登出 网页
def logout(request,folder,post_url):
    try:
        session = request.session.get(s.SESSION_LOGIN)

        if session:
            clean_cache(session)

    except:
        pass

    finally:
        request.session.clear()
        request.session.flush()

    return err.page_shutdown(request,200,'已安全退出')


# 登录检查
def check_session(request, session_id):

    data = {}

    data['state'] = 'error'

    data['session'] = session_id

    r = cache_suspend.objects.filter(type=s.CACHE_TYPE_LOGIN_SESSION_TO_USER, key=session_id)

    res = r[0].value

    if res == '-1':
        return data

    else:
        user_info = get_auth_user(res)
        request.session['userid'] = res
        request.session['nickname'] = user_info['nickname']
        request.session['headimg'] = user_info['headimg']

        data['state'] = 'success'
        data['openid'] = user_info['openid']
        data['nickname'] = user_info['nickname']
        data['provider'] = user_info['provider']
        data['headimg'] = user_info['headimg']
        data['session'] = session_id
        return data

def create_session_cache(request):

    key = request.session[s.SESSION_LOGIN] = gen_session_id()

    try:
        cache_suspend.objects.create(type=s.CACHE_TYPE_LOGIN_SESSION_TO_USER, key=key, value='-1')
    except Exception as e:
        raise Exception(e)

    return key

def gen_session_id():

    res = str(int(time.time())) + token.alpha_token(7)

    check = cache_suspend.objects.filter(type=s.CACHE_TYPE_LOGIN_SESSION_TO_USER, key=res)
    if len(check) != 0:
        return gen_session_id()

    return res

def get_auth_user(id):
    r = auth_user.objects.filter(id=id)
    openid = r[0].openid
    headimg = r[0].headimg
    nickname = r[0].nickname
    authprovider = r[0].authprovider
    return {'openid':openid,'nickname':nickname,'provider':authprovider,'headimg':headimg}


def clean_cache(key):
    r = cache_suspend.objects.filter(type=s.CACHE_TYPE_LOGIN_SESSION_TO_USER, key=key)
    for item in r:
        item.delete()

# 添加跳转用到
def get_user_by_session(request, session):
    r = cache_suspend.objects.filter(type=s.CACHE_TYPE_LOGIN_SESSION_TO_USER, key=session)
    return r[0].value
