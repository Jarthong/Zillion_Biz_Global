from http_utils_api import *
import json, datetime
from time import sleep

# 2 下单 入参：市场名称，下单类型（buy/sell），价格，数量
def create_param(market_name, side, price, amount):
    api_url = '/exchange/api/v1/order/create'
    params = {'symbol': market_name, 'side': side, 'price': price, 'amount': amount}
    # r = signed_request('POST', base_url + api_url, **params)
    r = signed_request_post(api_url, **params)
    print('下单:{}\n{}\n{}'.format(datetime.datetime.now(), r, '-' * 100))

def create():
    api_url = '/exchange/api/v1/order/create'
    params = {'symbol': 'zt_usdt', 'side': 'buy', 'price': '0.05', 'amount': '0.01'}
    r = signed_request_post(api_url, **params)
    print('下单:\n{}\n{}'.format(r, '-' * 100))

# 2 批量取消委托
def cancel_entrust_more(market_name):
    api_url = '/exchange/entrust/controller/website/EntrustController/cancelEntrustMore'
    params = {'marketName': market_name}
    r = signed_request_post(api_url, **params)
    print('批量取消委托:\n{}\n{}'.format(r, '-' * 100))


if __name__ == '__main__':
    # create()
    # cancel_entrust_more('box_zt')  # 批量取消委托，入参：市场名称
    # create_param('box_zt', 'sell', 0.44, 0.1)
    while True:
        create_param('box_zt', 'sell', 0.44, 0.1)  # 下单 入参：市场名称，下单类型（buy/sell），价格，数量
        sleep(0.1)
