# coding=utf-8
import pub.functions.coder as c
import pub.functions.token as k
import pub.functions.time as t
import pub.settings as s

# token验证是否使用过 能否翻译验证是不是正确的票

def get_register_ticket_by_days(days):
    seconds = days*24*60*60
    token=k.alpha_token(7)
    #print(token)
    return (c.base64_plus_encode_str(token+str(seconds),s.TICKET_SAFE_CODE))[::-1]

def get_days_by_ticket(ticket):
    try:
        r = c.base64_plus_decode_str(ticket[::-1],s.TICKET_SAFE_CODE)
        #token = r[0:7]
        r = int(r[7:])
        r = r/60/60/24
        return int(r)
    except:
        return -1

# erase token
def use_ticket(ticket):
    None

ss=get_register_ticket_by_days(1000000)
print(ss)
dd = get_days_by_ticket(ss)
print(dd)