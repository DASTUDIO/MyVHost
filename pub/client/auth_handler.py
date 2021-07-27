#coding=utf-8
import pub.response.json as j
from pub.tables.user import *
import pub.client.login as login
import pub.strings as strings
import pub.settings as settings
import pub.functions.coder as coder
import pub.response.error as error

def get_auth_url(request,folder,posturl):

    data = {'state':'error'}
    session = request.session.get(settings.SESSION_LOGIN)
    if not session:
        data['message'] = '请刷新页面重试，若依然存在问题请检查浏览器是否禁用了JS及AJAX功能。'
        return j.dic(data,'utf-8')
    host = request.META['HTTP_HOST'] # if settings.RELEASE else '192.168.0.103'
    url = strings.HTTP_OR_HTTPS + host + '/' + strings.FLODER_AUTH + '/' + coder.navie_dvc_base64_encode(session)
    data['result'] = url
    data['state'] = 'success'
    return j.dic(data,'utf-8')


# def test_handler(request,folder,posturl):
#
#     if not request.GET:
#         return j.err('没有传入参数','utf-8')
#
#     f = handler_test_auth(request.GET)
#
#     if not f.is_valid():
#         return j.err('参数不正确', 'utf-8')
#
#     data = {}
#
#     data['openid'] = f.cleaned_data['openid']
#
#     data['nickname'] = f.cleaned_data['nickname']
#
#     data['headimg'] = f.cleaned_data['headimg']
#
#     data['authprovider'] = f.cleaned_data['authprovider']
#
#     data['session_id'] = posturl
#
#     return login_user(data)

# 构建data后调用这个
def login_user(request,data):                           # login & reigister user
    try:
        openid = data['openid']

        nickname = data['nickname']

        headimg = data['headimg']

        authprovider = data['authprovider']

        h = auth_user.objects.filter(openid=openid,authprovider=authprovider)

        if len(h) == 0:
            t = auth_user.objects.create(openid=openid,nickname=nickname,headimg=headimg,authprovider=authprovider)
            user_permission.objects.create(user_id=t.id,type=s.RESOURCE_TYPE_CUSTOMED,volume=10)
            user_permission.objects.create(user_id=t.id, type=s.RESOURCE_TYPE_TEMPLATED, volume=10)
            user_permission.objects.create(user_id=t.id, type=s.RESOURCE_TYPE_RESTFUL_API, volume=10)
            user_permission.objects.create(user_id=t.id, type=s.RESOURCE_TYPE_SHORT_LINK, volume=10)
            user_permission.objects.create(user_id=t.id, type=s.RESOURCE_TYPE_IFRAME, volume=10)
            id = t.id
        else:
            id = h[0].id
            h[0].nickname = nickname
            h[0].headimg = headimg
            h[0].save()

        session_id = data['session_id']

        login.set_cache(session_id, id)

        data['state'] = 'ok'

        return error.page_shutdown(request,200,'登录成功')

    except Exception as e:
        return j.err(e,'utf-8')
