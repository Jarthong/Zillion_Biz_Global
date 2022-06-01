import requests, hashlib
import time, datetime, random
import json
# import jarthong_zbg_GetMarketId
import urllib3
import threading

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 测试环境
# base_url = 'http://179.zbg.com'
# server_id = 'eXXXXXXX'
# http_key = '3a65XXXXXXXXXXXXXX'
base_url = 'http://178.zbg.com'
server_id = '85bCTwwAaAaiBc85bCTiBd'  # 990908814@qq.com
http_key = '3cac9ed9e1a07b6dc28dc3bd9ab76f62'

# 队列下单接口
api_url = '/exchange/api/v1/order/queue-order'
# 普通下单接口
API_ADD_ENTRUST = '/exchange/entrust/controller/website/EntrustController/addEntrust'

def buy(types, UserId, market_name, amount, price):
    # 队列下单
    if types == 0:
        params = {"symbol": market_name, "side": "buy", "amount": amount, "price": price}
        param = json.dumps(params)
        timestamp = str(int(time.time() * 1000))
        sig_str = server_id + timestamp + param + http_key
        signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
        header = {'Clienttype': '0', 'Serverid': server_id, 'Userid': UserId, 'Timestamp': timestamp, 'Sign': signature, 'Lan': 'cn'}
        r_sell = requests.request(method='POST', url=base_url + api_url, headers=header, json=params, verify=False)
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # 当前时间
        result_sell = r_sell.json()
        print('用户：{}；下单时间：{}；结果：{}'.format(UserId, time_now, result_sell))
    # 普通下单
    elif types == 1:
        # entrust_type = random.choice([0, 1])  # 要下单的类型，0 卖出 1 购买
        params = {'marketId': market_id, 'amount': amount, 'price': price, 'rangeType': 0, 'type': 0}
        param = json.dumps(params)
        timestamp = str(int(time.time() * 1000))
        sig_str = server_id + timestamp + param + http_key
        signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
        header = {'Clienttype': '0', 'Serverid': server_id, 'Userid': UserId, 'Timestamp': timestamp, 'Sign': signature, 'Lan': 'cn'}
        r_sell = requests.request(method='POST', url=base_url + API_ADD_ENTRUST, headers=header, json=params, verify=False)
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # 当前时间
        result_sell = r_sell.json()
        print('用户：{}；下单时间：{}；结果：{}'.format(UserId, time_now, result_sell))
    else:
        # entrust_type = random.choice([0, 1])  # 要下单的类型，0 卖出 1 购买
        params = {'marketId': market_id, 'amount': amount, 'price': price, 'rangeType': 0, 'type': 1}
        param = json.dumps(params)
        timestamp = str(int(time.time() * 1000))
        sig_str = server_id + timestamp + param + http_key
        signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
        header = {'Clienttype': '0', 'Serverid': server_id, 'Userid': UserId, 'Timestamp': timestamp, 'Sign': signature, 'Lan': 'cn'}
        r_sell = requests.request(method='POST', url=base_url + API_ADD_ENTRUST, headers=header, json=params, verify=False)
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # 当前时间
        result_sell = r_sell.json()
        print('用户：{}；下单时间：{}；结果：{}'.format(UserId, time_now, result_sell))


if __name__ == '__main__':
    market_name = "zt_usdt"
    market_id = '336'
    amount = '10'  # 购买数量
    user_id_list = ['7eqJKPUylZY']

    while True:
        # 获取盘口深度数据
        path_entrusts = 'http://179kline.zbg.com/api/data/v1/entrusts?marketId={}&dataSize=1'.format(market_id)
        r_entrusts = requests.get(url=path_entrusts, verify=False)
        data = r_entrusts.json()
        print(data)
        # 获取盘口最高买单价格
        bids_price = float(data['datas']['bids'][0][0])
        # 获取盘口最低卖单价格
        asks_price = float(data['datas']['asks'][0][0])
        print('最高买单价格:{}，最低卖单价格{}'.format(bids_price, asks_price))
        # 在最高买单和最低卖单价格上取值（8位小数）
        price = round(random.uniform(bids_price, asks_price), 8)
        n = int(len(user_id_list))
        # print('循环次数', n)
        for i in range(0, n):
            user_id = user_id_list[i]
            # print('I的值为：{},userid为{}'.format(i, user_id), type(i))
            t = threading.Thread(target=buy, args=(i, user_id, market_name, amount, price,))
            t.start()
        time.sleep(6)





