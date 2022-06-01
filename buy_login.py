import time, datetime, random
import requests, hashlib, json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64, struct, hmac

# 测试环境
# base_url = 'http://179.zbg.com'
# username = '3300@qq.com'
# pwd = 'h1234567'

# 正式环境
base_url = 'https://www.zbg.com'
username = '574zzz4@qq.com'  # 990908 652628
pwd = 'xxxxxxx'
market_id = '464'   # 交易市场id号   462(untz_zt)  364(qc_zt) 464(bhtx_zt)  336(zt_usdt)
entrust_type = 1  # 要下单的类型，0 卖出 1 购买
amount = 20    # 购买数量
price = 2.375     # 下单价格

# user_id = '7e7Atz61gAu'
# google_secret = 'X4IAXKGQHG4CREJ4'

# base_url = 'http://boss.zbg.com'   # 域名
# server_id = 'exch-xxxxxxxxxx'
# http_key = '71a80xxxxxxxxxxxx-xxxxxx3f'


'''
def get_google_code(secret):
    """注意返回的是str，调用时，若需要int，则需要转换"""
    intervals_no = int(time.time()) // 30
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = ord(chr(h[19])) & 15
    h = (struct.unpack(">I", h[o:o + 4])[0] & 0x7fffffff) % 1000000
    return '%06d' % h
'''

get_pubkey_url = '/exchange/user/controller/website/baseapicontroller/getpubkey'
r_get_pubkey = requests.get(base_url+get_pubkey_url, verify=False)
pubkey = r_get_pubkey.json()['datas']['pubKey']
pubkey_str = '-----BEGIN RSA PRIVATE KEY-----\n' + pubkey + '\n-----END RSA PRIVATE KEY-----'
IP = r_get_pubkey.json()['datas']['keyId']
# 生成password字符串
rsakey = RSA.importKey(pubkey_str)
cipher = Cipher_pkcs1_v1_5.new(rsakey)
cipher_text = base64.b64encode(cipher.encrypt(pwd.encode(encoding="utf-8")))
cipher_str = cipher_text.decode('utf-8')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Accept': '*/*',
    'Clienttype': '1',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Content-Length': '271',
    'Accept-Language': 'zh-CN,zh;q=0.9,vi;q=0.8,ko;q=0.7,be;q=0.6,ja;q=0.5'
           }
param = {'userType': '2', 'userName': username, 'password': cipher_str, 'rsaKeyId': IP, 'countryCode': '+86'}

# 登录
login_url = '/exchange/user/controller/website/usercontroller/loginbypassword'
r_login = requests.request(method='POST', url=base_url+login_url, headers=headers, json=param, verify=False)
# print(r_login.status_code)
print('登录返回信息：', r_login.json()['resMsg'])

# 登录需要谷歌验证码的时候
# if r_login.json()['resMsg']['code'] == '6011':
#     print('谷歌验证码：', get_google_code(google_secret))
#     param = {'userNameType': '2', 'userName': username, 'password': cipher_str, 'rsaKeyId': IP, 'countryCode': '+86',
#              "googleCode": get_google_code(google_secret)}
#     r_login = requests.request(method='POST', url=base_url + login_url, headers=headers, json=param, verify=False)

token = str(r_login.json()['datas']['token'])
userId = str(r_login.json()['datas']['userId'])
# print('token的值是:', token, type(token))
# print('userId的值是:', userId, type(userId))

# 新增委托单接口
buy_url = '/exchange/entrust/controller/website/EntrustController/addEntrust'
param_buy = {"type": entrust_type, "price": price, "marketId": market_id, "userId": userId,
             "rangeType": 0, "amount": amount}
param_str = json.dumps(param_buy)

# while True:
    # time.sleep(0.01)
timestamp = str(int(time.time() * 1000))
# 拼接sign字符串并进行md5加密
sign_str = userId + timestamp + param_str + token
sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
headers_buy = {'Clienttype': '1', 'Timestamp': timestamp, 'Userid': userId, 'Sign': sign}
r_buy = requests.post(url=base_url+buy_url, headers=headers_buy, json=param_buy, verify=False)
print('买单时间：', datetime.datetime.now(), '结果：', r_buy.json()['resMsg'])

