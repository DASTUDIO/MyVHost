# coding=utf-8
import random

# -------------------------------------

# default alpha token length

alpha_token_length = 16

# default digit token length

digit_token_length = 32

# default sms token length

sms_token_length = 6

# -------------------------------------


alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

digit =['0','1','2','3','4','5','6','7','8','9']


alpha_max_index = 51

digit_max_index =9


def alpha_token(length=-1):
    _length = alpha_token_length
    if not length == -1:
        _length = length
    result = []
    for time in range(0,_length):
        result.append(alpha[random.randint(0,alpha_max_index)])
    return ''.join(result)

def digit_token(length=-1):
    _length = digit_token_length
    if not length == -1:
        _length = length
    result = []
    for time in range(0,_length):
        result.append(digit[random.randint(0,digit_max_index)])
    return ''.join(result)

def sms_token(length=-1):
    _length = sms_token_length
    if not length == -1:
        _length = length
    result = []
    for time in range(0,sms_token_length):
        result.append(digit[random.randint(0,digit_max_index)])
    return ''.join(result)

def random_0_to_1():
    return random.random()




