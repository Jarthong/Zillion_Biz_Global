'''
该脚本封装不同类型接口请求的（签名）方式
'''

import hashlib
import json
import time
import requests
import config_params

# 不需要签名的接口 get请求
def public_request_get(api_url, **payload):
    return public_request('GET',api_url,**payload)

# 不需要签名的接口 post请求
def public_request_post(api_url, **payload):
    return public_request('POST',api_url,**payload)

# 不需要签名的接口
def public_request(method, api_url, **payload):
    """request public url"""
    r_url = api_url
    try:
        r = requests.request(method, r_url, params=payload)
        r.raise_for_status()
        if r.status_code == 200:
            return True, r.json()
        else:
            return False, {'error': 'E10000', 'data': r.status_code}
    except requests.exceptions.HTTPError as err:
        return False, {'error': 'E10001', 'data': r.text}
    except Exception as err:
        return False, {'error': 'E10002', 'data': err}

# 需要签名的接口 get请求
def signed_request_get(api_url, **payload):
    return signed_request('GET',api_url,**payload)

# 需要签名的接口 post请求
def signed_request_post(api_url, **payload):
    return signed_request('POST',api_url,**payload)

# 需要签名的接口
def signed_request(method, api_url, **payload):
    """request a signed url"""
    timestamp = str(int(time.time() * 1000))
    full_url = api_url

    param = ''
    if method == 'GET' and payload:
        for k in sorted(payload):
            param += k + payload[k].__str__()
    elif method == 'POST' and payload:
        param = json.dumps(payload)
    elif not payload:
        payload = ''

    sig_str = config_params.API_ID + timestamp + param + config_params.API_SECRET
    signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()

    # 判断是否有API访问口令
    if config_params.pass_phrase == '':  # 无访问口令
        headers = {
            'Apiid': config_params.API_ID,
            'Timestamp': timestamp,
            'Sign': signature
        }

    else:  # 有访问口令
        phrase_time = timestamp + config_params.pass_phrase
        phrase = hashlib.md5(phrase_time.encode('utf-8')).hexdigest()  # 加上时间戳的API访问口令进行md5加密
        headers = {
            'Apiid': config_params.API_ID,
            'Timestamp': timestamp,
            "Passphrase": phrase,
            'Sign': signature
        }

    try:
        r = requests.request(method, full_url, headers=headers,
                             json=payload) if method == 'POST' else requests.request(
            method, full_url, headers=headers, data=payload)
        '''
        # 上面这行代码和下面这四行代码等同：（判断请求是否为POST）
        if method == 'POST':
            r = requests.request(method, full_url, headers=headers, json=payload)
        else:
            r = requests.request(method, full_url, headers=headers, data=payload)
        '''

        r.raise_for_status()
        if r.status_code == 200:
            return True, r.json()
        else:
            return False, {'error': 'E10000', 'data': r.status_code}
    except requests.exceptions.HTTPError as err:
        return False, {'error': 'E10001', 'data': r.text}
    except Exception as err:
        return False, {'error': 'E10002', 'data': err}

