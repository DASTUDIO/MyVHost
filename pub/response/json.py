#coding=utf-8
import json
from django.http import HttpResponse

def dic(params,encoding=''):
    if encoding != '':
        return HttpResponse(json.dumps(params,ensure_ascii=False),content_type='application/json', charset=encoding)
    else:
        return HttpResponse(json.dumps(params))

def err(msg,encoding=''):
    if encoding == '':
        return HttpResponse(json.dumps({'error':str(msg)}))
    else:
        return HttpResponse(json.dumps({'error': str(msg)},ensure_ascii=False),content_type='application/json', charset=encoding)

def custom(msg,encoding=''):
    if encoding != '':
        return  HttpResponse(msg,content_type='application/json', charset=encoding)
    else:
        return HttpResponse(msg)

def dic_json_p(params,callback_name,encoding=''):
    if encoding != '':
        return HttpResponse(callback_name+"("+json.dumps(params,ensure_ascii=False)+");",content_type='text/javascript', charset=encoding)
    else:
        return HttpResponse(json.dumps(params))