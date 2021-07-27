# coding=utf-8
from pub.tables.resources import *
from pub.tables.user import *
import pub.client.login as login
import pub.tables.map.domain as d

def is_logged(request):
    try:
        user = login.get_user_by_session(request,request.session.get(s.SESSION_LOGIN))
        if user:
            if user != '-1':
                return True
        return False
    except:
        return False


def is_owner(request,key):
    if not is_logged(request):
        return False
    try:
        user = request.session.get('userid')
        resource_to_user.objects.get(key=key, userid=user)
        return True
    except:
        return False


def has_domain(request,domain):
    try:
        userid = request.session.get('userid')
        res = d.domain_to_user.objects.get(domain=domain, user=userid)
        if res.token == '':
            return True
        else:
            return False
    except:
        return False
