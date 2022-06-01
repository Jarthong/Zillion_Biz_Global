import requests, hashlib
import time, datetime, random
import json
import threading

# base_url = 'http://boss.zbg.com'   # 域名
base_url = 'https://www.zbg.com'
user_id_list = ['7fxxxxxxxxx','XXXXXXXXX']
server_id = 'xxxx-xxxxxxxxxx'
http_key = 'xxxxxxxxxxxxxx-xxxxxxxx'
# 交易市场id号   462(untz_zt)  364(qc_zt) 464(bhtx_zt) bitw_zt(474) bitw_usdt(475)
market_id_list = ['474', '475']
m = int(len(market_id_list))

# 测试环境  990（ID:7ezdaxgBgC8，Google:IHKWBKQZUHBHOBWI）,330（7gwUzgkdsdE）,440(7gtW9L90fsO)
# base_url = 'http://179.zbg.com'
# user_id_list = ['7ezdaxgBgC8', '7gwUzgkdsdE']
# server_id = 'exxxx-xxx'
# http_key = '3a659xxxxxxxxxxxxxc73e'
# secret = 'IHKHBHWBKQZUOBWI'
# # market_id = '103'  # zb_zt(103)
# market_id_list = ['100', '103']
# m = int(len(market_id_list))

# 新增委托单接口
API_ADD_ENTRUST = '/exchange/entrust/controller/website/EntrustController/addEntrust'
entrust_type = 1  # 要下单的类型，0 卖出 1 购买
# amount = 20    # 购买数量
# price = 2.1571     # 下单价格
amount_list = [182, 150]
price_list = [26, 1.52]

def buy(UserId, MarketId, Amount, Price):
    params = {'marketId': MarketId, 'amount': Amount, 'price': Price, 'rangeType': 0, 'type': entrust_type}
    param = json.dumps(params)
    timestamp = str(int(time.time() * 1000))
    sig_str = server_id + timestamp + param + http_key
    signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
    header = {'Clienttype': '0', 'Serverid': server_id, 'Userid': UserId, 'Timestamp': timestamp, 'Sign': signature}
    r_sell = requests.request(method='POST', url=base_url + API_ADD_ENTRUST, headers=header, json=params, verify=False)
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # 当前时间
    result_sell = r_sell.json()['resMsg']
    # print('买单时间：', time_now, '结果：', result_sell)
    print('下单用户：{}；市场{}；数量{}；价格{}；时间:{}；结果:{}\n'.format(UserId, MarketId, Amount, Price, time_now, result_sell))

while True:
    # time.sleep(1)
    for i in user_id_list:
        # print('此次使用的ID：', i)
        for j in range(0, m):
            t = threading.Thread(target=buy, args=(i, market_id_list[j], amount_list[j], price_list[j]))
            t.start()



