# coding=utf-8
import pub.response.error as error
import pub.response.wrap as wrapper
import pub.functions.wx as wx
from django.http import HttpResponse
from .folder import cast
from pub.tables.map.files import hash_to_key


def testh(r,f,p):
    hash_to_key.objects.create(hash='test1',key='testkey')


def wx(request,folder,post_url):
    sig = request.GET.get('signature')
    ts = request.GET.get('timestamp')
    nc = request.GET.get('nonce')
    es = request.GET.get('echostr')
    rst = wx.verify(sig, ts, nc, es)
    return HttpResponse(rst)

def profile(request,folder,post_url):
    ctx = {}
    ctx['username'] = request.user.username
    ctx['userlevel'] = 'developer'
    return wrapper.page(request, 'profile.html', ctx)

def ajax(request,folder,post_url):
    return error.page(request)

def html(request,folder,post_url):
    return wrapper.page(request, str(post_url))

def iframe(request,folder,posturl):
    return wrapper.agent(request, 'iframe', 'http://' + posturl)


def do():

    # cast('testh', testh)

    # cast('weixin',wx)
    #
    # cast('tsms',(lambda request,folder,post_url:sms.tsms(request)))
    # cast('token',(lambda request,folder,post_url:HttpResponse(token.alpha_token())))
    # cast('number_token',(lambda request,folder,post_url:HttpResponse(token.digit_token())))
    # cast('sms_token',lambda request,folder,post_url:HttpResponse(token.sms_token()))
    # cast('random_number',(lambda request,folder,post_url:HttpResponse(token.random_0_to_1())))
    # cast('qrcode', (lambda request,folder,post_url: wrapper.page(request, 'libs/qrcode.html')))
    # cast('file', (lambda request,folder,post_url: wrapper.page(request, 'file-manager.html')))
    # cast('login', (lambda request,folder,post_url: wrapper.page(request, 'login.html')))
    # cast('formc', (lambda request,folder,post_url: wrapper.page(request, 'form-components.html')))
    # cast('forme', (lambda request,folder,post_url: wrapper.page(request, 'form-elements.html')))
    # cast('dologin',(lambda request,folder,post_url:mlogin.login(request)))
    # cast('doregister',(lambda request,folder,post_url:mlogin.register(request)))
    # cast('meditor', (lambda request,folder,post_url: wrapper.page(request, 'libs/meditor.html')))
    # cast('pceditor', (lambda request,folder,post_url: wrapper.page(request, 'libs/pceditor.html')))
    # cast('cmp', (lambda request,folder,post_url: wrapper.page(request, 'components.html')))
# cast('?',lambda request,folder,post_url:HttpResponse(api_f.get_time()))
# cast('check_resource',(lambda request,folder,post_url:HttpResponse(api_f.check_resource(request.GET.get('id')))))
# cast('isowner',(lambda request,folder,post_url:HttpResponse(api_f.check_owner(1,'boss'))))
# cast('post',(lambda request,folder,post_url:HttpResponse(repr(api_f.get_post_params(request)))))
# cast('get',(lambda request,folder,post_url:HttpResponse(repr(api_f.get_get_params(request)))))
# cast('json',(lambda request,folde,post_urlr:HttpResponse(repr(api_f.get_json(request)))))
#     cast('gen_path',(lambda request,folder,post_url:HttpResponse(repr(gen_path(request.GET.get('username'), request.GET.get('rname'), token.alpha_token())))))
#     cast('gen_sp',(lambda request,folder,post_url:HttpResponse(repr(gen_sp(request.GET.get('username'), request.GET.get('rname'), token.alpha_token())))))
#     cast('ajax',ajax)
    cast('page',html)
    cast('iframe',iframe)

    # cast('ch',creator.resource_custom_html)
