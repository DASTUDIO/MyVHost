# coding=utf-8

import pub.settings as s
from urllib.parse import urlencode ,quote_plus
import json,requests
import pub.client.auth_handler as auth_handler

import pub.response.wrap as wrapper

import pub.strings as strings
import pub.settings as settings
import pub.functions.coder as coder

import pub.response.json as j

import pub.log.logger as l

# configs
# 显式授权
config_scope = "snsapi_userinfo"


# return types
# error
#error = "errcode"
#error_msg = "errmsg"

# access token
#token = "access_token"
#expires = "expires_in"
#refresh = "refresh_token"
#openid = "openid"
#scope = "scope"

# user info
#open_id = "openid"
#nickname = "nickname"
#sex = "sex"
#province = "province"
#city = "city"
#country = "country"
#headimg = "headimgurl"
#privilege = "privilege"
#unionid = "unionid"


# url constructor
# return get: code state
def __get_code_url(state:str,redirect_url:str):
    return "https://open.weixin.qq.com/connect/oauth2/authorize?appid=" + s.WX_KEY +\
      "&redirect_uri=" + quote_plus(redirect_url) +\
      "&response_type=code"\
      "&scope=" + config_scope +\
      "&state=" + state +\
      "#wechat_redirect"

# return json : access token
def __get_access_token_url_by_code(code:str):
    return "https://api.weixin.qq.com/sns/oauth2/access_token?appid="+s.WX_KEY + \
           "&secret=" + s.WX_SECRET + \
           "&code="+code + \
           "&grant_type=authorization_code"

#return json: user info
def __get_user_info_url_by_access_token(access_token:str,open_id:str):
    return "https://api.weixin.qq.com/sns/userinfo?access_token="+access_token+\
           "&openid="+open_id+\
           "&lang=zh_CN"

# tools
def _get(url):
    response = requests.get(url=url)
    return response.text

# do login
def weixin_login(session):
    #return j.err(__get_code_url(session,"https://src.pub/auth_ax/"))
    return wrapper.jump(__get_code_url(session,"https://src.pub/auth_wx/"))

# 微信方发起的回调auth_wx
def get_code_callback(request, folder, posturl):

    _code = request.GET.get('code')
    _state = request.GET.get('state')

    # 获取 accesstoken openid
    jres = _get(__get_access_token_url_by_code(_code))
    #return j.err(jres)
    res = json.loads(jres)
    #return j.err(repr(res))
    _access_token = res['access_token']

    _openid = res['openid']

    # 获取用户详情
    jinfo = _get(__get_user_info_url_by_access_token(_access_token, _openid))

    #return j.err(jinfo)
    info = json.loads(jinfo)

    _nickname = info['nickname'].encode('iso-8859-1').decode('utf8')
    _sex = info['sex']
    _province = info['province'].encode('iso-8859-1').decode('utf8')
    _city = info['city'].encode('iso-8859-1').decode('utf8')
    _country = info['country'].encode('iso-8859-1').decode('utf8')
    _headimg = info['headimgurl'].encode('iso-8859-1').decode('utf8')

    data = {}

    data['openid'] = _openid

    data['nickname'] = _nickname

    data['headimg'] = _headimg

    data['authprovider'] = s.AUTH_PROVIDER_WEIXIN

    data['session_id'] = _state

    return auth_handler.login_user(request,data)

def wx_auth(func):

    def process(r,f,p):
        try:
            user_agent = r.META['HTTP_USER_AGENT'].lower()

            if strings.AGENT_WEIXIN.lower() in user_agent:

                userid = r.session.get('userid')

                if not userid or userid == -1:
                    return wrapper.jump('https://src.pub/page/wxlogin.html')

        except:pass

        return func(r,f,p)

    return process