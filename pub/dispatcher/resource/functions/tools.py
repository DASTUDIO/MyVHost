# coding=utf-8
import pub.functions.coder as c
import pub.functions.token as t
from pub.forms.functions import *
import pub.response.json as j
from urllib import parse


def resource_functions_token(request,url_key):
    try:
        res = {}
        res['state'] = 'error'
        if request.GET or request.POST:
            form = None
            if request.GET:
                form = functions_resource_token(request.GET)
            else:
                form = functions_resource_token(request.POST)

            if not form.is_valid():
                return _token_params_err(res,'需要参数type:alpha/digit,length:0-256')

            type = form.cleaned_data['type']
            length = form.cleaned_data['length']

            if length>256:
                res['message'] = 'length 超过范围'
                return j.dic(res,'utf-8')

            if type =='alpha':
                 res['result'] = t.alpha_token(length)
            elif type=='digit':
                res['result'] = t.digit_token(length)
            else:
                return _crypto_params_err(res,'未知的type类型')

            res['state'] = 'success'
            return j.dic(res,'utf-8')
        else:
            raise Exception('需要参数type:alpha/digit,length:0-256')
    except Exception as e:
        return j.err(e,'utf-8')
def _token_params_err(res,msg):
    res['message'] = msg
    return j.dic(res, 'utf-8')

def resource_functions_crypto(request,url_key):
    global default_password
    try:
        res = {}
        res['state'] = 'error'
        if request.GET or request.POST:
            form = None
            pass_form = None
            size_form = None
            digit_form = None

            if request.GET:
                form = functions_resource_crypto(request.GET)
                pass_form = functions_resource_crypto_pwd(request.GET)
                noise_form = functions_resource_crypto_noise(request.GET)
                digit_form = functions_resource_crypto_digit(request.GET)
            else:
                form = functions_resource_crypto(request.POST)
                pass_form = functions_resource_crypto_pwd(request.POST)
                noise_form = functions_resource_crypto_noise(request.POST)
                digit_form = functions_resource_crypto_digit(request.POST)
            if not form.is_valid():
                return _crypto_params_err(res,'需要参数act:encrypt/decrypt加解密标识,(string)data加解密源数据,[可选]password使用密码,[可选]noise百分比如100即大小翻倍')

            act = form.cleaned_data['act']
            data = form.cleaned_data['data']

            password = ""

            if act == 'encrypt':
                noise = 0
                digit = 0
                if pass_form.is_valid():
                    password = pass_form.cleaned_data['password']
                if noise_form.is_valid():
                    noise = noise_form.cleaned_data['noise']
                if digit_form.is_valid():
                    digit = digit_form.cleaned_data['digit']

                raw_result = c.encode(data,password,c.code_encoding,noise)

                res['result'] = raw_result

                if digit == 'yes':
                    res['result'] = c.to_dirty_digit(c.get_digit(raw_result.encode(c.code_encoding)),int(len(data)*100*0.25))

                res['state'] = 'success'
                return j.dic(parse.urlencode(res),'utf-8')

            elif act=='decrypt':
                data = parse.unquote(data)
                password = ""
                try:
                    digit = 0
                    if pass_form.is_valid():
                        password = pass_form.cleaned_data['password']
                    if digit_form.is_valid():
                        digit = digit_form.cleaned_data['digit']
                    if digit=='yes':
                        data = c.reverse_get_digit(c.from_dirty_digit(data))

                    res['result'] = c.decode(data,password)
                    res['state'] = 'success'
                    return j.dic(res, 'utf-8')
                except:
                    #return j.err(eee)
                    return _crypto_params_err(res,'不是正确的密文或密码，无法解密')
            else:
                return _crypto_params_err(res,'未知的act类型')

        else:
            return _crypto_params_err(res,'需要参数act:encrypt/decrypt加解密标识,(string)data加解密源数据,[可选]password使用密码,[可选]noise百分比如100即大小翻倍')
    except Exception as e:
        return j.err(e)
def _crypto_params_err(res,msg):
    res['message'] = msg
    return j.dic(res,'utf-8')