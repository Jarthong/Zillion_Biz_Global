import config_params
from http_utils import *
from custom_error import CustomError
import json
base_url = 'http://178.zbg.com'  # 测试环境


# 1 获取用户信息
def getuserinfo():
    api_url = '/exchange/user/controller/website/usercontroller/getuserinfo'
    r = signed_request('POST', base_url + api_url)
    print('1 获取用户信息:\n{}\n{}'.format(r, '-'*100))

# 1 搜索用户信息
def search():
    api_url = '/exchange/api/v1/account/search'
    params = {'account': '159157735xx', 'account-type': 0, 'google-code': '123456', 'country-code': '+86'}
    r = signed_request('GET', base_url + api_url, **params)
    print('1 搜索用户信息:\n{}\n{}'.format(r, '-' * 100))

# 1 查询当前用户的资产信息
def balance():
    api_url = '/exchange/api/v1/account/balance'
    r = signed_request('GET', base_url + api_url)
    print('1 查询当前用户的资产信息:\n{}\n{}'.format(r, '-' * 100))

# 1 获取用户所有资金信息
def findbypage():
    api_url = '/exchange/fund/controller/website/fundcontroller/findbypage'
    params = {'pageSize': 5, 'pageNum': 1}
    r = signed_request('POST', base_url + api_url, **params)
    print('1 获取用户所有资金信息:\n{}\n{}'.format(r, '-'*100))

# 1 查询当前用户信息及其子账号列表
def accounts():
    api_url = '/exchange/api/v1/account/accounts'
    r = signed_request('GET', base_url + api_url)
    print('1 查询当前用户信息及其子账号列表:\n{}\n{}'.format(r, '-' * 100))

# 2 新增委托
def addEntrust():
    api_url = '/exchange/entrust/controller/website/EntrustController/addEntrust'
    params = {'marketId': '336', 'amount': 1, 'price': 0.0505, 'rangeType': 0, 'type': 0}
    r = signed_request('POST', base_url + api_url, **params)
    print('2 新增委托:\n{}\n{}'.format(r, '-' * 100))
    return r[1]  # 返回订单数据

# 2 查询已提交但是仍未完全成交或未被撤销的订单
def openOrders():
    api_url = '/exchange/api/v1/order/orders'
    params = {'symbol': 'zt_usdt', 'page': 1, 'size': 2}
    r = signed_request('GET', base_url + api_url, **params)
    print('2 查询已提交但是仍未完全成交或未被撤销的订单:\n{}\n{}'.format(r, '-' * 100))

# 2 取消委托
def cancelEntrust():
    api_url = '/exchange/entrust/controller/website/EntrustController/cancelEntrust'
    # params = {'entrustId': addEntrust()['datas']['entrustId'], 'marketName': 'zt_usdt'}
    params = {'entrustId': 'E6658198933195464704', 'marketName': 'zt_usdt'}
    r = signed_request('POST', base_url + api_url, **params)
    print('2 取消委托:\n{}\n{}'.format(r, '-' * 100))

# 2 撤销订单
def cancel():
    api_url = '/exchange/api/v1/order/cancel'
    # params = {'order-id': addEntrust()['datas']['entrustId'], 'symbol': 'zt_usdt'}
    params = {'order-id': 'E6658198933195464704', 'symbol': 'zt_usdt'}
    r = signed_request('POST', base_url + api_url, **params)
    print('2 撤销订单:\n{}\n{}'.format(r, '-' * 100))

# 2 基于搜索条件查询历史订单
def orders():
    api_url = '/exchange/api/v1/order/open-orders'
    # params = {'symbol': 'zt_usdt', 'state': 'partial-filled', 'page': 1, 'size': 10}
    params = {'symbol': 'zt_usdt', 'page': 1, 'size': 2}
    r = signed_request('GET', base_url + api_url, **params)
    print('2 基于搜索条件查询历史订单:\n{}\n{}'.format(r, '-' * 100))

# 2 查询订单详情
def detail():
    api_url = '/exchange/api/v1/order/detail'
    params = {'symbol': 'zt_usdt', 'order-id': 'E6658202485003395072'}
    r = signed_request('GET', base_url + api_url, **params)
    print('2 查询订单详情:\n{}\n{}'.format(r, '-' * 100))

# 2 分页查询正在进行的委托
def getUserEntrustRecord():
    api_url = '/exchange/entrust/controller/website/EntrustController/getUserEntrustRecordFromCacheWithPage'
    params = {'marketName': 'zt_usdt', 'pageIndex': 1, 'pageSize': 1}
    r = signed_request('GET', base_url + api_url, **params)
    print('2 分页查询正在进行的委托:\n{}\n{}'.format(r, '-' * 100))

# 2 根据委托单id查询此委托单的所有成交记录
def gettransactionlistbyentrustid():
    api_url = '/exchange/entrust/controller/website/entrustcontroller/getTransactionListByEntrustId'
    params = {'marketId': '336', 'entrustId': 'E6658204401473167360'}
    r = signed_request('GET', base_url + api_url, **params)
    print('2 根据委托单id查询此委托单的所有成交记录:\n{}\n{}'.format(r, '-' * 100))

# 2 根据委托单id查询委托记录
def getEntrustById():
    api_url = '/exchange/entrust/controller/website/EntrustController/getEntrustById'
    params = {'marketName': 'zt_usdt', 'entrustId': 'E6658204401473167360'}
    r = signed_request('GET', base_url + api_url, **params)
    print('2 根据委托单id查询委托记录:\n{}\n{}'.format(r, '-' * 100))

# 2 分页查询历史委托委托
def getUserEntrustList():
    api_url = '/exchange/entrust/controller/website/EntrustController/getUserEntrustList'
    params = {'marketName': 'zt_usdt', 'pageIndex': 1, 'pageSize': 1, 'status': 2}
    r = signed_request('GET', base_url + api_url, **params)
    print('2 分页查询历史委托委托:\n{}\n{}'.format(r, '-' * 100))

# 2 批量取消委托
def cancel_entrust_more():
    api_url = '/exchange/entrust/controller/website/EntrustController/cancelEntrustMore'
    params = {'marketName': 'zt_usdt'}
    r = signed_request('POST', base_url + api_url, **params)
    print('2 批量取消委托:\n{}\n{}'.format(r, '-' * 100))

# 2 查询正在进行的委托
def get_entrust_record():
    api_url = '/exchange/entrust/controller/website/EntrustController/getUserEntrustRecordFromCache'
    params = {'marketName': 'zt_usdt'}
    r = signed_request('GET', base_url + api_url, **params)
    print('2 查询正在进行的委托:\n{}\n{}'.format(r, '-' * 100))

# 2 批量撤销订单
def batch_cancel():
    api_url = '/exchange/api/v1/order/batch-cancel'
    params = {'symbol': 'zt_usdt'}
    r = signed_request('POST', base_url + api_url, **params)
    print('2 批量取消委托:\n{}\n{}'.format(r, '-' * 100))

# 2 下单 入参：市场名称，下单类型（buy/sell），价格，数量
def create_param(market_name, side, price, amount):
    api_url = '/exchange/api/v1/order/create'
    params = {'symbol': market_name, 'side': side, 'price': price, 'amount': amount}
    r = signed_request('POST', base_url + api_url, **params)
    print(base_url + api_url)
    print('2 下单:\n{}\n{}'.format(r, '-' * 100))

def create():
    api_url = '/exchange/api/v1/order/create'
    params = {'symbol': 'zt_usdt', 'side': 'buy', 'price': '0.05', 'amount': '0.01'}
    r = signed_request('POST', base_url + api_url, **params)
    print('2 下单:\n{}\n{}'.format(r, '-' * 100))

# 查询成交明细
def trades():
    api_url = '/exchange/api/v1/order/trades'
    params = {'symbol': 'zt_usdt', 'order-id': 'E6658204401473167360'}
    r = signed_request('GET', base_url + api_url, **params)
    print('2 查询成交明细:\n{}\n{}'.format(r, '-' * 100))

# 3 提币  签名非法
def doPayoutCoin():
    api_url = '/exchange/fund/controller/website/fundwebsitecontroller/doPayoutCoin'
    params = {"amount": '1', "currencyName": "btc", "address": "1LXuF8s1qpuSA828kipPcTLn3ddufy5hjd"}
    # api_url = '/exchange/api/v1/account/withdraw/create'
    # params = {"amount": 1.0, "currency": "btc", "address": "1LXuF8s1qpuSA828kipPcTLn3ddufy5hjd"}
    r = signed_request('POST', base_url + api_url, **params)
    print('3 提币:\n{}\n{}'.format(r, '-' * 100))

# 3 查询提币地址
def getwithdrawaddress():
    api_url = '/exchange/fund/controller/website/fundwebsitecontroller/getwithdrawaddress'
    params = {'currencyId': '2'}
    r = signed_request('GET', base_url + api_url, **params)
    print('3 查询提币地址:\n{}\n{}'.format(r, '-' * 100))

# 3 获取充币地址
def getPayinAddress():
    api_url = '/exchange/fund/controller/website/fundcontroller/getpayinaddress'
    params = {"currencyTypeName": "ltt"}
    r = signed_request('POST', base_url + api_url, **params)
    print('3 获取充币地址:\n{}\n{}'.format(r, '-' * 100))

# 3 提币记录查询
def history():
    api_url = '/exchange/api/v1/account/withdraw/history'
    params = {'currency': 'zt', 'size': '1'}
    r = signed_request('GET', base_url + api_url, **params)
    print('3 提币记录查询:\n{}\n{}'.format(r, '-' * 100))

# 3 查询充币记录
def getPayinCoinRecord():
    api_url = '/exchange/fund/controller/website/fundcontroller/getpayincoinrecord'
    params = {'currencyTypeName': 'btc', 'pageNum': 1, 'pageSize': 20}
    r = signed_request('POST', base_url + api_url, **params)
    print('3 查询充币记录:\n{}\n{}'.format(r, '-' * 100))

# 3 查询提币记录
def get_pay_out_coin_record():
    api_url = '/exchange/fund/controller/website/fundwebsitecontroller/getpayoutcoinrecord'
    params = {'currencyId': 19, 'tab': 'all'}
    r = signed_request('GET', base_url + api_url, **params)
    print('3 查询提币记录:\n{}\n{}'.format(r, '-' * 100))

# 3 取消提币
def docancelpayout():
    api_url = '/exchange/fund/controller/website/fundwebsitecontroller/docancelpayout'
    params = {'userApplyWithdrawId': '1111'}
    r = signed_request('GET', base_url + api_url, **params)
    print('3 取消提币:\n{}\n{}'.format(r, '-' * 100))

# 3 充币地址查询
def address():
    api_url = '/exchange/api/v1/account/deposit/address'
    params = {'currency': 'btc'}
    r = signed_request('GET', base_url + api_url, **params)
    print('3 充币地址查询:\n{}\n{}'.format(r, '-' * 100))

# 提币地址查询
def with_draw_address():
    api_url = '/exchange/api/v1/account/withdraw/address'
    params = {'currency': 'btc'}
    r = signed_request('GET', base_url + api_url, **params)
    print('3 提币地址查询:\n{}\n{}'.format(r, '-' * 100))

# 3 充币记录查询
def deposit_history():
    api_url = '/exchange/api/v1/account/deposit/history'
    params = {'currency': 'btc', 'page': 1, 'size': 2}
    r = signed_request('GET', base_url + api_url, **params)
    print('3 充币记录查询:\n{}\n{}'.format(r, '-' * 100))

# 3 取消提币
def withdraw_cancel():
    api_url = '/exchange/api/v1/account/withdraw/cancel/1111'
    r = signed_request('POST', base_url + api_url)
    print('3 取消提币:\n{}\n{}'.format(r, '-' * 100))

# 4 子账号余额（汇总）
def aggregate_balance():
    api_url = '/exchange/api/v1/account/sub/aggregate-balance'
    r = signed_request('GET', base_url + api_url)
    print('4 子账号余额（汇总）:\n{}\n{}'.format(r, '-' * 100))

# 4 子账号余额(母账户查询其下指定子账号的各币种余额。)
def sub_balance():
    api_url = '/exchange/api/v1/account/sub/balance/7vJz6SWZ2lk'
    # params = {'sub-uid': '7vJz6SWZ2lk'}
    r = signed_request('GET', base_url + api_url)
    print('4 子账号余额(母账户查询其下指定子账号的各币种余额。):\n{}\n{}'.format(r, '-' * 100))

# 4 资产划转（母子账号之间）
def transfer():
    api_url = '/exchange/api/v1/account/sub/transfer'
    params = {'sub-uid': '7vJz6SWZ2lk', 'currency': 'zt', 'amount': 1, 'type': 'master-transfer-out'}
    r = signed_request('POST', base_url + api_url, **params)
    print('4 资产划转（母子账号之间）:\n{}\n{}'.format(r, '-' * 100))

# 5 合约下单
def place():
    api_url = '/exchange/api/v1/future/place'
    params = {'symbol': 'btc_zusd', 'side': 1, 'quantity': '1', 'orderType': 3,'positionEffect': 1, 'marginType': 2, 'marginRate':'0.2'}
    r = signed_request('POST', base_url + api_url, **params)
    print('5 合约下单:\n{}\n{}'.format(r, '-' * 100))

# 5 查询合约历史委托
def orders_history():
    api_url = '/exchange/api/v1/future/orders/his'
    params = {'symbol': 'btc_zusd'}
    r = signed_request('GET', base_url + api_url, **params)
    print('6 查询合约历史委托:\n{}\n{}'.format(r, '-' * 100))

# 5 查询合约历史强平
def fcorders():
    api_url = '/exchange/api/v1/future/fcorders'
    r = signed_request('GET', base_url + api_url)
    print('5 查询合约历史强平:\n{}\n{}'.format(r, '-' * 100))

# 5 合约撤单
def future_cancel():
    api_url = '/exchange/api/v1/future/cancel'
    params = {'symbol': 'btc_zusd', 'orderId': 'W6574581089036550144'}
    r = signed_request('POST', base_url + api_url, **params)
    print('5 合约撤单:\n{}\n{}'.format(r, '-' * 100))

# 5 合约一键撤单
def future_cancel_all():
    api_url = '/exchange/api/v1/future/cancel-all'
    r = signed_request('POST', base_url + api_url)
    print('5 合约一键撤单:\n{}\n{}'.format(r, '-' * 100))

# 5 合约持仓查询
def positions():
    api_url = '/exchange/api/v1/future/positions'
    r = signed_request('GET', base_url + api_url)
    print('5 合约持仓查询:\n{}\n{}'.format(r, '-' * 100))

# 5 查询合约当前委托
def future_orders():
    api_url = '/exchange/api/v1/future/orders'
    r = signed_request('GET', base_url + api_url)
    print('5 查询合约当前委托:\n{}\n{}'.format(r, '-' * 100))

# 5 调整保证金率
def adjust_margin_rate():
    api_url = '/exchange/api/v1/future/adjust-margin-rate'
    params = {'symbol': 'btc_zusd', 'initMarginRate': '0.5', 'marginType': 2}
    r = signed_request('POST', base_url + api_url, **params)
    print('5 调整保证金率:\n{}\n{}'.format(r, '-' * 100))

# 5 调整保证金
def adjust_margin():
    api_url = '/exchange/api/v1/future/adjust-margin'
    params = {'symbol': 'btc_zusd', 'margin': '500'}
    r = signed_request('POST', base_url + api_url, **params)
    print('5 调整保证金:\n{}\n{}'.format(r, '-' * 100))


# 6 查询合约资金流水
def flow():
    api_url = '/exchange/api/v1/future/assets/flow'
    # params = {'currencyName': 'zusd', 'pageSize': 5}
    r = signed_request('GET', base_url + api_url)
    print('6 查询合约资金流水:\n{}\n{}'.format(r, '-' * 100))

# 6 查询合约可用资金
def available():
    api_url = '/exchange/api/v1/future/assets/available'
    r = signed_request('GET', base_url + api_url)
    print('6 查询合约可用资金:\n{}\n{}'.format(r, '-' * 100))

# 6 查询合约盈亏历史
def profits():
    api_url = '/exchange/api/v1/future/assets/profits'
    # params = {'currencyName': 'zusd', 'pageNum': 1, 'pageSize': 5}
    r = signed_request('GET', base_url + api_url)
    print('6 查询合约盈亏历史:\n{}\n{}'.format(r, '-' * 100))

if __name__ == '__main__':
    # 1
    getuserinfo()
    balance()
    search()

    findbypage()
    accounts()

    # 2
    addEntrust()
    cancelEntrust()
    orders()
    openOrders()
    detail()
    cancel()

    getUserEntrustRecord()
    gettransactionlistbyentrustid()
    getEntrustById()
    getUserEntrustList()
    cancel_entrust_more()
    get_entrust_record()
    batch_cancel()
    create()
    trades()

    # 3
    doPayoutCoin()
    getwithdrawaddress()
    getPayinAddress()

    history()
    getPayinCoinRecord()
    get_pay_out_coin_record()
    docancelpayout()
    address()
    with_draw_address()
    deposit_history()
    withdraw_cancel()

    # 4
    aggregate_balance()
    sub_balance()
    transfer()

    # 5
    place()
    fcorders()
    orders_history()

    future_cancel()
    future_cancel_all()
    positions()
    future_orders()
    adjust_margin_rate()
    adjust_margin()

    # 6
    flow()
    available()
    profits()

    # 下单测试  入参：市场名称，下单类型（buy/sell），价格，数量
    # create_param('zt_usdt', 'sell', 0.055, 1)
    create()

