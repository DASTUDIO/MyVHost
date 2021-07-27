# coding=utf-8
from .file import cast
import pub.settings as settings
import os

# 1.path 地址前 别加 / 否则会被认为是根目录 2.url_key 前也别加 / 就像 folder
def do():
    cast("cdn/theme/whiteconsole/webfonts/material_icons.woff2",
         _pub_path_join("static/theme/whiteconsole/webfonts/material_icons.woff2"))

    cast("cdn/theme/whiteconsole/webfonts/fa-regular-400.eot",
         _pub_path_join("static/theme/whiteconsole/webfonts/fa-regular-400.eot"))

    cast("cdn/theme/whiteconsole/webfonts/fa-regular-400.ttf",
         _pub_path_join("static/theme/whiteconsole/webfonts/fa-regular-400.ttf"))

    cast("cdn/theme/whiteconsole/webfonts/fa-regular-400.woff",
         _pub_path_join("static/theme/whiteconsole/webfonts/fa-regular-400.woff"))

    cast("cdn/theme/whiteconsole/webfonts/fa-regular-400.woff2",
         _pub_path_join("static/theme/whiteconsole/webfonts/fa-regular-400.woff2"))


def _pub_path_join(path):
    return os.path.join(settings.BASE_DIR,path)