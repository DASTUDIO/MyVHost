# coding=utf-8
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
import pub.settings as settings
import time
import pub.models as db

from django.http import HttpResponse as show_text

appid="1400184471"
appkey="dce3abb24f93e1346f51961388f72bbc"


def send_verification(number,verification):
    phone_numbers =[number]
    template_id=275687
    sms_sign="微服务器"
    ssender=SmsSingleSender(appid,appkey)
    params=[verification]
    try:
        return ssender.send_with_param(86,phone_numbers[0],template_id,params,sign=sms_sign,extend="",ext="")
    except HTTPError as e:
        return e
    except Exception as e:
        return e


def get_cache(phone_number):
    search_params = {}       # 构建查询字典
    search_params['token_type'] = settings.TOKEN_SMS_VERIFICATION
    search_params['key'] = phone_number

    result_list = db.token.objects.filter(**search_params)  # 查询

    result = -1

    if len(result_list) > 0:            # 如果有值
        result = result_list[0].value   # 取值

        if result_list[0].due_time < int(time.time()):  # 判断是否过期 如果是清除
            result_list[0].delete()

    return result



def set_cache(phone_number,verification):
    search_params = {}  # 构建查询字典
    search_params['token_type'] = settings.TOKEN_SMS_VERIFICATION
    search_params['key'] = phone_number


    _value = verification
    _due_time = int(time.time()) + settings.TIME_SMS_VERIFICATION

    result_list = db.token.objects.filter(**search_params)  # 查询

    if len(result_list) != 0:       # 如果有值 更新
        result_list[0].due_time = _due_time
        result_list[0].value = _value

        result_list[0].save()
    else:                           # 如果没值 创建
        cache = db.token.objects.create(token_type=search_params['token_type'],due_time=_due_time,key=phone_number,value=_value)
        cache.save()



#print(int(time.time()))

def tsms(request):
    #return show_text('???')

    set_cache('173xxxxxxxx','testtoken123')
    send_verification('173xxxxxxxx','testtoken123')
    return show_text(get_cache('173xxxxxxxx'))
