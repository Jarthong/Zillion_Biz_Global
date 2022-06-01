# ! /usr/bin/env python
# -*- coding:utf-8 -*-
from ws4py.client.threadedclient import WebSocketClient
from threading import Thread
import time
from datetime import datetime
import hashlib
import requests
import json
import random
import os
from zapi import ZApi


class Zbg:
    def __init__(self, key, secret):
        self.base_url = 'https://www.zbg.com'
        self.key = key
        self.secret = secret

    def switch_url(self):
        if self.base_url == 'https://www.zbg.com':
            self.base_url = 'https://api.zbg.com'
        else:
            self.base_url = 'https://www.zbg.com'

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

    def get_PayinAddress(self, name="btc"):
        a = {"currencyTypeName": name}
        return self.signed_request('POST', '/exchange/fund/controller/website/fundwebsitecontroller/getwithdrawaddress', **a)

    def get_market(self):
        return self.signed_request('POST', '/exchange/config/controller/website/marketcontroller/getByWebId')

    def create_order(self, **payload):
        """create order"""
        return self.signed_request('POST', '/exchange/entrust/controller/website/EntrustController/addEntrust', **payload)

    def buy(self, marketId, price, amount):
        """buy someting"""
        return self.create_order(marketId=marketId, type=1, rangeType=0, price=price, amount=amount)

    def sell(self, marketId, price, amount):
        """buy someting"""
        return self.create_order(marketId=marketId, type=0, rangeType=0, price=price, amount=amount)

    def cancel_order(self, entrustId, marketId):
        payload = {'entrustId': entrustId, 'marketId': marketId}
        return self.signed_request('POST', '/exchange/entrust/controller/website/EntrustController/cancelEntrust', **payload)

    def get_unfinish_order(self, marketId):
        return self.signed_request('GET', '/exchange/entrust/controller/website/EntrustController/getUserEntrustRecordFromCache', marketId = marketId)

    def get_depth(self, marketId):
        a = {'marketId': marketId}
        depth = self.public_request('GET', 'entrusts', **a)
        return depth


class DummyClient(WebSocketClient):
    def __init__(self, url):
        super(DummyClient, self).__init__(url)

        self.zb = ZApi(access_key='', secret_key='')
        self.z = Zbg(key='7fL2TWPgP4a7fL2TWPgP4b', secret='1c9f1ba10fe433953e2c73f44b83b87b')  # 设置自己的api参数
        self.data = {'asks': [], 'bids': ['0.01', '0.01'], 'ts': 0}
        self.ts = 0
        self.adjust_orders = set()

        self.symbol = 'btc_usdt'  # 特殊   btcusdt 329, ethusdt 330, ztusdt 336
        self.sell_cur, self.buy_cur = self.symbol.split('_')
        self.base_price = 8200  # 特殊
        self.zb_ask1 = self.zb_bid1 = self.base_price
        self.rate = 0.01
        self.init_buy_amount = 1100000  # 特殊
        self.init_sell_amount = 133  # 特殊

        self.marketId = '0'
        self.price_decimal = 2  # 特殊
        self.amount_decimal = 4  # 特殊
        self.buy_id = 11  # 特殊,一般为usdt
        self.sell_id = 2  # 特殊
        self.min_amount = 0.0001

        market = self.z.get_market()
        if market[0]:
            for cur in market[1]['datas']:
                if cur['name'] == self.symbol:
                    self.marketId = cur['marketId']
                    self.price_decimal = cur['priceDecimal']
                    self.amount_decimal = cur['amountDecimal']
                    self.buy_id = int(cur['buyerCurrencyId'])
                    self.sell_id = int(cur['sellerCurrencyId'])
                    self.min_amount = float(cur['minAmount'])

        self.price_tick = 10 ** (-self.price_decimal)  # 最小价格变动单位

        self.vol = 0.0001
        self.sign = 5  # 0代表均衡，1代表usdt过多， 2代表usdt过少

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
        if ts > self.ts:
            if self.base_price != 0:
                self.update_trade()
            if ts // 5 > self.ts // 5:
                Thread(target=self.loop).start()

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

        if (self.sign == 1 and ask1 > self.zb_bid1) or (self.sign == 2 and bid1 < self.zb_ask1):
            self.adjust_market(ask1, bid1)
            return

        if ask1 - bid1 < self.price_tick * 1.5:
            print('价差太小\t{}\t{}'.format(ask1, bid1))
            return

        vol = max(round(self.vol * random.randint(50, 150) / 100, self.amount_decimal), self.min_amount)
        price = round((self.zb_ask1 + self.zb_bid1) / 2, self.price_decimal)

        if price < bid1 or price > ask1:
            price = round((ask1 + bid1) / 2, self.price_decimal)
        if self.sign == 1:  # usdt过多
            price = ask1 - self.price_tick
        elif self.sign == 2:  # usdt过少
            price = bid1 + self.price_tick

        self.send_order(price, vol)

    def adjust_market(self, ask1, bid1):
        if self.sign == 1:
            sum_vol = self.min_amount
            for bid in self.data['bids']:
                if float(bid[0]) < self.zb_bid1 - self.price_tick:
                    break
                sum_vol += float(bid[1])
            if sum_vol == self.min_amount:
                sell_order = self.z.sell(self.marketId, self.zb_bid1 - self.price_tick, sum_vol)
                if sell_order[0] and 'datas' in sell_order[1] and sell_order[1]['datas']:
                    self.adjust_orders.add(sell_order[1]['datas']['entrustId'])
                print('压价!\t{}\t{:.2f}\t{}'.format(self.marketId, self.zb_bid1 - self.price_tick, sum_vol))
            elif ask1 - bid1 > self.price_tick * 1.5:
                print('随机下单\t{:.2f}\t{}\tsum:{:.2f}'.format(self.zb_bid1 - self.price_tick, ask1, sum_vol))
                self.random_send_order(ask1, bid1)
            else:
                print('\t价差太小\t{}\t{}'.format(ask1, bid1))

        if self.sign == 2:
            sum_vol = self.min_amount
            for ask in reversed(self.data['asks']):
                if float(ask[0]) > self.zb_ask1 + self.price_tick:
                    break
                sum_vol += float(ask[1])
            if sum_vol < self.vol / 10 or sum_vol == self.min_amount:
                buy_order = self.z.buy(self.marketId, self.zb_ask1 + self.price_tick, sum_vol)
                if buy_order[0] and 'datas' in buy_order[1] and buy_order[1]['datas']:
                    self.adjust_orders.add(buy_order[1]['datas']['entrustId'])
                print('拉价!\t{}\t{:.2f}\tsum:{}'.format(self.marketId, self.zb_ask1 + self.price_tick, sum_vol))
            elif ask1 - bid1 > self.price_tick * 1.5:
                print('随机下单\t{:.2f}\t{}\t{:.2f}'.format(self.zb_ask1 + self.price_tick, bid1, sum_vol))
                self.random_send_order(ask1, bid1)
            else:
                print('\t价差太小\t{}\t{}'.format(ask1, bid1))

    def random_send_order(self, ask1, bid1):
        mult = 10**self.price_decimal
        price = random.randint(int(bid1 * mult) + 1, int(ask1 * mult) - 1) / mult
        print('{}\t{:.2f}\t{}'.format(self.marketId, price, self.min_amount))
        self.send_order(price, self.min_amount)

    def send_order(self, price, vol):
        if self.sign == 1:
            Thread(target=self.async_trade, args=['buy', self.marketId, price, vol]).start()
            self.z.sell(self.marketId, price, vol)
        else:
            Thread(target=self.async_trade, args=['sell', self.marketId, price, vol]).start()
            self.z.buy(self.marketId, price, vol)

        print('{}\t{}\t{}\t{}\t{:.2f}\t{:.4f}'.format(str(datetime.now())[:19], self.data['ts'], self.marketId, self.symbol, price, vol))

    def async_trade(self, side, marketId, price, vol):  # 异步委托
        if side == 'buy':
            self.z.buy(marketId, price, vol)
        elif side == 'sell':
            self.z.sell(marketId, price, vol)

    def loop(self):
        try:
            tick = self.zb.ticker(self.symbol)
            self.base_price = float(tick['ticker']['last'])
            self.zb_ask1 = float(tick['ticker']['sell'])
            self.zb_bid1 = float(tick['ticker']['buy'])
            print('ask:{}\tbid:{}'.format(self.zb_ask1, self.zb_bid1))

            depth = self.z.get_depth(self.marketId)
            if depth[0] and 'datas' in depth[1] and depth[1]['datas']:
                self.data['asks'] = depth[1]['datas']['asks']
                self.data['bids'] = depth[1]['datas']['bids']
        except Exception as e:
            print(e)

        try:
            buy_amount = buy_amount_available = 0
            sell_amount = sell_amount_available = 0
            bln = self.z.get_balance()
            if bln[0] and bln[1]['datas']:
                for b in bln[1]['datas']['list']:
                    if b['currencyTypeId'] == self.buy_id:
                        buy_amount = float(b['amount']) + float(b['freeze'])
                        buy_amount_available = float(b['amount'])
                    elif b['currencyTypeId'] == self.sell_id:
                        sell_amount = float(b['amount']) + float(b['freeze'])
                        sell_amount_available = float(b['amount'])

            if buy_amount == 0 or buy_amount_available == 0 or sell_amount == 0 or sell_amount_available == 0:
                print('获取资金信息失败!')
                self.z.switch_url()
                return

            if buy_amount_available < self.vol * self.base_price * 2 or sell_amount_available < self.vol * 2:
                print('可用不足!\t{}\t{}'.format(buy_amount_available, sell_amount_available))
                os._exit(0)

            dif_buy_amount = buy_amount - self.init_buy_amount
            dif_sell_amount = (sell_amount - self.init_sell_amount) * self.base_price

            if dif_buy_amount - dif_sell_amount > 100:  # usdt过多
                self.sign = 1
            elif dif_buy_amount - dif_sell_amount < -100:
                self.sign = 2
            else:
                self.sign = 0

            print('{}\t{}:{:.2f}\t{}:{:.2f}\tdif:{:.2f}\tsum:{:.2f}\t{}'.format(str(datetime.now())[:19], self.buy_cur,
                                                                                dif_buy_amount,
                                                                                self.sell_cur, dif_sell_amount,
                                                                                dif_buy_amount - dif_sell_amount,
                                                                                dif_buy_amount + dif_sell_amount,
                                                                                self.sign))
        except Exception as e:
            print(e)

        try:
            orders = self.z.get_unfinish_order(self.marketId)  # btc的marketId：329

            if orders[0] and 'datas' in orders[1] and orders[1]['datas']:
                unfinish_orders = set()
                for order in orders[1]['datas']:
                    unfinish_orders.add(order['entrustId'])
                    if (order['entrustId'] not in self.adjust_orders and int(self.data['ts']) - order[
                        'createTime'] // 1000 > 3) or \
                            (order['entrustId'] in self.adjust_orders and int(self.data['ts']) - order[
                                'createTime'] // 1000 > 100):
                        self.z.cancel_order(order['entrustId'], self.marketId)
                self.adjust_orders = self.adjust_orders & unfinish_orders
        except Exception as e:
            print(e)


if __name__ == '__main__':
    while True:
        try:
            ws = DummyClient('wss://kline.zbg.com/websocket')
            if ws.marketId == '0':
                print("can't get marketId!!")
                continue

            ws.connect()
            ws.run_forever()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print('end')
            print(e)
