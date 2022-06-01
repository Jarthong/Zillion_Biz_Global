'''撤单的脚本'''
import requests, hashlib
import time, datetime, random
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 线上环境
# base_url = 'http://boss.zbg.com'   # 域名
# base_url = 'https://www.zbg.com'
# # # base_url = 'https://ae.zbg.com'
# user_id = '7fxxxxxxxxx'
# server_id = 'exch-xxxxxxxxxx'
# http_key = '71a80xxxxxxxxxxxx-xxxxxx3f'
# url = '/exchange/fund/controller/website/FreezeController/getExFreezeRecord'

# 测试环境  990（ID:7ezdaxgBgC8，Google:IHKWBKQZUHBHOBWI）,330（7gwUzgkdsdE）  15915774459_google(5XBNLYUSQ6YJVXK4)
base_url = 'http://179.zbg.com'
user_id = '7puZCO60k1g'
server_id = 'exxxx-xxx'
http_key = '3a659xxxxxxxxxxxxxc73e'
url = '/exchange/fund/controller/website/FreezeController/getExFreezeRecord'


def getExFreezeRecord(pageSize):
    params = {"pageNum": 1, "pageSize": pageSize, "status": "0", "freezeType": "1"}
    param = json.dumps(params)
    timestamp = str(int(time.time() * 1000))
    sig_str = server_id + timestamp + param + http_key
    signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
    header = {'Clienttype': '0', 'Serverid': server_id, 'Userid': user_id, 'Timestamp': timestamp, 'Sign': signature}
    r_get = requests.request(method='POST', url=base_url + url, headers=header, json=params, verify=False)
    # print(r_get.json())
    # print(json.dumps(r_get.json(), indent=4, sort_keys=True))
    return r_get.json()


# 获取总订单条数
totalRow = getExFreezeRecord(1)['datas']['totalRow']
print('订单条数：', totalRow, type(totalRow))

# 把所有的市场编号和订单放入数组中
result_get = getExFreezeRecord(totalRow)
# 获取页面的所有市场编号
list_marketId = []
for i in range(0, totalRow):
    entrustId = result_get['datas']['list'][i]['marketId']
    list_marketId.append(entrustId)
print(list_marketId)

# 获取页面的所有订单编号
list_entrustId = []
for k in range(0, totalRow):
    entrustId = result_get['datas']['list'][k]['EntrustId']
    list_entrustId.append(entrustId)
print(list_entrustId)

# 取消订单
url_cancel = '/exchange/entrust/controller/website/EntrustController/cancelEntrust'
for j in range(0, totalRow):
    params1 = {"marketId": list_marketId[j], "entrustId": list_entrustId[j]}
    param1 = json.dumps(params1)
    timestamp1 = str(int(time.time() * 1000))
    sig_str1 = server_id + timestamp1 + param1 + http_key
    signature1 = hashlib.md5(sig_str1.encode('utf-8')).hexdigest()
    header1 = {'Clienttype': '0', 'Serverid': server_id, 'Userid': user_id, 'Timestamp': timestamp1, 'Sign': signature1}
    r_cancel = requests.request(method='POST', url=base_url + url_cancel, headers=header1, json=params1, verify=False)
    result_cancel = r_cancel.json()
    print(result_cancel)
