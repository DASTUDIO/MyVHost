# coding=utf-8
from pub.tables.resources import *
from pub.tables.map.domain import *
from pub.tables.cache.token import *
from pub.tables.map.files import *
from pub.tables.user import *
from pub.tables.cache.suspend import *
from pub.tables.notice import *
from pub.tables.template import *
from pub.tables.comments import *

reg = admin.site.register

# resource
reg(resource_to_user,resource_to_user_decoration)

reg(resource_type, resource_type_decoration)
reg(resource_state,resource_state_decoration)

reg(resource_customed,resource_customed_decoration)
reg(resource_templated,resource_templated_decoration)
reg(resource_iframe,resource_iframe_decoration)
reg(resource_link,resource_link_decoration)
reg(resource_restful,resource_restful_decoration)
reg(resource_restful_item, resource_restful_item_decoration)

# domain
reg(domain_to_key,domain_to_key_decoration)

# token
reg(token,token_decoration)

# files
reg(file_key_to_path,file_key_to_path_decoration)

# auth_user
reg(auth_user,auth_user_decoration)

# supend
reg(cache_suspend,cache_suspend_decoration)

# user permission
reg(user_permission,user_permission_decoration)

# template
reg(template,template_decoration)

# resource info
reg(resource_info,resource_info_decoration)

# domain user
reg(domain_to_user,domain_to_user_decoration)

# file
reg(file_hash_to_key,file_hash_to_key_decoration)
reg(file_key_to_user,file_key_to_user_decoration)

# resource permission
reg(resource_permission,resource_permission_decoration)

# user info
reg(user_info,user_info_decoration)

# template info
reg(template_info,template_decoration)

# notices
reg(notice,notice_decoration)

# comments
reg(user_comments,user_comments_decoration)
reg(user_comments_likes_map,user_comments_likes_map_decoration)