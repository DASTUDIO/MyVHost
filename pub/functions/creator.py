# coding=utf-8
import pub.settings as settings
import pub.models as db
import pub.functions.io as io
import pub.functions.permission as permission
import pub.response.error as e
import  os


def _update_permission(_volume, _username, _token):
    if _username == '':
        if _volume == 1:
            try:
                #db.token.objects.filter(key=_token).delete()
                t = db.token.objects.get(key=_token)
                t.value = int(t.value) - 1
                t.save()
                return e.json_err(1)
            except:
                return e.json_err(2)
        else:
            try:
                t = db.token.objects.get(key=_token)
                t.value = int(t.value) - 1
                t.save()
                return e.json_err(1)
            except:
                return e.json_err(2)
    else:
        if _volume == 1:
            try:

                up = db.user_permission.objects.get(username=_username)
                up.volume = up.volume - 1
                up.save()
                return e.json_err(1)
            except:
                return e.json_err(3)
        else:
            try:
                up = db.user_permission.objects.get(username=_username)
                up.volume = up.volume - 1
                up.save()
                return e.json_err(1)
            except:
                return e.json_err(3)

def _write_file(file_name,html,_volume,_username,_token):
    try:
        path = str(settings.TEMPLATE_PATH) + '/' + str(file_name) +'.html'

        path = os.path.join(settings.TEMPLATE_PATH,'custom_html',str(file_name)+'.html')
        #return e.http_text(io.check_file(path))

        if io.check_file(path):
            return e.json_err(4)
        else:
            try:
                io.write_file(path,html)
                return _update_permission(_volume,_username,_token)

            except Exception as err:
                return e.http_text(err)

    except Exception as err:
        return e.http_text(err)




def resource_custom_html(request,folder,post_url):

    if not request.method == 'POST':
        return e.json_err(5)
        #return e.http_text(post_url[1:])

    token = post_url[1:]

    try:
        #data = request.POST.get('data')

        #data_obj = j.loads(data)

        #html = data_obj.html

        #file_name = data_obj.filename

        html = request.POST.get('html')

        file_name = request.POST.get('filename')

        #return e.http_text(html+'&'+file_name)

        _volume,_username,_token = \
            permission.get_volume_username_token_create_resource(
                request,settings.CREATE_CUSTOM_HTML_RESOURCE,token)

        _volume = int(_volume)

        if _volume <= 0:
            return e.json_err(0)

        # return e.http_text(_volume)

        return _write_file(file_name,html,_volume,_username,_token)

        #    return _update_permission(_volume, _username, _token)
        # else:
        #   return e.json_err(4)

        # return e.http_text('ok')

    except Exception as ee:
        return e.json_err_text(ee)


# 加时
def add_expire_time(request,resource_key,token=''):
    return 0

def resource_template_html(request,):
    db.template_resource_item.objects.create()
    return 0

def resource_api():
    return 0


def resouce_template_item():
    return 0


def resource_api_item():
    return 0

def ad():
    return 0

def order():
    return 0


