# coding=utf-8
import pub.response.wrap.jump as jump
from .resource import cast

def do():
    #  for custom delegate
    cast('favicon.ico',(lambda request,url_key:jump('/r/favicon.ico')))
