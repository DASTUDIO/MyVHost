# coding=utf-8
import pub.settings as settings
import pub.models as db



def get_volume_token(create_type,token):
    if token == '':
        return 0
    try:
        params = {}
        params['type'] = create_type
        params['key'] = token
        permission = db.token.objects.get(**params)
        return permission.value
    except:
        return 0

def get_volume_username_token_create_resource(request, create_type, token=''): # return (volume,username,token)
    if request.user.is_authenticated:
        try:
            params = {}
            params['username'] = request.user.username
            params['permission'] = create_type
            permission = db.user_permission.objects.get(**params)
            return (permission.volume,params['username'],'')
        except:
            return (get_volume_token(create_type, token),'',token)
    else:
        return (get_volume_token(create_type, token),'',token)


# 检测存不存在该权限码的权限
def check_user_permission(request,permission_code):

    # 只用于登陆才检测 一般是创建
    if not request.user.is_authenticated():
        return False

    permission_list = db.api_resource_item.objects.filter(username=request.user.username)

    for item in permission_list:
        if item.permission == permission_code:
            if item.volume > 0:
                return True

    return False

def check_owner(request,owner_username):
    if request.user.is_authenticated():
        return request.user.username == owner_username
    return False


def check_writeable(request, owner_username, permission_code,
                    verify_token_key='', verify_token_value=settings.UNIVERSAL_TOKEN,
                    verify_item_key='', verify_item_value='', verify_dict={}):

    # 所有者可写
    if check_owner(request,owner_username):
        return True

    # 全局可写许可 可写
    if (permission_code == settings.PERMISSION_READ_AND_WRITE) \
            or (permission_code == settings.PERMISSION_WRITE_ONLY) \
            or (permission_code == settings.PERMISSION_WRITE_AND_VERIFY_READ)\
            or (permission_code == settings.PERMISSION_WRITE_AND_IVERIFY_READ):
        return True

    # 全局不可写
    if (permission_code == settings.PERMISSION_READ_ONLY):
        return False

    # 需要验证token
    if (permission_code == settings.PERMISSION_READ_AND_VERIFY_WRITE) \
            or (permission_code == settings.PERMISSION_VERIFY_READ_AND_VERIFY_WRITE):
        if verify_token_key == verify_token_value:
            return True

    # 条目验证 用于 API 或者 Template 资源
    if (permission_code == settings.PERMISSION_IVERIFY_READ_AND_IVERIFY_WRITE) \
        or (permission_code == settings.PERMISSION_READ_AND_IVERIFY_WRITE):
        if verify_item_key == '':
            return False
        if not verify_item_key in verify_dict:
            return False
        if verify_dict[verify_item_key] == verify_item_value:
            return True

    return False


def check_readable(request, owner_username, permission_code,
                    verify_token_key='', verify_token_value=settings.UNIVERSAL_TOKEN,
                    verify_item_key='', verify_item_value='', verify_dict={}):
    # 所有者可读
    if check_owner(request, owner_username):
        return True

    # 全局可写许可 可读
    if (permission_code == settings.PERMISSION_READ_AND_WRITE) \
            or (permission_code == settings.PERMISSION_READ_ONLY) \
            or (permission_code == settings.PERMISSION_READ_AND_VERIFY_WRITE) \
            or (permission_code == settings.PERMISSION_READ_AND_IVERIFY_WRITE):
        return True

    # 全局不可写
    if (permission_code == settings.PERMISSION_WRITE_ONLY):
        return False

    # 需要验证token
    if (permission_code == settings.PERMISSION_WRITE_AND_VERIFY_READ) \
            or (permission_code == settings.PERMISSION_VERIFY_READ_AND_VERIFY_WRITE):
        if verify_token_key == verify_token_value:
            return True

    # 条目验证 用于 API 或者 Template 资源
    if (permission_code == settings.PERMISSION_IVERIFY_READ_AND_IVERIFY_WRITE) \
            or (permission_code == settings.PERMISSION_WRITE_AND_IVERIFY_READ):
        if verify_item_key == '':
            return False
        if not verify_item_key in verify_dict:
            return False
        if verify_dict[verify_item_key] == verify_item_value:
            return True

    return False


