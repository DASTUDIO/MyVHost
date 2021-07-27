# coding=utf-8
from django.http import FileResponse
from pub.response.error import page
import pub.settings as s
from pub.tables.map.files import *
import os,time
import pub.functions.token as token
import pub.tables.map.files as files
import pub.response.json as j
import pub.strings as strings
import pub.permission.decorator as permission
import pub.functions.hash as hash
import pub.permission.file as permission_file

map = {}

def cast(url_key, path):
    global map
    map.update({url_key:path})

try:
    from .cache import do
    do()
except:
    pass

def dispatch(request,url_key):

    try:                                                        # 为了测试表里的函数能不能用
        if url_key in map:
            file_location = map[url_key]
            file = open(file_location, 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="' + url_key
            return response
        else:
            raise LookupError('key not register')               # 为了跳到except里
    except Exception as e:              # databases
        try:
            path = file_key_to_path.objects.get(key=url_key).path
            file = open(path, 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="' + url_key
            return response
        except:
            #dic = {}
            #dic['uploaded'] = '0'
            #dic['url'] = ''
            #return j.dic(dic)
            return page(request,404,"找不到文件","找不到映射为\'"+url_key[1:]+"\'的文件，请检查是否URL正确。" )


def upload(request, url_key):

    if request.method != 'POST':

        return dispatch(request, url_key)

    # 上传权限
    try:
        if not permission.is_logged(request):
            return j.err("需要登录", 'utf-8')
    except:
        return j.err("需要登录", 'utf-8')

    # 上传
    try:
        obj = request.FILES.get('file')

        if not obj:
            return j.err('no file param')

        userid = request.session.get('userid')

        filename = token.alpha_token(7) + str(int(time.time()))

        path = os.path.join(s.UPLOAD_FILE_PATH, filename)

        url = strings.HTTP_OR_HTTPS + request.META['HTTP_HOST'] + '/' + s.UPLOAD_PROVIDER + '/' + filename  # for return

        with open(path, 'wb') as file:

            for chunk in obj.chunks():
                file.write(chunk)
            file.close()

            # 确保文件名唯一
            while not permission_file.is_valid_key(filename):
                filename = token.alpha_token(7) + str(int(time.time()))

            # 重复利用
            file_hash = hash.get_hashcode(path)

            try:
                res = files.file_hash_to_key.objects.get(hash=file_hash)
                res.reference += 1
                res.save()

                os.remove(path)

                dic = {}
                dic['uploaded'] = 'success'
                dic['url'] = strings.HTTP_OR_HTTPS + request.META['HTTP_HOST'] + '/' + s.UPLOAD_PROVIDER + '/' + res.key

            except:

                files.file_hash_to_key.objects.create(hash=file_hash,key=filename)

                dic = {}
                dic['uploaded']='success'
                dic['url'] = url

                files.file_key_to_path.objects.create(key=filename, path=path)
                files.file_key_to_user.objects.create(key=filename, userid=userid)

        return j.dic(dic)

    except Exception as e:

        dic={}

        dic['error']= str(e)

        return j.dic(dic)

