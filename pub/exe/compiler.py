# coding=utf-8
import os,subprocess,time
import pub.settings as s
import pub.functions.token as t

tmp_path = os.path.join(s.EXE_PATH,'tmp')
compiler = os.path.join(s.EXE_PATH,'EG.exe')
reference = os.path.join(s.EXE_PATH,'src.pub.dll')

def compile(code):
    _clean_tmp()
    filename = _get_random_file_name('.cs')
    code_path = os.path.join(tmp_path,filename)
    f = open(code_path,'w+')
    f.write(code)
    f.close()
    exe_path = os.path.join(tmp_path, _get_random_file_name('.exe'))
    cmd = "mono "+ compiler +" -i "+code_path+" -o "+exe_path+" -r "+reference
    print(cmd)
    subprocess.Popen(cmd,shell=True)
    return exe_path


def _get_random_file_name(postfix):
    filename = str(int(time.time()))+t.alpha_token(5)+postfix
    if os.path.exists(os.path.join(tmp_path,filename)):
        return _get_random_file_name(postfix)
    return filename

def _clean_tmp():
    for root,dirs,files in os.walk('./'):
        for name in files:
            if name.endswith('.cs') or name.endswith('.tmp'):
                os.remove(os.path.join(root,name))
    for root,dirs,files in os.walk('./tmp/'):
        for name in files:
            if name.endswith('.cs') or name.endswith('.mdb'):
                os.remove(os.path.join(root,name))

#c = 'using System;class A{static void Main(string[] args){Console.Write("hello");Console.ReadLine();}}'
#c='using System;using src.pub.network;namespace nettest{class Program{static public void accept(string client_token){Console.WriteLine(client_token);}static public string receive(string client_token, string data){Console.WriteLine(client_token+":"+data);return null;}static void Main(string[] args){network.TCP_Server_Start(accept,receive,7097);network.Keep_Alive();}}}'
#print(compile(c))