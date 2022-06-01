import requests
import time, datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64
import hashlib
import json

def get_pubkey_IP():
    get_pubkey_url = '/exchange/user/controller/website/baseapicontroller/getpubkey'
    r_get_pubkey = requests.get(base_url + get_pubkey_url, verify=False)
    pubkey = r_get_pubkey.json()['datas']['pubKey']
    pubkey_str = '-----BEGIN RSA PRIVATE KEY-----\n' + pubkey + '\n-----END RSA PRIVATE KEY-----'
    ip = r_get_pubkey.json()['datas']['keyId']
    return pubkey_str, ip

# 生成password字符串
def password_srt(password):
    rsa_key = RSA.importKey(get_pubkey_IP()[0])
    cipher = Cipher_pkcs1_v1_5.new(rsa_key)
    cipher_text = base64.b64encode(cipher.encrypt(password.encode(encoding="utf-8")))
    cipher_str = cipher_text.decode('utf-8')
    return cipher_str

# 登录,获取token、userid
def login_token(username, password):
    param = {'userType': '2', 'userName': username, 'password': password_srt(password), 'rsaKeyId': get_pubkey_IP()[1],
             'countryCode': '+86'}
    login_url = '/exchange/user/controller/website/usercontroller/loginbypassword'
    r_login = requests.request(method='POST', url=base_url+login_url, json=param, verify=False)
    user_id_2 = str(r_login.json()['datas']['userId'])
    token = str(r_login.json()['datas']['token'])
    # print('登录请求状态信息：', r_login.json()['resMsg'])
    return user_id_2, token

# 验证码登录，未注册的账号会自动注册
def add_user(phone):
    # base_url_1 = 'http://179.zbg.com'
    server_id = 'exchange-001'
    http_key = '3a659879-8832-41a7-b542-79b73c53c73e'
    # 验证码登录接口，未注册的账号会自动注册
    api_add_login = '/exchange/user/controller/website/usercontroller/loginByCode'
    params = {"userName": phone, "smsCode": "123456", "userNameType": 1, "countryCode": "+86"}
    param = json.dumps(params)
    timestamp_1 = str(int(time.time() * 1000))
    sig_str = server_id + timestamp_1 + param + http_key
    signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
    header = {'Clienttype': '0', 'Serverid': server_id, 'Timestamp': timestamp_1, 'Sign': signature, "Lan": 'cn'}
    r_add_user = requests.request(method='POST', url=base_url + api_add_login, headers=header, json=params, verify=False)
    result_add_user = r_add_user.json()['resMsg']
    print('验证码登录或注册结果：', result_add_user)
    user_id_1 = r_add_user.json()['datas']['userId']
    return user_id_1

# 给传入的user_id账号充币
def add_money(user,currency_name,amount,google):
    # 登录boss管理员账号，并获得userID和token值。
    user_id, token = login_token(boss_username, boss_password)

    # 给指定的user账号充币
    param_add_money = {'userId': user, 'currencyTypeName':currency_name, 'amount': amount, 'googleCode': google, 'freezeStatus': '0', 'remark': 'jarthong', 'smsCode':'123456'}
    param_sorted = sorted(param_add_money)
    param_str = ''
    for k in param_sorted:
        param_str += k + param_add_money[k]
    # print('排序后的值：', param_str)
    timestamp = str(int(time.time() * 1000))
    # 拼接sign字符串并进行md5加密
    sign_str = user_id + timestamp + param_str + token
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    headers = {'Clienttype': '1', 'Timestamp': timestamp, 'Userid': user_id, 'Sign': sign}
    add_money_url = '/exchange/fund/controller/admin/fundAdminController/addAmount'
    r_add_money = requests.post(url=base_url+add_money_url, headers=headers, data=param_add_money, verify=False)
    # return r_buy
    # print('充币接口请求状态码：', r_add_money.status_code)
    print('给账号充币请求的结果：', r_add_money.json()['resMsg'])

if __name__ == '__main__':
    phone = 13100000446           # 初始手机号
    num = 1                             # 要生成的账号个数
    # currency_name = ['btc', 'usdt', 'zb', 'qc', 'eth', 'bitw', 'krw']          # 充值的币种,可以数组的形式填入，填多个可以一次性充值多个
    currency_name = ['zt']
    amount = 5                     # 充值的数量

    google = '123456'                     # Google验证码，有需要可以调用生成方法
    boss_username = 'jarthong@qq.com'     # boss的管理员账号
    boss_password = 'h1234567'            # boss的管理员密码
    base_url = 'http://179.boss.zbg.com'  # 域名

    m = 0
    while m < num:
        user_name = str(phone + m)
        amount_str = str(amount)
        m += 1
        print('第{}个注册并充值的账号是：{}；充值的币种是：{}；充值数量是：{}'.format(m, user_name, currency_name, amount_str))
        # 验证码登录，未注册的账号会自动注册，并把返回的userID号赋给user_id变量
        user_id_login = add_user(user_name)
        # 给传入的user_id账号充值，遍历币种名的列表，多个币种名的话，进行多个充值
        for i in currency_name:
            add_money(user_id_login, i, amount_str, google)
        print('-'*100)
