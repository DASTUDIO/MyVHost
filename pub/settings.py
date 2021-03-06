# coding=utf-8
import os


RELEASE = False

THEME = 'whiteconsole'                                  # whiteconsole / superadmin

DOMAIN = ['lab.zhangxinhao.com','localhost','127.0.0.1']

# 用于验证域名是否解析过来了
IP = ['111.231.19.116']
# 绑定用户做的解析
DOMAIN_VERIFY_IP = '47.254.41.44'

CACHE_SIZE = 1024

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(BASE_DIR,'static')

STATIC_URL = '/r'

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

LOG_PATH = os.path.join(BASE_DIR,'logs')

EXE_PATH = os.path.join(BASE_DIR, 'exe')

DEFAULT_IFRAME_TITLE = '微转发 IFRAME'

CUSTOMED_HTML_PATH = os.path.join(TEMPLATE_PATH,'custom')

TICKET_SAFE_CODE = 12

UPLOAD_FILE_PATH = os.path.join(STATIC_ROOT,'upload')

UPLOAD_URL = 'upload'
UPLOAD_PROVIDER = 'r/upload'

PAGE_SIZE = 8
TEMPLATE_PAGE_SIZE = 4

# 前端首页 瀑布流卡片的行长度
CARD_ROW_LENGTH = 16



WX_KEY = ''

WX_SECRET = ''



SESSION_CLIENT = 'client_id'
SESSION_LOGIN = 'session_login'
SESSION_TIME_EXPIRE = 7200
SESSION_RECYCLE_COUNT_INTERVAL = 2

RESOURCE_PROTECTION_KEY = ['token','crypto']

AUTH_PROVIDER_GITHUB = 3
AUTH_PROVIDER_WEIXIN = 2
AUTH_PROVIDER_ALIPAY = 1



CACHE_TYPE_LOGIN = 0
CACHE_TYPE_TOKEN = 1
CACHE_TYPE_LOGIN_SESSION_TO_USER = 2
CACHE_TYPE_LOGIN_CLIENT_TO_SESSION = 3
CACHE_TYPE_LOGIN_CLIENT_TO_RECYCLE_TIME = 4

CACHE_MODE = 1
CACHE_MODE_RAM = 0
CACHE_MODE_DB =1

RESOURCE_CUSTOM_TYPE_NORMAL = 0
RESOURCE_CUSTOM_TYPE_TEMPLATE =1


LOG_PATH = "/home/log/1.txt"

TOKEN_SMS_VERIFICATION = 0
TIME_SMS_VERIFICATION = 180
# resource type
RESOURCE_TYPE_CUSTOMED = 1
RESOURCE_TYPE_TEMPLATED = 2
RESOURCE_TYPE_RESTFUL_API = 3
RESOURCE_TYPE_SHORT_LINK = 4
RESOURCE_TYPE_IFRAME = 5
RESOURCE_TYPE_EXE = 6
RESOURCE_TYPE_PDF = 7
# resource PERMISSION
RESOURCE_PERMISSION_EVERY_ONE = 0
RESOURCE_PERMISSION_LOGGED_ONLY = 1
RESOURCE_PERMISSION_SELF_ONLY =2
#resource state
RESOURCE_STATE_PLAY = 0
RESOURCE_STATE_PAUSE =1
RESOURCE_STATE_STOP = 2
RESOURCE_STATE_PREPARE_TO_DELETE = 3
# api accessibility
ACCESSIBILITY_PUBLIC = 0
ACCESSIBILITY_PRIVATE = 1
ACCESSIBILITY_TOKEN = 2
ACCESSIBILITY_LOGIN = 3
ACCESSIBILITY_LOGIN_OR_TOKEN = 4
# # USER PERMISSION
# PERMISSION_READ_AND_WRITE = 0 # w r
#
# PERMISSION_WRITE_ONLY = 1 # w        Add Only
# PERMISSION_READ_ONLY = 2 # r
#
# PERMISSION_READ_AND_VERIFY_WRITE = 3 # r vw
# PERMISSION_WRITE_AND_VERIFY_READ = 4 # w vr
#
# PERMISSION_VERIFY_READ_AND_VERIFY_WRITE = 5 # vw vr
# PERMISSION_IVERIFY_READ_AND_IVERIFY_WRITE = 6
#
# PERMISSION_WRITE_AND_IVERIFY_READ = 7
# PERMISSION_READ_AND_IVERIFY_WRITE = 8
# user permission
CREATE_TEMPLATE_RESOURCE = 10000
CREATE_CUSTOM_HTML_RESOURCE = 10001
# ???
EXE_INFO_PAGE = 'exe_info.html'
UNIVERSAL_TOKEN = 'this#is#a#test#token'
UNIVERSAL_ITEM_VALUE = 'this#is#a#universal#item#value'


ALIPAY_APPID = ''

ALIPAY_PUB_KEY = '''
'''

ALIPAY_MY_PRI_KEY = '''
'''

ALIPAY_MY_PUB_KEY='''
'''



# github
GITHUB_CLIENT_ID = ''
GITHUB_CLIENT_SECRETS = ''
GITHUB_REDIRECT_URL = 'https://lab.zhangxinhao.com/auth_github'
