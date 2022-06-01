# !/usr/bin/python
# -*- coding:utf-8 -*-
import requests, hmac, base64, struct, hashlib, time, datetime, json
import threading

# 测试环境
base_url = 'http://179.zbg.com'
server_id = 'eXXXXXXX'
http_key = '3a65XXXXXXXXXXXXXX'
order_id = "O6552142922563719168"  # 订单编号

# 接单-撤单
# user_id = ['7gtW9L90fsO', '7h8DRo8mjsu']
# params = [{"orderId": order_id, "status": 1}, {"orderId": order_id}]
# url = ['/exchange/otc/controller/otcordercontroller/acceptorder',
#        '/exchange/otc/controller/otcordercontroller/cancelorder']

# 撤单-接单
user_id = ['7ezdaxgBgC8', '7gtW9L90fsO']   # 1100@qq.com(7h8DRo8mjsu)  4400@qq.com  7ezdaxgBgC8
params = [{"orderId": order_id}, {"orderId": order_id, "status": 1}]
url = ['/exchange/otc/controller/otcordercontroller/cancelorder',
       '/exchange/otc/controller/otcordercontroller/acceptorder']

def otc(Params, User_id, url):
    timestamp = str(int(time.time() * 1000))
    param = json.dumps(Params)
    sig_str = server_id + timestamp + param + http_key
    signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
    headers = {'Clienttype': '0', 'Serverid': server_id, 'Userid': User_id, 'Timestamp': timestamp, 'Sign': signature, 'Lan': 'cn'}
    r = requests.post(url=base_url + url, headers=headers, json=Params, verify=False)
    print('访问结果', datetime.datetime.now(), r.json())

if __name__ == '__main__':
    for i in range(0, 2):
        t = threading.Thread(target=otc, args=(params[i], user_id[i], url[i]))
        t.start()
