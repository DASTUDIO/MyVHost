#coding=utf-8

from pub.tables.resources import resource_type,resource_info,resource_to_user,resource_permission,\
    resource_customed,resource_restful,resource_restful_item,resource_link,resource_iframe
from pub.tables.map.domain import domain_to_key
from pub.tables.user import user_info
import pub.settings as s
import pub.response.json as j
import pub.response.error as err
import pub.response.wrap as w
import os
import pub.permission.resource as p_resource
import pub.permission.user as p_user
from pub.functions.sms import send_verification

from pub.forms.verify import sms_code
from pub.functions.token import digit_token

def delete_resource(r,f,p):
    # login
    if not p_user.is_logged(r):
        return err.page(r,407,'需要登录才可以操作')

    # own
    if not p_user.is_owner(r, p):
        return j.err('只有本人才可以删除', 'utf-8')

    userid = r.session.get('userid')

    # sms verify(release only)
    if True:

        try:
            phone = user_info.objects.get(userid=userid).phone
        except:
            return err.page(r, 407, '需要填写手机号码才可以操作', '请进入微名片填写手机号码并完善用户信息')

        if r.GET or r.POST:
            if r.GET:
                request_content = r.GET
            else:
                request_content = r.POST

            f_sms = sms_code(request_content)

            if not f_sms.is_valid():
                _code = digit_token(6)
                send_verification(phone,str(_code))
                r.session['sms_code'] = _code
                return w.page(r,'error_verify.html',{'phone': phone,'title':'验证操作','code': 300})

            code = f_sms.cleaned_data['code']

            if code != r.session.get('sms_code'):
                return err.page(r, 407, '您填写的验证码不正确')
        else:
            _code = digit_token(6)
            send_verification(phone, str(_code))
            r.session['sms_code'] = _code
            return w.page(r, 'error_verify.html', {'phone': phone, 'title': '验证操作', 'code': 300})

    #  do del
    try:
        type = resource_type.objects.get(key=p)

        _type = type.type

        type.delete()

        if _type == s.RESOURCE_TYPE_CUSTOMED:
            return del_customed(p)

        if _type == s.RESOURCE_TYPE_TEMPLATED:
            return del_templated(p)

        if _type == s.RESOURCE_TYPE_RESTFUL_API:
            return del_restful_api(p)

        if _type == s.RESOURCE_TYPE_SHORT_LINK:
            return del_short_link(p)

        if _type == s.RESOURCE_TYPE_IFRAME:
            return del_iframe(p)

    except Exception as eee:
        return j.err('该记录不存在' if s.RELEASE else str(eee), 'utf-8')


def del_customed(key):

    result = []

    try:
        # files
        try:
            r = resource_customed.objects.get(key=key)
            os.remove(os.path.join(s.TEMPLATE_PATH, r.path))
            r.delete()
        except Exception as eee:
            result.append(str(eee))

        # owner
        try:
            ru = resource_to_user.objects.get(key=key)
            ru.delete()
        except Exception as eee:
            result.append(str(eee))

        # domain 非可选
        try:
            do = domain_to_key.objects.get(key=key)
            do.delete()
        except Exception as eee:
            result.append(str(eee))

        # permission
        try:
            pe = resource_permission.objects.get(key=key)
            pe.delete()
        except Exception as eee:
            result.append(str(eee))

        # card 非可选
        try:
            ri = resource_info.objects.get(key=key)
            ri.delete()
        except Exception as eee:
            result.append(str(eee))

        return j.dic({'success':'ok','log':result if not s.RELEASE else []}, 'utf-8')

    except Exception as eee:
        return j.err(str(eee), 'utf-8')


def del_templated(key):
    pass

def del_restful_api(key):

    result = []

    # reocord
    try:
        rr = resource_restful.objects.get(key=key)
        rr.delete()
    except Exception as eee:
        result.append(eee)

    # item
    try:
        ris = resource_restful_item.objects.filter(key=key)
        for item in ris:
            item.delete()
    except Exception as eee:
        result.append(eee)

    # owner
    try:
        ru = resource_to_user.objects.get(key=key)
        ru.delete()
    except Exception as eee:
        result.append(str(eee))

    # permission
    try:
        pe = resource_permission.objects.get(key=key)
        pe.delete()
    except Exception as eee:
        result.append(str(eee))

    return j.dic({'success': 'ok', 'log': result if not s.RELEASE else []}, 'utf-8')

def del_short_link(key):

    result = []

    # owner
    try:
        ru = resource_to_user.objects.get(key=key)
        ru.delete()
    except Exception as eee:
        result.append(str(eee))

    # permission
    try:
        pe = resource_permission.objects.get(key=key)
        pe.delete()
    except Exception as eee:
        result.append(str(eee))

    # reocord
    try:
        rr = resource_link.objects.get(key=key)
        rr.delete()
    except Exception as eee:
        result.append(eee)

    # owner
    try:
        ru = resource_to_user.objects.get(key=key)
        ru.delete()
    except Exception as eee:
        result.append(str(eee))

    # domain 非可选
    try:
        do = domain_to_key.objects.get(key=key)
        do.delete()
    except Exception as eee:
        result.append(str(eee))

    return j.dic({'success': 'ok', 'log': result if not s.RELEASE else []}, 'utf-8')


def del_iframe(key):
    result = []

    # reocord
    try:
        rr = resource_iframe.objects.get(key=key)
        rr.delete()
    except Exception as eee:
        result.append(eee)

    result = []

    # permission
    try:
        pe = resource_permission.objects.get(key=key)
        pe.delete()
    except Exception as eee:
        result.append(str(eee))

    # owner
    try:
        ru = resource_to_user.objects.get(key=key)
        ru.delete()
    except Exception as eee:
        result.append(str(eee))

    # domain 非可选
    try:
        do = domain_to_key.objects.get(key=key)
        do.delete()
    except Exception as eee:
        result.append(str(eee))

    return j.dic({'success': 'ok', 'log': result if not s.RELEASE else []}, 'utf-8')