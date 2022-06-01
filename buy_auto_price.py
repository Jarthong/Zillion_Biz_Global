import requests, hashlib
import time, datetime, random
import json
# import jarthong_zbg_GetMarketId

base_url = 'http://boss.zbg.com'   # 域名
user_id = '7fxxxxxxxxx'
server_id = 'xxxx-xxxxxxxxxx'
http_key = 'xxxxxxxxxxxxxx-xxxxxxxx'

# 新增委托单接口
API_ADD_ENTRUST = '/exchange/entrust/controller/website/EntrustController/addEntrust'
market_id = '5139'   # 交易市场id号   462(untz_zt)  364(qc_zt)  464(bhtx_zt)
entrust_type = 1  # 要下单的类型，0 卖出 1 购买

# amount = 1    # 购买数量
min_price = 1.2     # 下单价格
max_amount = 100  # 涨跌停最大下单量

while True:
    path_entrusts = 'https://kline.zbg.com/api/data/v1/entrusts?marketId={}&dataSize=1'.format(market_id)
    r_entrusts = requests.get(url=path_entrusts, verify=False)
    data = r_entrusts.json()
    # print(data)
    # print(data['datas']['asks'],type(data['datas']['asks']))
    if data['datas']['asks']:
        # 获取盘口最低卖单价格和数量
        price = float(data['datas']['asks'][0][0])
        print('最低价格：', price)
        min_sell_amount = float(data['datas']['asks'][0][1])
        if min_sell_amount < max_amount:
            amount = min_sell_amount
        else:
            amount = max_amount
    else:
        amount = max_amount
        price = min_price
    params = {'marketId': market_id, 'amount': amount, 'price': price, 'rangeType': 0, 'type': entrust_type}
    param = json.dumps(params)
    timestamp = str(int(time.time() * 1000))
    sig_str = server_id + timestamp + param + http_key
    signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
    header = {'Clienttype': '0', 'Serverid': server_id, 'Userid': user_id, 'Timestamp': timestamp, 'Sign': signature}
    r_sell = requests.request(method='POST', url=base_url + API_ADD_ENTRUST, headers=header, json=params, verify=False)
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # 当前时间
    result_sell = r_sell.json()
    print('买单时间：', time_now, '结果：', result_sell, '\n下单价格：', price, '下单数量：', amount)




