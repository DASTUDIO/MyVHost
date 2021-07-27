import pub.settings as s
from urllib.parse import quote_plus

from pub.client.auth.lib.alipay import ISVAliPay

from pub.response.json import custom
from  pub.response.error import page as epage

import pub.response.wrap as wrapper

import pub.client.auth_handler as auth_handler

config_scope = 'auth_user'



def __get_code_url(state:str,redirect_url:str):
    return 'https://openauth.alipay.com/oauth2/publicAppAuthorize.htm?' \
           'app_id='+ s.ALIPAY_APPID +\
           '&scope='+ config_scope +\
           '&redirect_uri='+quote_plus(redirect_url) +\
           '&state='+state

def get_code_callback(r,f,p):
    try:
        auth_code = r.GET.get('auth_code')
        auth_state = r.GET.get('state')
        if auth_code:
            isv_alipay = ISVAliPay(
            appid=s.ALIPAY_APPID,
            app_notify_url="https://src.pub/auth_alipay/",
            app_private_key_string=s.ALIPAY_MY_PRI_KEY,
            alipay_public_key_string=s.ALIPAY_PUB_KEY,
            sign_type="RSA2",
            debug=False,
            app_auth_code=auth_code,
            app_auth_token=None,
            )

            res = isv_alipay.api_alipay_open_auth_token()
            #return custom(res["access_token"])

            isv_alipay2 = ISVAliPay(
                appid=s.ALIPAY_APPID,
                app_notify_url="https://src.pub/auth_alipay/",
                app_private_key_string=s.ALIPAY_MY_PRI_KEY,
                alipay_public_key_string=s.ALIPAY_PUB_KEY,
                sign_type="RSA2",
                debug=False,
                app_auth_code=None,
                app_auth_token=res["access_token"]
            )

            res = isv_alipay2.api_alipay_open_auth_token_query()

            #return dic(res, 'gbk')

            if not 'nick_name' in res:
                return epage(r, 307, '目前仅支持个人用户登录')

            data = {}
            data['openid'] = res['user_id'].encode('gbk').decode('utf8')
            data['nickname'] = res['nick_name'].encode('gbk').decode('utf8')
            data['headimg'] = res['avatar'].encode('gbk').decode('utf8')
            data['authprovider'] = s.AUTH_PROVIDER_ALIPAY
            data['session_id'] = auth_state

            return auth_handler.login_user(r,data)

        return custom('NaN')
    except Exception as e1:
        return custom('error：'+str(e1))


# def sign_string(private_key, unsigned_string):
#     # 开始计算签名
#     #print(private_key)
#     key = RSA.importKey(private_key)
#     signer = PKCS1_v1_5.new(key)
#     signature = signer.sign(SHA.new(unsigned_string.encode("utf8")))
#     # base64 编码，转换为unicode表示并移除回车
#     sign = base64.encodebytes(signature).decode("utf8").replace("\n", "")
#     return sign
#
# signed_string = sign_string(s.ALIPAY_MY_PRI_KEY, '{"a":"123"}')
# print(signed_string)
#
#
# def validate_sign(public_key, message, signature):
#     # 开始计算签名
#     key = RSA.importKey(public_key)
#     signer = PKCS1_v1_5.new(key)
#     digest = SHA.new()
#     digest.update(message.encode("utf8"))
#     if signer.verify(digest, base64.decodebytes(signature.encode("utf8"))):
#         return True
#     return False
#
# result = validate_sign(s.ALIPAY_MY_PUB_KEY, '{"a":"123"}', signed_string)
# print(result)

def alipay_login(session):
    return wrapper.jump(__get_code_url(session,"https://src.pub/auth_alipay/"))


