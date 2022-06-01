import requests
import time, datetime
# 注意：没有Crypto库可以安装，但是安装pycryptodome库的时候，会同步下载Crypto这个库，另外crypto（小写字母）这个库与Crypto是不同的
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64
import hashlib
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_pubkey_IP():
    get_pubkey_url = '/exchange/user/controller/website/baseapicontroller/getpubkey'
    r_get_pubkey = requests.get(base_url + get_pubkey_url, verify=False)
    pubkey = r_get_pubkey.json()['datas']['pubKey']
    pubkey_str = '-----BEGIN RSA PRIVATE KEY-----\n' + pubkey + '\n-----END RSA PRIVATE KEY-----'
    IP = r_get_pubkey.json()['datas']['keyId']
    return pubkey_str, IP

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
    user_id = str(r_login.json()['datas']['userId'])
    token = str(r_login.json()['datas']['token'])
    print('登录请求状态信息：', r_login.json()['resMsg'])
    return user_id, token

def rob_buy(base_url, username, password, inputType, googleCode, amount):
    user_id, token = login_token(username, password)
    param_buy = {'inputType': inputType, 'googleCode': googleCode, 'amount': amount}
    param_sorted = sorted(param_buy)
    param_str = ''
    for k in param_sorted:
        param_str += k + param_buy[k]
    # print('排序后的值：', param_str)
    timestamp = str(int(time.time() * 1000))
    # 拼接sign字符串并进行md5加密
    sign_str = user_id + timestamp + param_str + token
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()

    headers_rob = {'Clienttype': '1', 'Timestamp': timestamp, 'Userid': user_id, 'Sign': sign}
    buy_url = '/exchange/activity/controller/zbgactivitycontroller/inputFund'
    r_buy = requests.post(url=base_url+buy_url, headers=headers_rob, data=param_buy, verify=False)
    # return r_buy
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print('当前时间：', time_now)
    print('购买请求状态码：', r_buy.status_code)
    print(r_buy.json())

if __name__ == '__main__':
    base_url = 'https://www.zbgpro.com'
    # base_url = 'http://179.zbg.com'
    username = 'xxxxxxx@qq.com'
    password = 'xxxxxxx'
    # username = '15xxxxxx4'
    # password = 'xxxxxxxxxxx'
    inputType = '7lFpNIUku1W'
    googleCode = '55'
    amount = '400'
    '''
    while True:
        # print(time_now)
        rob_buy(base_url, username, password, inputType, googleCode, amount)
        # if r_buy.json()['resMsg']['code'] == '1':
        #     break
    '''
    print(login_token(username, password))

