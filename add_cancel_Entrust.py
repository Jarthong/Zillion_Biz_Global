import requests, hashlib
import time, datetime, random
import json
import jarthong_zbg_GetMarketId

# 线上环境
# base_url = 'https://www.zbg.com'
# key = '7hviVA7J86uJVhvikFl6ZB'  # 9909
# secret = '57abc27e60a0c0e5abd098af6d1e148c'

# 测试环境
# base_url = 'http://179.boss.zbg.com'
base_url = 'http://178.zbg.com/'

key1 = '7hxEPeq7hx6PPE6V8V6Per'  # 9909
secret1 = 'df8f4da3a36b9djcee48c5747a2160b1'

key2 = '7ijNRjNRsNjk7iNsnssnHl'  # 136@qq.com
secret2 = '6a5349cddedd6c7f26653b94256f8c1a'

key3 = '7ijdEhZfdtjfEhw7ijNbZx'  # 8800@qq.com
secret3 = '81369cc5b7e18d37dford06c2c2d5a0b'

key4 = '7ijNgRijNgR0Z0Z8UK78UL'  # 7700@qq.com
secret4 = '06ac021e0b24d7620c8c380b20cf1c72'

key5 = '7ijNrVU5tjNcpJorcpJoVV'  # 6600@qq.com
secret5 = '3b801a856f1190e408296d9ace3f5f99'

key6 = '7ijNxZI7ijNwCwCNjNjxZJ'  # 3300@qq.com
secret6 = '3495a5a4dc884cf3f257b58fde031b98'

key7 = '7ijO0majO0makkkEK7ikEL'  # 2200@qq.com
secret7 = '33abaee49430f86662e7529ea01214c8'

key8 = '7ijO7P67ijOfKHD7PfKHD7'  # 1100@qq.com
secret8 = '66d4d8d4fb8e31ed17e77b3f6c7d05ae'

key9 = '7ijOR0q67P67ijOR0q67P7'  # 4400@qq.com
secret9 = '7d4a0e3cb517f728fa09f6dba4ca3966'

key10 = '7ijOX4YTYpc7ijOX4YTYpd'  # 15822334456
secret10 = '2f49d6edd2a62f70d065bdbab6f462d8'

key11 = '7ijObAWvOUa7ijObAWvOUb'  # 15822334457
secret11 = 'b0aeb278eb6192d4a2ef997dc81d05c7'

# 合盘测试环境
# base_url = 'http://zbgtest.bwpool.net'
# key = '7iWSsw1OCY47iWSsw1OCY5'  # 990908814@qq.com
# secret = '90c80d3688fd87023f9a1d8235b53443'

# 合盘测试环境
# base_url = 'http://zbgtest.bwpool.net'
# key = '7iWSoAcMArI7iWSoAcMArJ'  # 4400@qq.com
# secret = '7f59e03ccf85cc465eb034d5dd8db4e0'

# 新增委托单接口
API_ADD_ENTRUST = '/exchange/entrust/controller/website/EntrustController/addEntrust'
# 设置要下单的市场
# market_name = 'zb_qc'
# market_id = jarthong_zbg_GetMarketId.getID(market_name)
market_id = '100'   # 交易市场id号
market_id2 = '98'
market_id_list = [market_id, market_id2]
num = 2          # 要撮合的数量
min_amount = 1    # 随机最小购买数量
max_amount = 5  # 随机最大购买数量
min_price = 1     # 随机最小下单价格
max_price = 3    # 随机最大下单价格
# price = str(price_num)

# 撤单接口
API_cancel_ENTRUST = '/exchange/entrust/controller/website/EntrustController/cancelEntrust'


while True:
    for i in range(0, num):
        timestamp = str(int(time.time() * 1000))
        amount_float = random.uniform(min_amount, max_amount)  # 随机生成要下单的浮点数量
        amount = round(amount_float, 2)  # 生成要下单的两位小数精度的数量
        print('随机生成要下单的数量：', amount)
        price_float = random.uniform(min_price, max_price)     # 随机生成要下单的浮点价格
        price = round(price_float, 2)  # 生成要下单的两位小数点精度的价格
        print('随机生成要下单的价格：', price)
        market_id_random = random.choice(market_id_list)
        print('下单的市场id号是：', market_id_random)
        print('-'*100)

        for j in range(0, 2):
            if j == 0:
                entrust_type = 0  # 要下单的类型，0 卖出 1 购买
                params = {'marketId': market_id_random, 'amount': amount, 'price': price, 'rangeType': 0, 'type': entrust_type}
                param = json.dumps(params)
                # 随机生成key和secret
                number = random.randint(1, 11)
                key = eval('key' + str(number))
                secret = eval('secret' + str(number))
                print('下卖单的key值是', key)
                print('下卖单的keysecret值是', secret)
                sig_str = key + timestamp + param + secret
                signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
                header = {'Apiid': key, 'Timestamp': timestamp, 'Sign': signature}
                r_sell = requests.request(method='POST', url=base_url + API_ADD_ENTRUST, headers=header, json=params, verify=False)
                time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # 当前时间
                result_sell = r_sell.json()
                print('买单时间：', time_now, '', result_sell)
            else:
                entrust_type = 1  # 要下单的类型，0 卖出 1 购买
                params = {'marketId': market_id_random, 'amount': amount, 'price': price, 'rangeType': 0, 'type': entrust_type}
                param = json.dumps(params)
                # 随机生成key和secret
                number = random.randint(1, 11)
                key = eval('key' + str(number))
                secret = eval('secret' + str(number))
                print('下买单的key值是', key)
                print('下买单的keysecret值是', secret)
                sig_str = key + timestamp + param + secret
                signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()
                header = {'Apiid': key, 'Timestamp': timestamp, 'Sign': signature}
                r_buy = requests.request(method='POST', url=base_url + API_ADD_ENTRUST, headers=header, json=params, verify=False)
                time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # 当前时间
                result_buy = r_buy.json()
                print('卖单时间：', time_now, '', result_buy)
                time.sleep(0.18)





