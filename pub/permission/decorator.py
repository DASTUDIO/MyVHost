# coding=utf-8

from pub.permission.user import is_logged
import pub.response.error as e


# 装饰器  page
def require_login(func):

    def callback(r,f,p):
        try:
            if(is_logged(r)):
                return func(r,f,p)
            else:
                return e.page_shutdown(r,101,"需要登录")
        except Exception as err:
            return e.page(r, 101,err)

    return callback

