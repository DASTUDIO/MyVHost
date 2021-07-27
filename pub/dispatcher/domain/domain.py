# coding=utf-8
import pub.tables.map.domain as d
import pub.dispatcher.resource.resource as r
import pub.response.error as e
import pub.settings as s
import pub.dispatcher.file.file as f
from urllib.parse import urlparse
from socket import gethostbyname
import pub.response.json as j

map = {}

def cast(url_key, path):
    global map
    map.update({url_key:path})

try:
    from .cache import do
    do()
except:
    pass

# dispatch
def dispatch(request, domain, raw_url):                         # 原始的域名后url_key 没有去处第二个/

    try:                                                        # 为了测试表里的函数能不能用
        if domain in map:
            return map[domain](request, domain, raw_url)
        else:
            raise LookupError()                                 # 为了跳到except里
    except:
        try:                                                    #这个try用来判断有类型记录没
            # 文件目录穿透
            if raw_url[0:7] == s.UPLOAD_URL + '/':
                return f.dispatch(request,raw_url[6:])

            resource_key_list = d.domain_to_key.objects.filter(domain=domain)
            if len(resource_key_list) == 0:
                raise Exception()

            # 返回 resource
            for item in resource_key_list:

                if str(item.url) == raw_url:
                    return r.dispatch(request,item.key)

            return e.page(request,404,'找不到该页面','URL:'+raw_url+'是无效的')

        except :
            try:
                res = d.domain_to_user.objects.get(domain=domain)

                if not res.token == '':

                    _domain = 'http://' + res.token + '.' + domain

                    domain = str(urlparse(_domain).hostname)

                    ip = str(gethostbyname(domain))

                    if ip == s.DOMAIN_VERIFY_IP:

                        res.token = ''

                        res.save()

                        return e.page(request,766,'已绑定的域名','这个域名已经成功绑定，目前尚未被使用')
                    else:
                        return e.page(request, 766, '未绑定的域名', '这个域名已经成功解析至本服务器，尚未被绑定，如已经提交绑定请稍等解析')
                else:
                    return e.page(request,766,'已绑定的域名','这个域名已经成功绑定，目前尚未被使用')

            except:
                return e.page(request, 766, '未绑定的域名', '这个域名已经成功解析至本服务器，尚未被绑定，如已经提交绑定请稍等解析')





