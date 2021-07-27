#import os
import hashlib

def get_hashcode(path):
    try:
        f = open(path,'rb')
        content = f.read()
    finally:
        if f:
            f.close()
            m = hashlib.md5()
            m.update(content)
            return m.hexdigest()
        else:
            raise Exception('没有读到文件')

#print(get_hashcode(os.path.abspath(__file__)))