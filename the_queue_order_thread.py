import requests, hashlib
import time, datetime, random
import json
# import jarthong_zbg_GetMarketId
import urllib3
import threading

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 测试环境
base_url = 'http://179.zbg.com'
user_id = '7pu2HvNZCTI'
server_id = 'eXXXXXXX'
http_key = '3a65XXXXXXXXXXXXXX'

# 队列下单
api_url = '/exchange/api/v1/order/queue-order'
def buy(UserId, market_name, amount, price):
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
    time.sleep(1)

if __name__ == '__main__':
    market_name = "zb_usdt"
    market_id = '98'
    amount = '10'  # 购买数量
    user_id_list = ['7puZCQXs8cC', '7puZCT2HvNI', '7puZCVqI26q']   # 13100000398,13100000399, 13100000400
    # price_list = ['6', '6', '6']

    while True:
        # 获取盘口深度数据
        path_entrusts = 'http://179kline.zbg.com/api/data/v1/entrusts?marketId={}&dataSize=1'.format(market_id)
        r_entrusts = requests.get(url=path_entrusts, verify=False)
        data = r_entrusts.json()
        # print(data)
        # 获取盘口最高买单价格
        bids_price = float(data['datas']['bids'][0][0])
        # 获取盘口最低卖单价格
        asks_price = float(data['datas']['asks'][0][0])
        print('最高买单价格:{}，最低卖单价格'.format(bids_price, asks_price))
        for i in range(0, int(len(user_id_list))):
            # t = threading.Thread(target=buy, args=(user_id_list[i], market_name, amount, price_list[i],))
            # 在最高买单和最低卖单价格上取值（8位小数）
            price = round(random.uniform(bids_price, asks_price), 8)
            t = threading.Thread(target=buy, args=(user_id_list[i], market_name, amount, price,))
            t.start()
        time.sleep(6)





