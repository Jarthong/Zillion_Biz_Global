import requests, hashlib
import time
import json

# 线上环境
# base_url = 'http://boss.zbg.com'   # 域名
base_url = 'https://www.zbg.com'
user_id = '7eqylUPZUtY'
server_id = 'exch-xxxxxxxxxx'
http_key = '71a80xxxxxxxxxxxx-xxxxxx3f'

# 测试环境  990（ID:7eaxgBzdgC8，Google:IHKHOBWKHBBKQZWI）,330（7gwUzgkdsdE）
# base_url = 'http://179.zbg.com'
# user_id = '7ezdaxgBgC8'
# server_id = 'eXXXXXXX'
# http_key = '3a65XXXXXXXXXXXXXX'
# secret = 'IZUHBHKQBOHKWBWI'

timestamp = str(int(time.time() * 1000))
param = ''
# p = json.dumps(param)
sig_str = server_id + timestamp + param + http_key
signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
# header = {'Apiid': key, 'Timestamp': timestamp, 'Sign': signature}
header = {'Clienttype': '0', 'Serverid': server_id, 'Userid': user_id, 'Timestamp': timestamp, 'Sign': signature}

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
    # 线上：untz_zt   bhtx_zt  bitw_zt(474) bitw_usdt(475)
    # 测试：zb_zt（103）  zt_usdt(100)
    getID('bitw_usdt')
    # getName('393')


