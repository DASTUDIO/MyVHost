# coding=utf-8
import pub.response.wrap as wrapper
from .domain import cast

def do():
    cast("cacu.mxd.wiki", lambda request,domain,url_key: wrapper.page(request, 'maple_caculator.html'))
