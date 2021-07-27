import pub.settings as s
import json, requests
import pub.response.wrap as wrapper
import pub.response.error as e
import pub.client.auth_handler as auth_handler
import re

auth_url = 'https://github.com/login/oauth/authorize?client_id=' \
           + s.GITHUB_CLIENT_ID + '&state='

access_token_url = 'https://github.com/login/oauth/access_token'

info_url = 'https://api.github.com/user?access_token='


def begin_login(session):
    return wrapper.jump(auth_url+session)


def handle_callback(request, _):
    try:
        code = request.GET.get('code')
        session = request.GET.get('state')

        # \
        # + '?client_id=' + s.GITHUB_CLIENT_ID \
        # + '&client_secret=' + s.GITHUB_CLIENT_SECRETS \
        # + '&code='

        params = {'client_id': s.GITHUB_CLIENT_ID, 'client_secret': s.GITHUB_CLIENT_SECRETS, 'code': code}
        headers = {'accept': 'application/json'}
        res = requests.post(access_token_url, data=params).text
        #return e.json_err_text(res)
        try:

            access_token = re.match(r'access_token=(.*?)&', res).group(1)
            #return e.page(request, 511, access_token, res)
        except Exception as e1:
            return e.page(request, 501, e1, res)

        url = info_url + access_token
        headers = {"Authorization": "token " + access_token}
        res2 = requests.get(url, headers=headers).text
        #return e.page(request, 502, 'id?', res2)
        try:
            result = json.loads(res2)
        except Exception as e2:
            return e.page(request, 502, e2, res2)

        data = {'openid': result['id'], 'nickname': result['login'], 'headimg': result['avatar_url'],
                'session_id': session, 'authprovider': s.AUTH_PROVIDER_GITHUB}

        return auth_handler.login_user(request, data)
    except Exception as d:
        return e.page(request,500,"x",d)

