#coding=gb2312
import time,hashlib,requests
from urllib.parse import urlencode

username ='zxhmaster'
password ='api_west_password'

api_url = 'https://api.west.cn/api/v2/'
params_name = ['username','time','token']

def _md5(source_str):
    coder = hashlib.md5()
    source_bytes = source_str.encode(encoding='gb2312')
    coder.update(source_bytes)
    return coder.hexdigest()

def _get_params_dic():
    global username
    global password
    global params_name
    timestamp = (int(time.time()*1000))
    return {params_name[0]:username,params_name[1]:timestamp,params_name[2]:_md5(username+password+str(timestamp))}

def _get(url, params_dic):
    response = requests.get(url=url,params=params_dic)
    return response.text

def _post(url, params):
    data = urlencode(params,encoding='gb2312')
    response = requests.post(url=url,data=data,headers={'Content-Type':'application/x-www-form-urlencoded'})
    return response.text


# ��ѯ�ҵ����
def check_blance():
    url = api_url+'info/?act=checkbalance'
    return _get(url, _get_params_dic())

# ��ȡ�ҵ�����
def fetch_my_domains():
    url = api_url + 'domain/?act=getdomains'
    return _get(url, _get_params_dic())

# ��ѯ����״̬ ��ɷ�ע��
def query_domain(domain,suffix):
    url = api_url + 'domain/query/'
    params = _get_params_dic()
    params['domain'] = domain
    params['suffix'] = suffix
    return _post(url, params)

# ��ȡ�����۸�
def query_domain_price(domain):
    url=api_url+'info/?act=getprice'
    params = _get_params_dic()
    params['type'] ='domain'
    params['value'] = domain
    params['year']='1'
    return _post(url, params)

# �޸�����dns
def change_domain_dns(domain,dns1,dns2):
    url = api_url +'domain/?act=moddns'
    params = _get_params_dic()
    params['domain'] = domain
    params['dns1'] = dns1
    params['dns2'] = dns2
    return _post(url, params)

# �����������
def add_domain_dns_record(domain,prefix,type,value,ttl=900,level=10):
    url = api_url + 'domain/?act=adddnsrecord'
    params = _get_params_dic()
    params['domain'] = domain
    params['host'] = prefix
    params['type'] = type
    params['value'] = value
    params['ttl'] = ttl
    params['level'] = level
    return _post(url, params)

# ��ȡ����������¼ ���صĽ�����¼id����
def fetch_domain_dns_records(domain):
    url = api_url + 'domain/?act=getdnsrecord'
    params = _get_params_dic()
    params['domain'] = domain
    return _post(url, params)

# �޸�����������¼
def modify_domain_dns_record(domain,id,value,ttl=900):
    url = api_url + 'domain/?act=moddnsrecord'
    params = _get_params_dic()
    params['domain'] = domain
    params['id'] = id
    params['value'] = value
    params['ttl'] = ttl
    return _post(url, params)

# ɾ������������¼
def delete_domain_dns_record(domain,id):
    url = api_url + 'domain/?act=deldnsrecord'
    params = _get_params_dic()
    params['domain'] = domain
    params['id'] = id
    return _post(url,params)

# �������ģ��
def create_domain_info_template(
        c_name_xing,
        c_name_ming,
        c_province,
        c_city,
        c_address,
        e_first_name,
        e_last_name,
        e_province,
        e_city,
        e_address,
        email,
        postcode,

        phone_type,
        mobile_number='',
        phone_code='',
        phone_number='',

        owner='I',
        c_company_name='',
        e_company_name='',
        country='CN',
        country_phone_prefix='+86'):

    url = api_url + 'audit/?act=auditsub'
    params = _get_params_dic()

    if owner =='E':
        if c_company_name == '' or e_company_name == '':
            raise Exception('û�����빫˾���ƻ�û������Ӣ�Ĺ�˾����')

        params['c_org_m'] = c_company_name
        params['c_org'] = e_company_name
    elif owner != 'I':
        raise Exception('���������������')

    if phone_type == '0':
        params['c_ph'] = mobile_number
    elif phone_type == '1':
        params['c_ph_code'] = phone_code
        params['c_ph_num'] = phone_number
    else:
        raise Exception('����ĵ绰����')

    params['c_ph_type'] = phone_type
    params['c_regtype'] = owner
    params['c_co'] = country
    params['c_em'] = email
    params['c_pc'] = postcode
    params['cocode'] = country_phone_prefix
    params['c_ln_m'] = c_name_xing
    params['c_fn_m'] = c_name_ming
    params['c_st_m'] = c_province
    params['c_ct_m'] = c_city
    params['c_adr_m'] = c_address
    params['c_ln'] = e_last_name
    params['c_fn'] = e_first_name
    params['c_st'] = e_province
    params['c_ct'] = e_city
    params['c_adr'] = e_address
    return _post(url,params)

# ��ȡ�����ϴ�ͼƬ��token verify_type
def real_name_get_domain_info_template_token(info_template_id, verify_code,verify_type='1'):
    url = api_url + 'audit/?act=uploadwcftoken'
    params = _get_params_dic()
    params['c_sysid'] = info_template_id
    params['f_type_org'] = verify_type
    params['f_code_org'] = verify_code
    return _post(url,params)

# �������ȡ����token�ϴ�ʵ��ͼƬ��base64
def real_name_upload_img_by_token(token,img_base64):
    url = 'https://netservice.vhostgo.com/wcfservice/Service1.svc/Wcf_AuditUploadFile'
    params = {}
    params['token'] = token
    params['file_org'] = img_base64
    response = requests.post(url=url, data=params, headers={'Content-Type': 'application/json'})
    return response.text

# ע������
def register_domain(domain,year,info_template_id,safe_price=''):
    url = api_url + 'audit/?act=regdomain'
    params = _get_params_dic()
    if safe_price != '':
        params['client_price'] = safe_price
    params['c_sysid'] = info_template_id
    params['regyear'] = year
    params['domain'] = domain
    return _post(url,params)


# print(check_blance())
# print(query_domain('ttwerqff','.online'))
# print(fetch_my_domains())
#print(fetch_domain_dns_records('base64.plus'))
#print(add_domain_dns_record('base64.plus','www','CNAME','cloud.src.pub'))
#print(modify_domain_dns_record('base64.plus','49875273','src.pub'))
#print(delete_domain_dns_record('base64.plus','49875273'))
#print(create_domain_info_template('��','����','����','����','��������ׯ','wang','wang','beijing','beijing','haidianshangzhuang','wang@qq.com','100000','0','13932699587'))
# print(register_domain('asdfwg.test',1,274465))
# print(real_name_get_domain_info_template_token(274465,654301199202120317))
#print(real_name_upload_img_by_token('ig3rEUaK5ZNjwKaYhuVECNrcBoyHeSqkk/OwXwgzopkcaqS4DcUjrXupy0EzcugodCmKpq5YHoG4BujmNXAnF9z6Ffa0cUg1JE7i9dLho/3uTc19q+Ll767YKt2RepQ+nPtdH6jXpUkf6k3bXJL+7XpVzXzcfJNQ3HPKVdJNyiEFzVcnR1BXktUWPqgIe20wrFfnrCDG/luQA/Nkule7HXTMygpQ5A1eZBVHeddQvJe3O4J86K+Y60B5j02BL/LJHlGWOPSHFF9loirUdDLVZvdXyxWDTRy0FxkLZeMou4SI3p8r8rwC5k/UGioG8MUC+rAzme5gErOhRPdFIq3WB79iTaOXCOAQSX4q2NZFhgdvVSAa2rAeG14+LS1/s4vswYlvUhMJR9/Zv45oT5EqRw==','zxcv'))
#print(change_domain_dns('base64.plus','114.114.114.114','114.114.115.115'))
#print(get_test())