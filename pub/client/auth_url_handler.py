# coding=utf-8
import pub.functions.coder as coder
import pub.response.json as j
import pub.strings as strings
import pub.response.error as error
import pub.settings as settings
import pub.client.auth_handler as auth_handler
from pub.client.auth.weixin import weixin_login
from pub.client.auth.alipay import alipay_login

from pub.tables.cache.suspend import *

import pub.client.auth.github as github

# 扫码后的回调
def handler(request,folder,posturl):

    data ={'state':'error'}

    session = posturl

    try:
        session = coder.navie_dvc_base64_decode(session)

        try:
            userid = cache_suspend.objects.get(type=s.CACHE_TYPE_LOGIN_SESSION_TO_USER, key=session).value

            if userid != '-1':
                return error.page(request, 706, '这个二维码已经使用过了')
        except:
            return error.page(request, 706, '这个二维码过期了')

    except Exception as e:
        msg = '' if settings.RELEASE else str(e)
        return error.page(request, 706, 'url不正确'+msg)

    user_agent = request.META['HTTP_USER_AGENT'].lower()

    # if strings.AGENT_WEIXIN.lower() in user_agent:
    #
    #     return weixin_login(session)
    #     #return error.page(request,200,'微信客户端',session)
    # elif strings.AGENT_ALIPAY.lower() in user_agent:
    #     return alipay_login(session)
    #     #return error.page(request, 200, '支付宝客户端',session)
    # elif strings.AGENT_WEIBO.lower() in user_agent:
    #
    #     return error.page(request, 200, '暂不支持微博客户端', '为了确保用户实名，目前仅支持支付宝和微信客户端')
    # elif strings.AGENT_QQ.lower() in user_agent:
    #
    #     return error.page(request, 200, '暂不支持QQ客户端', '为了确保用户实名，目前仅支持支付宝和微信客户端')
    # else:
    #     return error.page(request,707,'暂不其他客户端', '为了确保用户实名，目前仅支持支付宝和微信客户端')

    return github.begin_login(session)


def test_login(session_id):
    data = {}

    data['openid'] = 'test_open_id'

    data['nickname'] = 'test_nickname'

    data['headimg'] = 'test_headimg'

    data['authprovider'] = 0

    data['session_id'] = session_id

    return auth_handler.login_user(data)