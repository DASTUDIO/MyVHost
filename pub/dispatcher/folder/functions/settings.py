# coding=utf-8

from pub.forms.settings import form_settings_profile
import pub.response.json as j
from pub.tables.user import user_info
import pub.permission.decorator as deco

@deco.require_login
def settings_set_profile(r,f,p):

    if not r.POST:
        return j.err('参数不正确','utf-8')

    f_profile = form_settings_profile(r.POST)

    if not f_profile.is_valid():
        return j.err('请完整填写', 'utf-8')

    userid = r.session.get('userid')

    try:
        res = user_info.objects.get(userid=userid)
        res.delete()
        raise Exception()
    except:
        try:
            user_info.objects.create(userid=userid,
                                     active=0,

                                    position=f_profile.cleaned_data['position'],
                                    friend_url = f_profile.cleaned_data['friend_url'],
                                    brief = f_profile.cleaned_data['brief'],

                                    real_name = f_profile.cleaned_data['real_name'],
                                    id_code = f_profile.cleaned_data['id_code'],
                                    phone = f_profile.cleaned_data['phone'],
                                    email = f_profile.cleaned_data['email']
                                    )
        except Exception as eee:
            return j.err(eee)
        return j.dic({'success':'ok'}, 'utf-8')