#coding=utf-8

import pub.settings as settings
from pub.tables.resources import resource_restful,resource_type,resource_restful_item
import pub.forms.api as api
import pub.response.json as j

from pub.forms.token import form_token
import pub.permission.resource as permission

def get_restful_api(request, url_key):

    is_jsonp = False

    cb_name = 'callback'

    if request.GET or request.POST:

        try:

            data = {'state':'error'}

            if request.GET:
                request_content = request.GET
            else:
                request_content = request.POST

            # act
            form_act = api.api_query(request_content)

            if not form_act.is_valid():
                raise Exception('parameter : act is required , add this after parameters &act=someact')

            act = form_act.cleaned_data['act']

            # jsonp : callback
            cb = api.api_callback(request_content)
            if cb.is_valid():
                cb_name = cb.cleaned_data['callback']

            # token
            token = ''
            tk = form_token(request_content)
            if tk.is_valid():
                token = tk.cleaned_data['token']

            if act == 'query':

                if not permission.can_read(request, url_key, token or ''):
                    return j.dic({'error': '您需要权限执行此操作'}, 'utf-8')

                return _restful_query(url_key, data, request_content)

            if act == 'queryp':

                if not permission.can_read(request, url_key, token or ''):
                    return j.dic({'error': '您需要权限执行此操作'}, 'utf-8')

                is_jsonp = True

                return _restful_query(url_key, data, request_content, True, cb_name)

            elif act == 'add':

                if not permission.can_write(request, url_key, token or ''):
                    return j.dic({'error': '您需要权限执行此操作'}, 'utf-8')

                return _restful_add(url_key, data, request_content)

            elif act == 'addp':

                if not permission.can_write(request, url_key, token or ''):
                    return j.dic({'error': '您需要权限执行此操作'}, 'utf-8')

                is_jsonp = True

                return _restful_add(url_key, data, request_content, True, cb_name)

            elif act == 'delete':

                if not permission.can_modify(request, url_key, token or ''):
                    return j.dic({'error': '您需要权限执行此操作'}, 'utf-8')

                return _restful_delete(url_key, data, request_content)

            elif act == 'deletep':

                if not permission.can_modify(request, url_key, token or ''):
                    return j.dic({'error': '您需要权限执行此操作'}, 'utf-8')

                is_jsonp = True

                return _restful_delete(url_key, data, request_content, True, cb_name)

            elif act == 'modify':

                if not permission.can_modify(request, url_key, token or ''):
                    return j.dic({'error': '您需要权限执行此操作'}, 'utf-8')

                return _restful_modify(url_key,data,request_content)

            elif act == 'modifyp':

                if not permission.can_modify(request, url_key, token or ''):
                    return j.dic({'error': '您需要权限执行此操作'}, 'utf-8')

                return _restful_modify(url_key,data,request_content,True,cb_name)


            elif act == 'help':

                data['act'] = 'help'

                data['message'] = '你可以使用GET或POST方式提交参数,提交的参数有四个act,key,value,token,其中act的值为:query查询,add增加,delete删除,modify删除,help帮助,login登录,logout登出,在后加p为jsonp模式，如queryp,jsonp模式下使用callback参数指定回调函数名如&callback=run默认为\'callback\''

                data['state'] = 'ok'

            elif act == 'login':
                pass

            elif act == 'logout':
                pass

            else:
                raise Exception('unknow act: '+act+' , query ?act=help to get manual . ')

        except Exception as ex:
            data['message'] = str(ex)

        return __return_json_error(data,is_jsonp,cb_name)

    else:
        try:
            token = ''

            if request.GET or request.POST:
                if request.GET:
                    request_content = request.GET
                else:
                    request_content = request.POST

                # token
                tk = form_token(request_content)
                if tk.is_valid():
                    token = tk.cleaned_data['token']

            if not permission.can_read(request, url_key, token or ''):
                return j.dic({'error': '您需要权限执行此操作'}, 'utf-8')

            return __return_all(url_key, cb_name , is_jsonp)
        except Exception as ee:
            if settings.RELEASE:
                resource_type.objects.filter(key=url_key).delete()
            return j.err('404 not found' + str(ee) if not settings.RELEASE else '')


def __return_all(url_key, callback_name, is_jsonp=False):
    resource = resource_restful.objects.get(key=url_key)
    name = resource.name
    # check accessibility...
    params_list = resource_restful_item.objects.filter(key=url_key)
    params = {}
    for i in params_list:
        params[i.item] = i.value
    if(is_jsonp):
        return j.dic_json_p(params,callback_name,'utf-8')
    else:
        return j.dic(params,'utf-8')

def __return_json_error(msg, is_jsonp=False, cb_name='callback'):

    if is_jsonp:
        return j.dic_json_p({ 'error': msg },cb_name, 'utf-8')

    else:
        return j.dic({ 'error': msg },'utf-8')

def _restful_query(url_key, data, request_content, is_jsonp=False, cb_name='callback'):

    data['act'] = 'query'

    form_key = api.api_key(request_content)

    if not form_key.is_valid():
        return __return_all(url_key, cb_name, is_jsonp)
    else:
        try:
            key = form_key.cleaned_data['key']

            data['key'] = key

            _value = resource_restful_item.objects.get(key=url_key, item=key).value

            data['state'] = 'success'

            data[key] = _value

            if(is_jsonp):
                return j.dic_json_p(data,cb_name,'utf-8')
            else:
                return j.dic(data,'utf-8')

        except Exception as ee:

            if is_jsonp:
                return j.dic_json_p({'error':'该键不存在 key not found.' + str(ee) if not settings.RELEASE else '' }, cb_name, 'utf-8')
            else:
                return j.dic({'error':'该键不存在 key not found.' + str(ee) if not settings.RELEASE else ''}, 'utf-8')

def _restful_add(url_key, data, request_content, is_jsonp=False, cb_name='callback'):

    data['act'] = 'add'

    form_key = api.api_key(request_content)

    form_value = api.api_value(request_content)

    if not form_key.is_valid() or not form_value.is_valid():
        return __return_json_error('parameter : key and value are both required , add this after parameters &key=somekey&value=somevalue', is_jsonp, cb_name)

    key = form_key.cleaned_data['key']

    value = form_value.cleaned_data['value']

    data['key'] = key

    t = resource_restful_item.objects.filter(key=url_key, item=key)

    if len(t) != 0:
        return __return_json_error(url_key + ' :: ' + key + ' is already exist.', is_jsonp, cb_name)

    resource_restful_item.objects.create(key=url_key, item=key, value=value)

    data['state'] = 'success'

    if not is_jsonp:
        return j.dic(data,'utf-8')
    else:
        return j.dic_json_p(data,cb_name,'utf-8')

def _restful_delete(url_key, data, request_content, is_jsonp=False, cb_name='callback'):

    data['act'] = 'delete'

    form_key = api.api_key(request_content)

    if not form_key.is_valid():
        return __return_json_error('parameter : key is and required , add this after parameters &key=somekey', is_jsonp, cb_name)

    key = form_key.cleaned_data['key']

    data['key'] = key

    t = resource_restful_item.objects.filter(key=url_key, item=key)

    if len(t) == 0:
        return __return_json_error(url_key + ' :: ' + key + ' is not exist.', is_jsonp, cb_name)

    for item in t:
        item.delete()

    data['state'] = 'success'

    if is_jsonp:
        return j.dic_json_p(data,cb_name,'utf-8')
    else:
        return j.dic(data,'utf-8')

def _restful_modify(url_key, data, request_content, is_jsonp=False, cb_name='callback'):

    data['act'] = 'modify'

    form_key = api.api_key(request_content)

    form_value = api.api_value(request_content)

    if not form_key.is_valid() or not form_value.is_valid():
        return __return_json_error('parameter : key and value are both required , add this after parameters &key=somekey&value=somevalue', is_jsonp, cb_name)

    key = form_key.cleaned_data['key']

    value = form_value.cleaned_data['value']

    data['key'] = key

    t = resource_restful_item.objects.filter(key=url_key, item=key)

    if len(t) == 0:
        return __return_json_error(url_key + ' :: ' + key + ' is not exist.', is_jsonp, cb_name)

    t[0].value = value

    t[0].save()

    data['state'] = 'sucess'

    if is_jsonp:
        return j.dic_json_p(data,cb_name,'utf-8')
    else:
        return j.dic(data,'utf-8')

