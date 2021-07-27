#coding=utf-8
import random, re, base64

key = {}

noise = ['8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '+', '-', '=', '/', '<', '>', ';', '(', ')', '*', '&', '^', '%', '$', '#', '@', '!', '~']

key['0'] = ['1', '3', '2', '4', '6', '5', '7', '0']
key['1'] = ['2', '3', '4', '5', '6', '7', '0', '1']
key['2'] = ['3', '4', '5', '6', '7', '0', '1', '2']
key['3'] = ['4', '5', '6', '7', '0', '1', '2', '3']
key['4'] = ['5', '6', '7', '0', '1', '2', '3', '4']
key['5'] = ['6', '7', '0', '1', '2', '3', '4', '5']
key['6'] = ['7', '0', '1', '2', '3', '4', '5', '6']
key['7'] = ['0', '1', '2', '3', '4', '5', '6', '7']
key['8'] = ['1', '3', '4', '5', '6', '7', '0', '2']
key['9'] = ['2', '3', '1', '4', '6', '5', '7', '0']
key['a'] = ['3', '2', '1', '4', '6', '5', '7', '0']
key['b'] = ['4', '2', '1', '3', '6', '5', '7', '0']
key['c'] = ['5', '2', '1', '3', '6', '4', '7', '0']
key['d'] = ['6', '2', '1', '3', '5', '4', '7', '0']
key['e'] = ['7', '2', '1', '3', '5', '4', '6', '0']
key['f'] = ['0', '2', '1', '3', '5', '4', '7', '6']
key['g'] = ['1', '2', '6', '3', '5', '4', '7', '0']
key['h'] = ['2', '6', '1', '3', '5', '4', '7', '0']
key['i'] = ['3', '2', '1', '6', '5', '4', '7', '0']
key['j'] = ['4', '2', '1', '3', '5', '6', '7', '0']
key['k'] = ['5', '2', '1', '3', '6', '4', '7', '0']
key['l'] = ['6', '2', '1', '3', '5', '4', '7', '0']
key['m'] = ['7', '2', '1', '3', '5', '4', '6', '0']
key['n'] = ['0', '2', '1', '3', '5', '4', '7', '6']
key['o'] = ['1', '2', '6', '3', '5', '4', '7', '0']
key['p'] = ['2', '6', '1', '3', '5', '4', '7', '0']
key['q'] = ['3', '2', '1', '6', '5', '4', '7', '0']
key['r'] = ['4', '2', '1', '3', '5', '6', '7', '0']
key['s'] = ['5', '2', '1', '3', '6', '4', '7', '0']
key['t'] = ['6', '2', '1', '3', '5', '4', '7', '0']
key['u'] = ['7', '2', '1', '3', '5', '4', '6', '0']
key['v'] = ['0', '2', '1', '3', '5', '4', '7', '6']
key['w'] = ['1', '2', '6', '3', '5', '4', '7', '0']
key['x'] = ['2', '6', '1', '3', '5', '4', '7', '0']
key['y'] = ['3', '2', '1', '6', '5', '4', '7', '0']
key['z'] = ['4', '2', '1', '3', '5', '6', '7', '0']


code_encoding = "utf8"

safe_pre_fix = 'dvc7://'

redundance_rate = 0.2

complicated_coding = True

# ================================   Dvc7 Encoding   ================================
# @Facade
# digit->caesar->compress->base64 =>digit... last time digit->caesar->dirtify->base64
def encode(input,password='',encoding=code_encoding,size=str(redundance_rate)):

    password = str(password).lower()

    if password == '':
        return navie_dvc_base64_encode(input)

    # get bytes
    input = input.encode(encoding)

    password = list(password)

    length = len(password)

    for i in range(0,length):
        if i < length-1:
            input = get_digit(input)
            input = caesar(input, password[i])
            input = compress(input)
            input = base64.b64encode(input)
        else:
            input = get_digit(input)
            input = caesar(input, password[i])  # 最后一位不压缩可以全凯撒自由映射
            times = int(len(input) * int(size)/100)
            input = mess(input,times)
            input = str(base64.b64encode(input.encode(encoding)), encoding=encoding)

    return navie_dvc_base64_encode(input)

# bytes -> str
def get_digit(bytes):
    return __encode_convert_once(bytes)

def to_dirty_digit(str,times):
    dirty_num = ['8','9']
    input = list(str)
    for i in range(times):
        redundance = random.choice(dirty_num)
        input.insert(int((len(input) - 1) * random.random()), redundance)
    return "".join(input)

def from_dirty_digit(input):
    dirty_num = ['8', '9']
    for item in dirty_num:
        input = input.replace(item, '')
    return input

# str -> str
def caesar(str,key):
    return __encode_caesar_once(str,key)

# str -> bytes
def compress(str,encoding=code_encoding):
    return compress_dvc7_str(str,encoding)

# str -> str
def mess(str,times):
    return __encode_mess_once(str,times)

# @Facade
# limited input length  用于 适合长度内
def encode_str(input, password="", _encoding=code_encoding, _redundance_rate=redundance_rate):
    if complicated_coding:
        input = str(base64.b64encode(input.encode(_encoding)), _encoding)
    try:
        password = str(password) # int 转  string 不用encoding
        if password == "":
            return __encode_convert_once(bytes(input, encoding=_encoding))

        input = safe_pre_fix + input
        password = list(password)
        # for 每一位一个迭代 第二位密码就已经是加密上次迭代的密文了
        for i in range(0, len(password)):
            input = __encode_convert_once(bytes(input, encoding=_encoding))  # To 0-7
            input = __encode_caesar_once(input, password[i])  # To Caesar
            # 不是最后一次 就加冗余
            if i < len(password) - 1:  # To Acsii
                property_redundance_times = int(len(input) * _redundance_rate)
                input = __encode_mess_once(input, property_redundance_times)
            # 最后一次 去掉末尾重复的数字
            else:
                code_zero = key[password[i]][0]
                input = re.sub(r'(' + code_zero + '*?)$', '', input)
        return input
    except LookupError as e:
        return e

# convert 0-7
def __encode_convert_once(input_bytes):
    input_len = len(input_bytes)
    loop_times = input_len // 3
    mod = input_len % 3
    if mod > 0:
        loop_times += 1
        if mod == 1:
            input_bytes += b'\x00\x00'
        if mod == 2:
            input_bytes += b'\x00'
    result = ""
    for i in range(0, loop_times):
        pkg_result = __encode_convert_package(input_bytes[i * 3:i * 3 + 3])
        result += pkg_result
    return result

# 3 bytes -> 8 bytes
def __encode_convert_package(package):
    if (len(package) != 3):
        raise BufferError("wrong buffer size")
    data = package  # 24 bits
    b1 = (data[0] & 0b11100000) >> 5
    b2 = (data[0] & 0b00011100) >> 2
    b3 = ((data[0] & 0b00000011) << 1) + ((data[1] & 0b10000000) >> 7)
    b4 = (data[1] & 0b01110000) >> 4
    b5 = (data[1] & 0b00001110) >> 1
    b6 = ((data[1] & 0b00000001) << 2) + ((data[2] & 0b11000000) >> 6)
    b7 = (data[2] & 0b00111000) >> 3
    b8 = (data[2] & 0b00000111)
    result_str = ""
    # int -> str 不用 Encoding
    result_str = result_str.join((str(b1), str(b2), str(b3), str(b4), str(b5), str(b6), str(b7), str(b8)))
    return result_str

# Original 0-7 => Caesar 0->7
def __encode_caesar_once(input_str, password_key):
    input = list(input_str)
    if not password_key in key:
        raise BufferError("Caesar Key Error")
    for i in range(0, len(input)):
        input[i] = key[password_key][int(input[i])]
    return "".join(input)

# Cardar 0-7 => Ascii
def __encode_mess_once(input_str, times):
    input = list(input_str)
    for i in range(times):
        redundance = random.choice(noise)
        input.insert(int((len(input) - 1) * random.random()), redundance)
    return "".join(input)

# ================================   Dvc7 Decoding   ================================
# @Facade
def decode(input,password='',encoding=code_encoding):

    try:
        password = str(password).lower()
        if password == '':
            return navie_dvc_base64_decode(input)

        password = list(password)

        length = len(password)

        for i in range(0,length):
            index = length - i - 1
            if i == 0: # first
                input = str(base64.b64decode(input.encode(code_encoding)),encoding) # s->s
                input = reverse_mess(input)                # s->s
                input = reverse_caesar(input,password[index])              # s->s
                input = reverse_get_digit(input,encoding)                   #  # s-> b->s
            else:
                input = base64.b64decode(input.encode(encoding))           # s->b (b->b)
                input = reverse_compress(input)
                input = reverse_caesar(input,pwd_key=password[index])
                input = reverse_get_digit(input)

        return navie_dvc_base64_decode(input)
    except Exception as eee:
        raise Exception('不是正确的密文或密码，无法解密')
        #raise Exception(eee)

#str
def reverse_get_digit(str,encoding=code_encoding):
    return __decode_convert_once(str,encoding)

# str
def reverse_mess(str):
    return __decode_clean_once(str)

# str
def reverse_caesar(str,pwd_key):
    return __decode_caesar_once(str,pwd_key)

# str
def reverse_compress(bytes):
    return decompress_dvc7_bytes(bytes)

# @Facade
def decode_str(input, password="", _encoding=code_encoding):
    try:
        password = str(password)
        if password == "":
            input = __decode_convert_once(input, _encoding)
            if complicated_coding:
                input = str(base64.b64decode(input.encode(_encoding)), _encoding)
            return input
        password = list(password)
        for i in range(0, len(password)):
            index = len(password) - i - 1
            if i != 0:
                input = __decode_clean_once(input)  # To Pure Caesar
            input = __decode_caesar_once(input, password[index])  # To 0-7
            input = __decode_convert_once(input, _encoding)  # To Str
        if input[:7] == safe_pre_fix:
            input = input[7:]
        else:
            raise PermissionError('Wrong Password')
        if complicated_coding:
            input = str(base64.b64decode(input.encode(_encoding)), _encoding)
        return input
    except:
        return 'wrong password'

# Valid Content & Redundance -> Caesar Acsii
def __decode_clean_once(input):
    for item in noise:
        input = input.replace(item, '')
    return input

# Caesar Acsii -> 0-7
def __decode_caesar_once(input, password_key=''):
    input = list(input)
    if not password_key == "":
        if not password_key in key:
            raise BufferError("Redundance Key Error")
        for i in range(0, len(input)):
            input[i] = str(key[password_key].index(input[i]))
    return "".join(input)

# 0-7 -> Real Content
def __decode_convert_once(input_str, _encoding):
    loop_times = len(input_str) // 8
    mod = len(input_str) % 8
    if mod > 0:
        loop_times += 1
        for i in range(0, 8 - mod):
            input_str += '\0'
    result = ""
    for i in range(0, loop_times):
        pkg_result = __decode_convert_package(input_str[i * 8:i * 8 + 8], _encoding)
        result += pkg_result
    return result.replace('\0', '')

# 8 bytes -> 3 bytes
def __decode_convert_package(package, _encoding):
    data = list(package)  # 24 bits
    for i in range(0, len(data)):
        data[i] = bytes(data[i], _encoding)[0]
    if (len(data) != 8):
        raise BufferError("wrong buffer size")
    b1 = ((data[0] & 0b00000111) << 5) + ((data[1] & 0b00000111) << 2) + ((data[2] & 0b00000110) >> 1)
    b2 = ((data[2] & 0b00000001) << 7) + ((data[3] & 0b00000111) << 4) + ((data[4] & 0b00000111) << 1) + (
                (data[5] & 0b00000100) >> 2)
    b3 = ((data[5] & 0b00000011) << 6) + ((data[6] & 0b00000111) << 3) + ((data[7] & 0b00000111))
    result_b = b'\x00\x00\x00'
    result_b = list(result_b)
    result_b[0] = bytes([b1])
    result_b[1] = bytes([b2])
    result_b[2] = bytes([b3])
    result_b = b''.join(result_b)
    result_str = result_b.decode(_encoding)
    return result_str

# ========================================== Compress 压缩dvc7密文 ========================================

# return bytes 压缩dvc7密文字符串为小型Bytes
def compress_dvc7_str(input_str,_encoding=code_encoding):
    loop_times = len(input_str) // 8
    mod = len(input_str) % 8
    if mod > 0:
        loop_times += 1
        for i in range(0, 8 - mod):
            input_str += '\0'
    result = []
    for i in range(0, loop_times):
        # return bytes
        pkg_result = __compress_convert_package(input_str[i * 8:i * 8 + 8], _encoding)
        result.append(pkg_result)
    return b''.join(result)

# 8 bytes -> 3 bytes
def __compress_convert_package(package, _encoding):
    data = list(package)  # 24 bits
    for i in range(0, len(data)):
        data[i] = bytes(data[i], _encoding)[0]
    if (len(data) != 8):
        raise BufferError("wrong buffer size")
    b1 = ((data[0] & 0b00000111) << 5) + ((data[1] & 0b00000111) << 2) + ((data[2] & 0b00000110) >> 1)
    b2 = ((data[2] & 0b00000001) << 7) + ((data[3] & 0b00000111) << 4) + ((data[4] & 0b00000111) << 1) + (
            (data[5] & 0b00000100) >> 2)
    b3 = ((data[5] & 0b00000011) << 6) + ((data[6] & 0b00000111) << 3) + ((data[7] & 0b00000111))
    result_b = b'\x00\x00\x00'
    result_b = list(result_b)
    result_b[0] = bytes([b1])
    result_b[1] = bytes([b2])
    result_b[2] = bytes([b3])
    result_b = b''.join(result_b)
    return result_b

# ========================================== Decompress 解压dvc7密文 ========================================

# return strings 把压缩过的密文还原为字符串密文
def decompress_dvc7_bytes(input_bytes):
    input_len = len(input_bytes)
    loop_times = input_len // 3
    mod = input_len % 3
    if mod > 0:
        loop_times += 1
        if mod == 1:
            input_bytes += b'\x00\x00'
        if mod == 2:
            input_bytes += b'\x00'
    result = ""
    for i in range(0, loop_times):
        pkg_result = __decompress_convert_package(input_bytes[i * 3:i * 3 + 3])
        result += pkg_result
    return re.sub(r'(0*?)$','',result) # 去处0x00 字符

# 3 bytes -> 8 bytes
def __decompress_convert_package(data):
    if (len(data) != 3):
        raise BufferError("wrong buffer size")
    b1 = (data[0] & 0b11100000) >> 5
    b2 = (data[0] & 0b00011100) >> 2
    b3 = ((data[0] & 0b00000011) << 1) + ((data[1] & 0b10000000) >> 7)
    b4 = (data[1] & 0b01110000) >> 4
    b5 = (data[1] & 0b00001110) >> 1
    b6 = ((data[1] & 0b00000001) << 2) + ((data[2] & 0b11000000) >> 6)
    b7 = (data[2] & 0b00111000) >> 3
    b8 = (data[2] & 0b00000111)
    result_str = ""
    # int -> str 不用 Encoding
    result_str = result_str.join((str(b1), str(b2), str(b3), str(b4), str(b5), str(b6), str(b7), str(b8)))
    return result_str

# ========================================== Bytes Tools bytes转成字符串再操作 ====================================

# 从文件读的bytes内容转为可加密的高兼容的Base64字符串
def bytes_to_base64_str(input_bytes,_encoding=code_encoding):
    return str((base64.b64encode(input_bytes)),encoding=_encoding)

# 从解密过的Base64串 还原回原始bytes
def base64_str_to_bytes(input_str,_encoding=code_encoding):
    input_str = str(input_str)
    return(base64.b64decode(input_str.encode(_encoding)))

# ========================================== To Safe Base64 （密码凯撒里不能大于7 因为过了7内压缩111）=======================
# @Facade
def base64_plus_encode_str(input_str,password='',encoding=code_encoding,redundance=redundance_rate):
    progess = encode_str(input_str,password,encoding,redundance)
    progess = compress_dvc7_str(progess,encoding)
    return navie_dvc_base64_encode(bytes_to_base64_str(progess,encoding))
# @Facade
def base64_plus_decode_str(input_str,password='',encoding=code_encoding):
    input_str = navie_dvc_base64_decode(input_str)
    progess = base64_str_to_bytes(input_str)
    progess = decompress_dvc7_bytes(progess)
    return decode_str(progess,password,encoding)

#===============================  压缩字母 aaaab 变成 a4b （数字不能用 使用时注意小心数字作为冗余被去掉）=================================

# @Facade
def zip_alpha(input):
    temp = input[0]
    count = 0
    result = ''
    for x in input:
        if x == temp:
            count += 1
        else:
            count_str = '' if str(count) == '1' else str(count)
            result += str(temp) + str(count_str)  # 将上一步相同的字符进行统计
            temp = x  # 改变temp
            count = 1
    result += str(temp) + str(count)
    if len(result) > len(input):
        return input
    else:
        return result

# @Facade
def unzip_alpha(input):
    temp = input[0]
    result = ''
    for x in input:
        if x.isdigit():
            for i in range(0,int(x) - 1):
                result += temp
        else:
            temp = x
            result += temp
    return result


safe_dirty_defalt_password_key = 'f'

# @Facade
def navie_dvc_base64_encode(input):
    global safe_dirty_defalt_password_key
    bytes = input.encode('utf-8')
    res = get_digit(bytes)
    res = caesar(res,safe_dirty_defalt_password_key)
    res = compress(res,code_encoding)
    res = str(base64.b64encode(res),code_encoding)
    return res

# @Facade
def navie_dvc_base64_decode(input):
    global safe_dirty_defalt_password_key
    res = base64.b64decode(input.encode(code_encoding))
    res = decompress_dvc7_bytes(res)
    res = from_dirty_digit(res)
    res = reverse_caesar(res,safe_dirty_defalt_password_key)
    res = reverse_get_digit(res)
    return res

# ======================== test =======================

# b64 = base64_plus_encode_str("dvc7:的//Wkhaak56b3ZMdz09",12)
# print(b64)
# print(base64_plus_decode_str( b64,12) + '\n' )
#

# bbb = encode('小鼻子呢', 34,code_encoding,20)
# print(bbb)
# ddd = decode(bbb,34)
# print(ddd)
#
# m = '3107511615046127320405113644456422466531142615512543112433441171234525473604746132025515324545612546551534453153316745431465110523230502216550603563011632252462306421443646215121453132364524602423114426445525346735172145312031042106204621551626753221051064312651262404612532632515146471452504351136454552224531153324514125267131140605042123212532452562234745151426050534632522364411612343106114460526340531202125046224641550206605532645152125266125242421531445117221475127210471673047514315245504202745212125113125042065202465562145352526055110312414712044706214252515144511012325212132647461264741163265110324475122340511723562551514247114302440651464655133055144216301642343007114451463336311431446212023230560126471531407052532670124230315473505415221442115144615723124410632655060254745153323446226466516224541532346054221455162234521703405015325265124246551262643014714253554244545453263052731466516262611071425512614265570232751321404715126267515214544602365357035044524360431241425255324653505140615062545353136451162264534713424646033070520324444633067511633447461262255443244715023442111140625261507311536254553234541013605246122230116252305232546606535246552224701422105115725066543320465242323352321452461232305013646110523453115326431312263052225047124224745323265112030652105362505051422552433272064310311251425215121452142324471562246711215061460160751111403215723265163320515722223051225232170242651153544550432631523332465612345255314252552360531452503246024244153362621051424611714473470232644612324715214074516212465553026506524052061202741411425115424431532250545242544411336267460234441163265050526467523144655523126610220247526310505202104446123230505146521512645211525040572234415642545010436064526246301702446453225053126336325232204516623075125324451541507114114466104230515642425515123265143334405532523015736247103162705453245510723452111140511722544212621032564246751013505315422454514250424623046550135451171244655413264306525431160320521262627411221046554232751211465212424425515250471252627510514451527140315162147017123266471244531713363052620672124232521251444710534667515146640612326614422446552242741251465106325465116356461722544412526062106224525573645052421473117250621153026554314452523336305252545510731030160236550613406752021043131314650643644706234071514140431152623115335446504214721452545246025265143144465512327054425234554232315111444557226440545212321662566511634453552224701261427010423430154342525272527411533232465236315263326210425453541142425522445246131261555262741432467017023241532344501033163413214453061262300603404557133630521364305573107512235452130244315262063453223252064332475262047151425467557314655253325152424274545256511252327513223045526340701221404455323452557364605243063212021442567250311503564717221425525210431712345214715261504202705453264514125253553360631542345014314473564242651111426050523464145324411032427510516046124310411463224657023653132362545263063151721450463234311051464716717236400'
# rrr = decode(reverse_get_digit(m),'love')
# print(rrr)

#
# dirty = 'MjE3NTUzMjEyMzI3MTY3MjM2NjQzMTEx'
# print(decode(dirty,'l0'))
#
# tt = base64_plus_encode_str('hel日lo',12)
# print(tt)
# rr = base64_plus_decode_str(tt,12)
# print(rr)

# tt = '测试一哈123'
# tten = navie_dvc_base64_encode(tt)
# print(tten)
# ttde = navie_dvc_base64_decode(tten)
# print(ttde)
