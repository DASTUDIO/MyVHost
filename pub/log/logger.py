# coding=utf-8
import io
import pub.settings as s

def log(msg:str):
    f = open(s.LOG_PATH,'a')
    f.write(msg)
    f.close()
