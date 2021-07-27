# coding=utf-8
from django.shortcuts import render
import json
from django.http import HttpResponse as http_text
import pub.settings as settings

NO_PERMISSION = 0
WRONG_TOKEN = 1
ALREADY_EXIST = 2
NO_OBJECT = 3


def page(request, code='500', error='', detail=''):
    content_dict = {}
    content_dict['code'] = code
    content_dict['error'] = error
    content_dict['detail'] = detail
    return render(request,settings.THEME +'/error.html',content_dict)

def page_shutdown(request, code='500', error='', detail=''):
    content_dict = {}
    content_dict['code'] = code
    content_dict['error'] = error
    content_dict['detail'] = detail
    return render(request,settings.THEME +'/error_shutdown.html',content_dict)


def json_err(result_code):
    msg = {}
    msg['error'] = _result_code_msg(str(result_code))
    return http_text(json.dumps(msg))

def json_err_text(msg,error_tag='error'):
    msg = {error_tag:msg}
    return http_text(json.dumps(msg))

def _result_code_msg(result_code):
    dic = {}
    dic['0'] = 'no permission'
    dic['1'] = 'ok'
    dic['2'] = 'can not found token'
    dic['3'] = 'can not found userpermission'
    dic['4'] = 'file already exists'
    dic['5'] = 'params format not correct'
    dic['6'] = 'invalid create token'
    if result_code in dic:
        return dic[result_code]
    return 'unknow'