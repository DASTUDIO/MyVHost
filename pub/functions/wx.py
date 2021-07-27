# coding=utf-8
import hashlib


def verify(signature,timestamp,nonce,echostr):

    token = ""
    list = [token,timestamp,nonce]
    list.sort()
    sha1 = hashlib.sha1()
   # map(sha1.update,list)
    
    res = ""
    for item in list:
        res=res+item

    sha1.update(res.encode('utf-8'))

    hashcode = sha1.hexdigest()
    
    print(hashcode)    
    
    if(hashcode == signature):
        return echostr
    else:
        return "tk: "+token+"ts"+timestamp+"nonce"+nonce +  "-1 "+hashcode

if __name__ == "__main__":
    print(verify('123','456','789','000',))





