# coding=utf-8
import pub.settings as settings
import pub.dispatcher.folder.folder as folder
import pub.dispatcher.domain.domain as domain
import pub.dispatcher.resource.resource as resource
from pub.response.wrap import page
import pub.functions.token as token
import time

def dispatch(request, raw_url):       # raw_url 不包含域名，不包含域名后的'/'，也不包含?x=1这类get参数

    # Domain
    domain_name = request.META['HTTP_HOST']

    if domain_name not in settings.DOMAIN:
        return domain.dispatch(request, domain_name, raw_url)

    # Main Site Pages
    index = raw_url.find('/')         # 第一层目录的索引

    folder_url_length = 0             # 是否主页

    folder_url = raw_url              # 第一层目录名 (src.pub/xxx/ -> xxx)

    url_after_folder = ''             # 目录后的url内容 (src.pub/xxx/yyy/ -> yyy)

    if index != -1:                   # 赋值
        folder_url = raw_url[0:index]
        url_after_folder = raw_url[index:]
        folder_url_length = len(folder_url.replace('/',''))

    if folder_url_length == 0:        # 一级分发
        if raw_url.replace('/', '') == '':
            return page(request,'news.html')
        else:                         # 一级资源 shortlink
            return resource.dispatch(request, folder_url)
    else:
        return folder.dispatch(request, folder_url , url_after_folder[1:])
