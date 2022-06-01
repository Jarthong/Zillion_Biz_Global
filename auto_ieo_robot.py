# !/usr/bin/python
# -*- coding:utf-8 -*-
'''
注意返回的是str，调用时，若需要int，则需要转换
'''
import requests
import sys
import json
import hmac, base64, struct, hashlib, time

def signed_request(method, api_url, **payload):
    """request a signed url"""
    timestamp = str(int(time.time() * 1000))
    full_url = host_url + api_url

    param = ''
    if method == 'GET' and payload:
        for k in sorted(payload):
            param += k + payload[k]
    elif method == 'POST' and payload:
        param = json.dumps(payload)
    elif not payload:
        payload = ''

    sig_str = server_id + timestamp + param + http_key
    signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()

    headers = {
        'Clienttype': '0',
        'Serverid': server_id,
        'Userid': user_id,
        'Timestamp': timestamp,
        'Sign': signature
    }

    try:
        r = requests.request(method, full_url, headers=headers, json=payload) if method == 'POST' else requests.request(
            method, full_url, headers=headers, data=payload)
        r.raise_for_status()
        if r.status_code == 200:
            return True, r.json()
        else:
            return False, {'error': 'E10000', 'data': r.status_code}
    except requests.exceptions.HTTPError as err:
        return False, {'error': 'E10001', 'data': r.text}
    except Exception as err:
        return False, {'error': 'E10002', 'data': err}


def get_google_code(secret):
    """
    :return: googlecode
    """
    intervals_no = int(time.time()) // 30
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    # 很多网上的代码不可用，就在于这儿，没有chr字符串
    o = ord(chr(h[19])) & 15
    h = (struct.unpack(">I", h[o:o + 4])[0] & 0x7fffffff) % 1000000

    # 这儿需要注意，程序返回的是去0的字符串，比如验证码是005123，程序计算的结果是5123，所以，需要在前面补0，补到六位数
    return '%06d' % h

def ieo_config():
    return signed_request('GET', '/exchange/activity/controller/ZbgActivityController/getConfig')

def ieo(secret, ieo_id, amount):
    google_code = get_google_code(secret)
    return signed_request('GET', '/exchange/activity/controller/ZbgActivityController/inputFund', inputType=ieo_id,
                          googleCode=google_code, amount=amount)

if __name__ == '__main__':
    # 正式环境
    # server_id = 'xxx_xxx_xxx'
    # http_key = '71sxxxxx-4dd-ec-1bb23c3f'
    # host_url = 'http://boss.zbg.com'  # 域名
    # # host_url = 'https://www.zbg.com'
    # # host_url = 'https://ae.zbg.com'
    # user_id = '7ezY8tA61Au'      # 用户ID (574)7fZJygtlQrM (730)7etA62Yz7Au
    # secret = 'L2KBVWR9EXUHGNNE'  # google验证码密钥  (574)F6AUBFhZ6CW75Q27  (730)L2NBWHHUR5VHGNEE
    # ieo_id = '7mFtY8xGV6o'
    # amount = '100'

    # 测试环境  990（ID:7ezdaxgBgC8，Google:IHKWBKQZUHBHOBWI）,330（7gwUzgkdsdE）
    host_url = 'http://179.zbg.com'
    user_id = '7ezdaxgBgC8'
    server_id = 'exxxx-xxx'
    http_key = '3a659xxxxxxxxxxxxxc73e'
    secret = 'IHKHBHOWBKQZUBWI'
    ieo_id = '7mGqhmmdlWO'
    amount = '1000'

    while True:
        amount_total = ieo(secret, ieo_id, amount)
        print(amount_total)
        if amount_total[1]['resMsg']['code'] in ('9003', '9010'):
            break
