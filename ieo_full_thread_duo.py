# !/usr/bin/python
# -*- coding:utf-8 -*-
import requests, hmac, base64, struct, hashlib, time, datetime
import threading

# 正式环境
base_url = 'http://boss.zbg.com'   # 域名
# base_url = 'https://www.zbg.com'
# base_url = 'https://ae.zbg.com'
user_id = '7eztA7d71Yw'
secret = 'L2KBR5HGNNVWEXUE'        # google 验证码密钥
server_id = 'exch-xxxxxxxxxx'
http_key = '71a80xxxxxxxxxxxx-xxxxxx3f'

# 测试环境  990（ID:7ezdaxgBgC8，Google:IHKWBKQZUHBHOBWI）,330（7gwUzgkdsdE）  15915774459_google(5XBNLYUSQ6YJVXK4)
# base_url = 'http://179.zbg.com'
# user_id = '7luyUt8sO92'
# server_id = 'eXXXXXXX'
# http_key = '3a65XXXXXXXXXXXXXX'
# secret = 'IZUHBHKQBOHKWBWI'

def get_google_code(secret):
    intervals_no = int(time.time()) // 30
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = ord(chr(h[19])) & 15
    h = (struct.unpack(">I", h[o:o + 4])[0] & 0x7fffffff) % 1000000
    return '%06d' % h

# ieo抢购
def rob_buy(inputType, amount):
    param_buy = {'inputType': inputType, 'googleCode': get_google_code(secret), 'amount': amount}
    param_sorted = sorted(param_buy)
    param_str = ''
    for k in param_sorted:
        param_str += k + param_buy[k]
    # print('排序后的值：', param_str)
    timestamp = str(int(time.time() * 1000))
    # 拼接sign字符串并进行md5加密
    sig_str = server_id + timestamp + param_str + http_key
    sign = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
    # headers_rob = {'Clienttype': '1', 'Timestamp': timestamp, 'Userid': user_id, 'Sign': sign}  #  这个请求头不行
    headers_rob = {'Clienttype': '0', 'Serverid': server_id, 'Userid': user_id, 'Timestamp': timestamp, 'Sign': sign}
    buy_url = '/exchange/activity/controller/zbgactivitycontroller/inputFund'
    r_buy = requests.post(url=base_url+buy_url, headers=headers_rob, data=param_buy, verify=False)
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print('当前时间：{}；账号：{}；返回信息：{}\n'.format(time_now, user_id, r_buy.json()['resMsg']))
    # print('购买请求状态码：', r_buy.status_code)
    # print(r_buy.json())
    # return r_buy.json()['resMsg']['code']

if __name__ == '__main__':
    # 7lWJfNVa9oG   7lWFpNUku1I  线上：7lbkjPx8thg  amount = '4179'
    # inputType = '7mFCGV6Y5xo'
    # amount = '100'
    # min_amount = '20'
    inputType_list = ['7mFCGV6Y5xo', '7mFBvE21Rtg']
    amount_list = ['100', '2000']
    # min_amount_list = ['20', '']

    while True:
        for j in range(0, 1):
            # rob = rob_buy(inputType_list[i], amount_list[i])
            rob = threading.Thread(target=rob_buy, args=(inputType_list[j], amount_list[j]))
            rob.start()
            # # print('状态码是：', rob, type(rob))
            # if rob == '9011' or rob == '9003':
            #     break
            # elif rob == '9007':
            #     while True:
            #         # amount = str(int(float(amount)/2))
            #         # print('此次的数量是', amount)
            #         # if amount == 0:
            #         #     break
            #         rob = rob_buy(inputType_list, min_amount_list)
            #         if rob == '9011' or rob == '9003':
            #             break

