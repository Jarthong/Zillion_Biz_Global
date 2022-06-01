import requests, hashlib
import time, datetime, random
import json
# import jarthong_zbg_GetMarketId
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 线上环境
base_url = 'https://ae.zbg.com'
key = '7rv1LqaG7gHLrv1NgHNqaH'  # 9909
secret = '072760618fb10fe43a5aee93d39c27c2'
pass_phrase = '786699'  # 访问口令

# 测试环境
# base_url = 'http://179.zbg.com'
# key = '7rutpEUjzCi7rutpEUjzCj'  # 13100000394
# secret = 'e0eb6d27616ddce3ab1d62ddcb1cf981'  # 76c39be932f1d433ccf75b8901d159fa
# pass_phrase = '999000'  # 访问口令

# 新增委托单接口
API_ADD_ENTRUST = '/exchange/entrust/controller/website/EntrustController/addEntrust'
# 设置要下单的市场
# market_name = 'zb_qc'
# market_id = jarthong_zbg_GetMarketId.getID(market_name)
market_id = '336'   # 交易市场id号
num = 2          # 要撮合的数量
min_amount = 0.01   # 随机最小购买数量
max_amount = 0.1  # 随机最大购买数量
min_price = 0.0322     # 随机最小下单价格
max_price = 0.0325    # 随机最大下单价格

while True:
    for i in range(0, num):
        timestamp = str(int(time.time() * 1000))
        amount_float = random.uniform(min_amount, max_amount)  # 随机生成要下单的浮点数量
        amount = round(amount_float, 2)  # 生成要下单的两位小数精度的数量
        print('随机生成要下单的数量：', amount)
        price_float = random.uniform(min_price, max_price)     # 随机生成要下单的浮点价格
        price = round(price_float, 2)  # 生成要下单的两位小数点精度的价格
        print('随机生成要下单的价格：', price)
        print('-'*100)
        time.sleep(1)

        for j in range(0, 2):
            if j == 0:
                number = random.randint(0, 1)
                # print('number:', number)
                entrust_type = number  # 要下单的类型，0 卖出 1 购买
                params = {'marketId': market_id, 'amount': amount, 'price': price, 'rangeType': 0, 'type': entrust_type}
                param = json.dumps(params)
                sig_str = key + timestamp + param + secret
                signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
                phrase = hashlib.md5((timestamp+pass_phrase).encode('utf-8')).hexdigest()
                header = {'Apiid': key, 'Timestamp': timestamp, "Passphrase": phrase, 'Sign': signature}
                try:
                    r_sell = requests.request(method='POST', url=base_url + API_ADD_ENTRUST, headers=header, json=params, verify=False)
                    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # 当前时间
                    result_sell = r_sell.json()
                    print('买单时间：', time_now, '', result_sell)
                except Exception as message:
                    print('下单报错，报错信息如下：', message)
            else:
                if number == 0:
                    entrust_type = 1  # 要下单的类型，0 卖出 1 购买
                else:
                    entrust_type = 0
                params = {'marketId': market_id, 'amount': amount, 'price': price, 'rangeType': 0, 'type': entrust_type}
                param = json.dumps(params)
                sig_str = key + timestamp + param + secret
                signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
                phrase = hashlib.md5((timestamp + pass_phrase).encode('utf-8')).hexdigest()
                header = {'Apiid': key, 'Timestamp': timestamp, "Passphrase": phrase, 'Sign': signature}
                try:
                    r_buy = requests.request(method='POST', url=base_url + API_ADD_ENTRUST, headers=header, json=params, verify=False)
                    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # 当前时间
                    result_buy = r_buy.json()
                    print('卖单时间：', time_now, '', result_buy)
                except Exception as message:
                    print('下单报错，报错信息如下：', message)
    time.sleep(7)





