# ! /usr/bin/env python
# -*- coding:utf-8 -*-
from ws4py.client.threadedclient import WebSocketClient
import time
import hashlib
import requests
import json
"""
订阅行情，在买1卖1平均价自买自卖（未处理不成交的情况）
"""


class Zbg:
    def __init__(self, key, secret):
        self.base_url = 'https://api.zbg.com'
        # self.base_url == 'https://www.zbg.com'  # 上面地址不行换这个
        self.key = key
        self.secret = secret


    def public_request(self, method, api_url, **payload):
        """request public url"""

        r_url = 'https://kline.zbg.com/api/data/v1/' + api_url
        try:
            r = requests.request(method, r_url, params=payload)
            r.raise_for_status()
            if r.status_code == 200:
                return True, r.json()
            else:
                return False, {'error': 'E10000', 'data': r.status_code}
        except requests.exceptions.HTTPError as err:
            return False, {'error': 'E10001', 'data': r.text}
        except Exception as err:
            return False, {'error': 'E10002', 'data': err}

    def signed_request(self, method, api_url, **payload):
        """request a signed url"""
        timestamp = str(int(time.time() * 1000))
        full_url = self.base_url + api_url

        param = ''
        if method == 'GET' and payload:
            for k in sorted(payload):
                param += k + payload[k]
        elif method == 'POST' and payload:
            param = json.dumps(payload)
        elif not payload:
            payload = ''

        sig_str = self.key + timestamp + param + self.secret
        signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()

        headers = {
            'Apiid': self.key,
            'Timestamp': timestamp,
            'Sign': signature
        }

        try:
            r = requests.request(method, full_url, headers=headers, json=payload) if method == 'POST' else requests.request(method, full_url, headers=headers, data=payload)
            r.raise_for_status()
            if r.status_code == 200:
                return True, r.json()
            else:
                return False, {'error': 'E10000', 'data': r.status_code}
        except requests.exceptions.HTTPError as err:
            return False, {'error': 'E10001', 'data': r.text}
        except Exception as err:
            return False, {'error': 'E10002', 'data': err}

    # 获取用户所有资金信息
    def get_balance(self):
        a = {"pageSize": "30", "pageNum": "1"}
        return self.signed_request('POST', '/exchange/fund/controller/website/fundcontroller/findbypage', **a)

    def get_info(self):
        return self.signed_request('POST', '/exchange/user/controller/website/usercontroller/getuserinfo')

    # 查询提币地址
    def get_PayinAddress(self, name="btc"):
        a = {"currencyTypeName": name}
        return self.signed_request('POST', '/exchange/fund/controller/website/fundwebsitecontroller/getwithdrawaddress', **a)

    # 获取市场列表
    def get_market(self):
        return self.signed_request('POST', '/exchange/config/controller/website/marketcontroller/getByWebId')

    # 新增委托
    def create_order(self, **payload):
        """create order"""
        return self.signed_request('POST', '/exchange/entrust/controller/website/EntrustController/addEntrust', **payload)

    def buy(self, marketId, price, amount):
        """buy someting"""
        return self.create_order(marketId=marketId, type=1, rangeType=0, price=price, amount=amount)

    def sell(self, marketId, price, amount):
        """buy someting"""
        return self.create_order(marketId=marketId, type=0, rangeType=0, price=price, amount=amount)

    # 取消委托
    def cancel_order(self, entrustId, marketId):
        payload = {'entrustId': entrustId, 'marketId': marketId}
        return self.signed_request('POST', '/exchange/entrust/controller/website/EntrustController/cancelEntrust', **payload)

    # 查询正在进行的委托
    def get_unfinish_order(self, marketId):
        return self.signed_request('GET', '/exchange/entrust/controller/website/EntrustController/getUserEntrustRecordFromCache', marketId=marketId)

    def get_depth(self, marketId):
        a = {'marketId': marketId}
        depth = self.public_request('GET', 'entrusts', **a)
        return depth


class ZbgClient(WebSocketClient):
    def __init__(self, url):
        super(ZbgClient, self).__init__(url)
        self.z = Zbg(key='key', secret='secret')
        self.symbol = 'zt_usdt'  # 刷别的币对自己改
        self.vol = 0.001  # 单次下单量，注意保证币的数量是充足的

        market = self.z.get_market()
        if market[0] and 'datas' in market[1]:
            for cur in market[1]['datas']:
                if cur['name'] == self.symbol:
                    self.marketId = cur['marketId']  # 市场id
                    self.price_decimal = cur['priceDecimal']  # 报价精度
                    self.amount_decimal = cur['amountDecimal']  # 委托精度
                    self.buy_id = int(cur['buyerCurrencyId'])  # 买方币种id
                    self.sell_id = int(cur['sellerCurrencyId'])  # 卖方币种id
                    self.min_amount = float(cur['minAmount'])  # 最小委托量

        self.price_tick = 10 ** (-self.price_decimal)  # 最小价格变动单位
        self.data = {'asks': [], 'bids': [], 'ts': 0}
        self.ts = 0

    def opened(self):
        self.send('{"dataType": "' + self.marketId + '_ENTRUST_ADD_' + self.symbol.upper() + '","dataSize":1000,"action":"ADD"}')

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, m):
        data = eval(str(m))
        if data[0] != 'E' and data[0][0] == 'AE':
            self.data['asks'] = data[0][4]['asks']
            self.data['bids'] = data[0][5]['bids']
            self.data['ts'] = data[0][3]
        elif data[0] == 'E':
            self.data['ts'] = data[2]
            self.update_data(data)

        ts = int(self.data['ts'])
        if ts > self.ts:  # 一秒刷一次，想刷快点也可以放开，不过好像平台有一秒3次访问限制
            self.update_trade()
            if ts // 5 > self.ts // 5:  # 推送盘口是增量更新，有时候会丢包，每隔5s用http较正一次，每隔5s撤一次单
                self.update_depth()

        self.ts = ts

    def update_data(self, data):
        side = data[4].lower() + 's'
        for i in range(len(self.data[side])):
            if self.data[side][i][0] == data[5]:
                if data[6] != '0':
                    self.data[side][i][1] = data[6]
                else:
                    self.data[side].pop(i)
                return
            elif float(data[5]) > float(self.data[side][i][0]) and data[6] != '0':
                self.data[side].insert(i, [data[5], data[6]])
                return

        if data[6] != '0':
            self.data[side].append([data[5], data[6]])

    def update_trade(self):
        ask1 = float(self.data['asks'][-1][0])
        bid1 = float(self.data['bids'][0][0])
        if ask1 - bid1 < self.price_tick * 1.5:
            print('ask1 bid1 太接近,无法刷单!\t{}\t{}'.format(ask1, bid1))
            return

        price = round((ask1 + bid1) / 2, self.price_decimal)
        buy_order = self.z.buy(self.marketId, price, self.vol)
        sell_order = self.z.sell(self.marketId, price, self.vol)
        print('{}\t{}\t{:.4f}\t{:.4f}'.format(self.marketId, self.symbol, price, self.vol))

    def update_depth(self):
        depth = self.z.get_depth(self.marketId)
        if depth[0] and 'datas' in depth[1] and depth[1]['datas']:
            self.data['asks'] = depth[1]['datas']['asks']
            self.data['bids'] = depth[1]['datas']['bids']

        orders = self.z.get_unfinish_order(self.marketId)
        if orders[0] and 'datas' in orders[1]:
            print('定时撤单!')
            for order in orders[1]['datas']:
                self.z.cancel_order(order['entrustId'], self.marketId)


if __name__ == '__main__':
    ws = ZbgClient('wss://kline.zbg.com/websocket')
    if hasattr(ws, 'marketId'):
        ws.connect()
        ws.run_forever()
    else:
        print("can't get marketId!")



