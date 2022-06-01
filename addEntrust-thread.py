import requests,hashlib
import time, datetime, random
import json
import urllib3
import threading
# import jarthong_zbg_GetMarketId

# 线上环境
# base_url = 'https://www.zbg.com'
# key = '7hvihvikFlVA7J86uJV6ZB'  # 9909
# secret = '57abc27e60a0c0e1e148c5abd098af6d'

# 测试环境
# base_url = 'http://179.boss.zbg.com'
base_url = 'http://178.zbg.com'

key = '85bCTw5bCTwAaiBc8AaiBd'  # 990908814@qq.com
secret = '3cac9ee1a07b6ddc3bd9ab76f9c28d62'
# pass_phrase = ''  # API访问口令



# 合盘测试环境
# base_url = 'http://zbgtest.bwpool.net'
# key = '7iWSsw1OCY47iWSsw1OCY5'  # 990908814@qq.com
# secret = '90c80d3688fd87023f9a1d8235b53443'

# 合盘测试环境
# base_url = 'http://zbgtest.bwpool.net'
# key = '7iWSoAcMArI7iWSoAcMArJ'  # 4400@qq.com
# secret = '7f59e03ccf85cc465eb034d5dd8db4e0'

# 新增委托单
API_ADD_ENTRUST = "/exchange/entrust/controller/website/EntrustController/addEntrust"
# 设置要下单的市场
# market_name = 'zb_qc'
# market_id = jarthong_zbg_GetMarketId.getID(market_name)
market_id1 = '336'   # 交易市场id号
market_id2 = '336'
market_id_list = [market_id1, market_id2]
num = 2          # 要撮合的数量
min_amount = 1    # 随机最小购买数量
max_amount = 2  # 随机最大购买数量
min_price = 1     # 随机最小下单价格
max_price = 3    # 随机最大下单价格
# price = str(price_num)
number = 5

def order(market_id_random,amount,price,entrust_type):
    params = {'marketId': market_id_random, 'amount': amount, 'price': price, 'rangeType': 0, 'type': entrust_type}
    param = json.dumps(params)
    # 随机生成key和secret
    # number = random.randint(4, 7)
    # key = eval('key' + str(number))
    # secret = eval('secret' + str(number))
    # print('下卖单的key值是', key)
    # print('下卖单的keysecret值是', secret)
    sig_str = key + timestamp + param + secret
    signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
    header = {'Apiid': key, 'Timestamp': timestamp, 'Sign': signature}
    print(base_url + API_ADD_ENTRUST)
    r_sell = requests.request(method='POST', url=base_url + API_ADD_ENTRUST, headers=header, json=params, verify=False)
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # 当前时间
    result_sell = r_sell.json()
    print('下单时间：', time_now, '', result_sell)


while True:
    for i in range(0, num):
        timestamp = str(int(time.time() * 1000))
        amount_float = random.uniform(min_amount, max_amount)  # 随机生成要下单的浮点数量
        amount = round(amount_float, 2)  # 生成要下单的两位小数精度的数量
        print('随机生成要下单的数量：', amount)
        price_float = random.uniform(min_price, max_price)     # 随机生成要下单的浮点价格
        price = round(price_float, 2)  # 生成要下单的两位小数点精度的价格
        print('随机生成要下单的价格：', price)
        market_id_random = random.choice(market_id_list)
        print('下单的市场id号是：', market_id_random)
        print('-'*100)

        for j in range(0, 2):
            if j == 0:
                entrust_type = 0  # 要下单的类型，0 卖出 1 购买
                # order(market_id_random,amount,price,entrust_type)
                for i in range(0, number):
                    # t = threading.Thread(target=buy, args=(user_id_list[i], market_name, amount, price_list[i],))
                    # 在最高买单和最低卖单价格上取值（8位小数）
                    # price = round(random.uniform(bids_price, asks_price), 8)
                    t = threading.Thread(target=order, args=(market_id_random,amount,price,entrust_type,))
                    t.start()
                time.sleep(2)

            else:
                entrust_type = 1  # 要下单的类型，0 卖出 1 购买
                # order(market_id_random, amount, price, entrust_type)
                for i in range(0, number):
                    # t = threading.Thread(target=buy, args=(user_id_list[i], market_name, amount, price_list[i],))
                    # 在最高买单和最低卖单价格上取值（8位小数）
                    # price = round(random.uniform(bids_price, asks_price), 8)
                    t = threading.Thread(target=order, args=(market_id_random,amount,price,entrust_type,))
                    t.start()
                time.sleep(2)





