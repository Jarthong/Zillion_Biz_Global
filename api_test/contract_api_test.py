from http_utils_api import *
import json

# 新增委托单  入参 quantity是‘下单量’   side：买1，卖-1
def add_entrust(quantity, side):
    api_url = '/exchange/api/v1/future/place'
    params = {'contractId': 999999, 'marginRate': 0, 'marginType': 1, 'orderSubType': 0, 'orderType': 3,
              'positionEffect': 1, 'price': '', 'quantity': quantity, 'side': side}
    r = signed_request_post(api_url, **params)
    # r = signed_request('POST', base_url + api_url, **params)
    print('新增委托单:\n{}\n{}'.format(r, '-' * 100))

# 市价全平  quantity：平仓数量   side：买1，卖-1
def place(quantity, side):
    api_url = '/exchange/api/v1/future/place'
    params = {'contractId': 999999, 'marginRate': 0, 'marginType': 1, 'orderSubType': 0, 'orderType': 3,
              'positionEffect': 2, 'price': '', 'quantity': quantity, 'side': side}
    r = signed_request_post(api_url, **params)
    print('新增委托单:\n{}\n{}'.format(r, '-' * 100))


# 合约持仓查询
def select_positions():
    api_url = '/exchange/api/v1/future/positions'
    r = signed_request_get(api_url)
    # print('2 合约持仓查询:\n{}\n{}'.format(r, '-' * 100))
    print('合约持仓查询:\n{}\n{}'.format(json.dumps(r, indent=4, sort_keys=True), '-' * 100))

# 查询合约历史委托
def select_his():
    api_url = '/exchange/api/v1/future/orders/his'
    params = {'symbol': 'btc_zusd'}
    r = signed_request_get(api_url, **params)
    print('查询合约历史委托:\n{}\n{}'.format(json.dumps(r, indent=4, sort_keys=True), '-' * 100))

# 合约撤单
def cancel(orderId):
    api_url = '/exchange/api/v1/future/cancel'
    params = {'symbol': 'btc_zusd', 'orderId': orderId}
    r = signed_request_post(api_url, **params)
    print('查询合约历史委托:\n{}\n{}'.format(json.dumps(r, indent=4, sort_keys=True), '-' * 100))

# 合约一键撤单
def cancel_all():
    api_url = '/exchange/api/v1/future/cancel-all'
    r = signed_request_post(api_url)
    print('合约一键撤单:\n{}\n{}'.format(json.dumps(r, indent=4, sort_keys=True), '-' * 100))



if __name__ == '__main__':
    add_entrust('200', 1)  # 新增委托单
    # place('200', -1)   # 平仓
    select_positions()  # 合约持仓查询  posiQty：持仓量  持仓量>0表示多头（买），持仓量<0表示空头（卖）

    # select_his()  # 查询合约历史委托
    # cancel('11591898246396478')  # 合约撤单
    # cancel_all()  # 合约一键撤单


