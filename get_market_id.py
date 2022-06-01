import requests, hashlib
import time
import json

# 线上环境990908814@qq.com
# base_url = 'https://www.zbg.com'
# key = '7h6ZJVd7hvFlFlivi6ZgVB'
# secret = '57a27e8a5ded09bcf60a0c0b6a1h648c'

# 测试环境
# base_url = 'http://179.boss.zbg.com'
base_url = 'http://178.zbg.com/'
key = '7hxE8V6PPeq7hxE8V6PPer'
secret = 'df8f4d2dfcee48a3a36b95747ac160b1'

# 测试环境 --给同事用
# base_url = 'http://179.boss.zbg.com'
# base_url = 'http://178.zbg.com/'
# key = '89blwqtYfIW89blwqtYfIX'
# secret = '936924986861a784b63bb8652fa845b4'

# 合盘测试环境
# base_url = 'http://zbgtest.bwpool.net'
# key = '7iWSoAcAcMMArI7iWSoArJ'  # 4400@qq.com
# secret = '7f59e03cc465eb034dcf85c5dd8db4e0'

timestamp = str(int(time.time() * 1000))
param = ''
# p = json.dumps(param)
sig_str = key + timestamp + param + secret
signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
header = {'Apiid': key, 'Timestamp': timestamp, 'Sign': signature}

# 查询market列表
API_GET_MARKET_LIST = "/exchange/config/controller/website/marketcontroller/getByWebId"
r = requests.post(base_url + API_GET_MARKET_LIST, data=param, headers=header, verify=False)
r1 = r.json()
print(r1['resMsg'])
# r2 = json.dumps(r1, indent=4, sort_keys=True)
# print('查询市场列表:\n', r1)
market_num = len(r1['datas'])
# print(type(market_num), market_num)
market_name_list = []
market_id_list = []
for i in range(0, market_num):
    data_name = r1['datas'][i]['name']
    data_id = r1['datas'][i]['marketId']
    # if data_name == market:
    #     print('交易对', market, '对应的市场ID是：', data_id)
    #     break
    market_name_list.append(data_name)
    market_id_list.append(data_id)
print('当前环境有以下这些市场名称：', market_name_list)
print('当前环境的市场名称对应的ID：', market_id_list)

# 根据市场id号查询市场名称
def getName(market_id):
    if market_id in market_id_list:
        for j in range(0, market_num):
            if market_id_list[j] == market_id:
                market_name = market_name_list[j]
                print(market_id, '的市场名字是:', market_name)
                break
    else:
        return print('您所输入的市场id不存在，请检查！')


# 检查交易对是否在数组里，并输出市场ID
def getID(market):
    if market in market_name_list:
        for j in range(0, market_num):
            if market_name_list[j] == market:
                marker_id = market_id_list[j]
                # return marker_id
                print('交易对', market, '对应的市场ID是：', marker_id)
                break
    else:
        return print('您所输入的市场交易对不存在，请检查！')


if __name__ == '__main__':
    getID('btc_usdt')
    # getName('393')


