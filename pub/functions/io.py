# coding=utf-8
import os,re,subprocess

# --------------------------------
# make sure these fields as same as fields in src/settings.py

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_ROOT = os.path.join(BASE_DIR,'static')

STATIC_URL = '/r'

TEMPLATE_ROOT = os.path.join(BASE_DIR,'templates')

EXE_ROOT = os.path.join(BASE_DIR,'exe')

# --------------------------------

def url_join(urla,urlb):
    return str(urla) + '/' + str(urlb)

def gen_template_path(username,resource_name,token):
    file_path = os.path.join(TEMPLATE_ROOT,username,resource_name+token)
    record_path = os.path.join(username,resource_name + token)
    url_path = url_join(username,resource_name + token)
    return (file_path,record_path,url_path)

# from record
def get_template_path(record_path):
    file_path = os.path.join(TEMPLATE_ROOT,record_path)
    return file_path


def gen_static_path(username,resource_name,token):
    file_path = os.path.join(STATIC_ROOT,username,resource_name+token)
    record_path = os.path.join(username,resource_name+token)
    url_path = url_join(STATIC_URL,url_join(username,resource_name+token))
    return (file_path,record_path,url_path)

def get_static_path_by(record_path):
    file_path = os.path.join(STATIC_ROOT,record_path)
    return file_path

# need fix -  os path to urlpath       
def get_static_url(record_path):
    url_path = url_join(STATIC_URL,record_path)
    return url_path

def gen_exe_path(username,resource_name,token):
    file_path = os.path.join(EXE_ROOT,username,resource_name+token)
    record_path = os.path.join(username,resource_name+token)
    return (file_path,record_path)

def get_exe_path(record_path):
    file_path = os.path.join(EXE_ROOT,record_path)
    return file_path


def check_folder(path):
    return os.path.exists(path)

def check_file(filepath):
    return os.path.isfile(filepath)


def mkdir(path):
    if not check_folder(path):
        return os.makedirs(path)
    else:
        return -1

def rmdir(path):
    if check_folder(path):
        return os.removedirs(path)
    else:
        return -1

def chdir(path):
    return os.chdir(path)

def remove_file(path):
    if check_file(path):
        return os.remove(path)
    else:
        return -1

def rename_file(ori,target):
    if check_file(ori):
        return os.rename(ori,target)
    else:
        return -1


def replace_content(path,pattern,repl):
    with open(path) as read_file , open(path+'.swap','w') as writed_file:
        for line in read_file:
            line = re.sub(pattern,repl,line)
            writed_file.write(line)
        read_file.close()
        writed_file.close()
    remove_file(path)
    rename_file(path+'.swap',path)

def write_file(path,content):
    fhandler = open(path,'w')
    fhandler.write(content)
    fhandler.close()


def gen_exe(path,sourcecode,reference=[]):
    r = ""    
    if len(reference)>0:
        r = reference[0]
        if len(reference)>1:
            for i in len(reference)-1 :
                r += ","+reference[i]
    cmd = "mono /mono/EG.exe -i"+sourcecode+" -i "+path+" -r "+r
    return cmd
    #return subprocess.Popen(cmd,shell=True)


#write_file('test.txt','i love you')
print(gen_exe_path('name','resoucename','token1312$%#'))

'''
def upload(request,form_name,path):
    if request.method == 'POST':
        try:
            obj = request.FILES.get(form_name)
            with open(path,'wb') as f
                for chunk in obj.chunks():
                    f.write(chunk)
                f.close()
                return 1
        except:
            return -1
    return 0
'''





#print(get_template_path('record_path'))
#print(get_static_path('record_path'))
#print(get_static_url('record_path'))

#mkdir(os.path.join(BASE_DIR,'io/testdir'))
#chdir(os.path.join(BASE_DIR,'io/testdir'))

#f1 = open('1.txt','w')
#f1.write('123123')
#f1.close()
#replace_content(os.path.join(BASE_DIR,'io/testdir','1.txt'),'.*?','456456')



















