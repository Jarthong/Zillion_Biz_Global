import requests, hashlib
import time, datetime, random
import json
import math
# import get_market_id

# 测试环境  990（ID:7ezdaxgBgC8，Google:IHKWBKQZUHBHOBWI）,330（7gwUzgkdsdE）,440(cc)
# base_url = 'http://179.zbg.com'
# user_id = '7ezdaxgBgC8'
# server_id = 'exxxx-xxx'
# http_key = '3a659xxxxxxxxxxxxxc73e'
# secret = 'IHKWBKQZUHBHOBWI'

# 线上环境
# base_url = 'http://boss.zbg.com'   # 域名
base_url = 'https://www.zbg.com'
# base_url = 'https://ae.zbg.com'
user_id = '7fxxxxxxxxx'
server_id = 'exch-xxxxxxxxxx'
http_key = '71a80xxxxxxxxxxxx-xxxxxx3f'
# 新增委托单接口
API_ADD_ENTRUST = '/exchange/entrust/controller/website/EntrustController/addEntrust'
market_id = '5052'   # 交易市场id号   462(untz_zt)  364(qc_zt) 464(bhtx_zt)  336(zt_usdt)
entrust_type = 1  # 要下单的类型，0 卖出 1 购买
amount = 0.5    # 购买数量
'''
price = 7.2  # 初始价格
rang = 0.1     # 涨幅
def decimals(Price, n):
    price_a = Price * (1 + rang) ** n * 10000
    price_a_1 = round(price_a, 8)   # 一位小数的时候，计算出来会有15位小数，且最后一位小数是1,要舍去，所有先取8位小数
    price_b = math.ceil(price_a_1)  # 进一取整
    price_c = price_b / 10000       # 还原为4位小数
    return price_c
'''
time_today = datetime.datetime.today().strftime('%Y%m%d')
# print(time_today, type(time_today))
if time_today == '20190607':
    price = 7.865
elif time_today == '20190608':
    price = 8.6515
elif time_today == '20190609':
    price = 9.5167
elif time_today == '20190610':
    price = 10.4684
else:
    price = 0
# print('价格是：{}'.format(price))

timestamp1 = int(time.time())
while True:
    timestamp2 = int(time.time())
    times = timestamp2 - timestamp1
    print('时间{}秒'.format(times))
    if times > 800:
        exit()
    else:
        # time.sleep(0.5)
        params = {'marketId': market_id, 'amount': amount, 'price': price, 'rangeType': 0, 'type': entrust_type}
        param = json.dumps(params)
        timestamp = str(int(time.time() * 1000))
        sig_str = server_id + timestamp + param + http_key
        signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
        header = {'Clienttype': '0', 'Serverid': server_id, 'Userid': user_id, 'Timestamp': timestamp, 'Sign': signature}
        r_sell = requests.request(method='POST', url=base_url + API_ADD_ENTRUST, headers=header, json=params, verify=False)
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # 当前时间
        result_sell = r_sell.json()['resMsg']
        print('买单时间：', time_now, '结果：', result_sell)


