# -*- coding: utf-8 -*-
# TODO:域名地址请获取文档的域名来配置
# EXCHANGE_HOST = "https://www.zbg.kim/"
EXCHANGE_HOST = "http://178.zbg.com"
# KLINE_WS_HOST = "ws://192.168.20.13:28080"
# KLINE_HTTP_HOST = KLINE_WS_HOST.replace("wss", "https").replace("ws", "http")
#
# WEBSOCKET_PATH = "/websocket"

# TODO:API_ID和API_SECRET请自行设置

# 线上环境 99090 全部权限
# API_ID = "7yqP4zGmMl67yqPzmm9Ml7"
# API_SECRET = "84a1t071b21c53cc7264a9334129lf0e"
# pass_phrase = '123456'
#
# API_ID = "7yq5QTplOAy7y8SQTelOAz"
# API_SECRET = "as8d7876404y7e53a8b5b8bitf2e7db8"
# pass_phrase = ''

API_ID = "7ypVnkiD6fRuqVtdiD9fQ9"
API_SECRET = "1ba3a4522u1f07f8drc2d2979aye78e5"
pass_phrase = ''



# 测试环境id
# 所有权限
# API_ID = "7vqZcyFnVNA7vqZcyFnVNB"
# API_SECRET = "f7b12b1a5e203655cc671c7001cfa2d3"
# pass_phrase = '123456'

# 有访问口令，1现货资产权限  全部权限
# API_ID = "7vqzikqokaW7vqzi5qokaX"
# API_SECRET = "16f919906161a0e783e82ee8bd0baf95"
# pass_phrase = '234567'  # API访问口令，如果没有设置口令，则请保留空''

# # 现货资产查询3
# API_ID = "7vqZIiRa6vg7vqZIDRa6vh"
# API_SECRET = "49e6c1c96d50849a882ee97dd4563b20"
# pass_phrase = ''

# 第五个-充值
# API_ID = "7vr9dr9dCVXCVXTvM9vTvN"
# API_SECRET = "0716dbf6ac85bc4a1eea0ebf760a03db"
# pass_phrase = '098765'

# 第六个
# API_ID = "7vr9i7vr9pypx5ipypx8ij"
# API_SECRET = "be1dd95b70e8cc8f0f3459a4bc02b99b"
# pass_phrase = '123456'

# 子账号第一个
# API_ID = "7vs7vsFAdFAdXN128XN829"
# API_SECRET = "9671rb0217efb96c702e56e9062bd0eb"
# pass_phrase = ''

# 英文
# API_ID = "7vsdvsd6Gd6GdnsUq7OsUr"
# API_SECRET = "28d89c5e6135a2c59ad6cdc94fua2c8f"
# pass_phrase = '234567'

# 子账号第十个
# API_ID = "7vsJ5vsJ5wcgwcgP4K7o4L"
# API_SECRET = "a738f2139a3989672def2cc265dwfe17"
# pass_phrase = '123456'



# url获取用户信息
API_USER_INFO = "/exchange/user/controller/website/usercontroller/getuserinfo"

# url查询market
API_GET_MARKET_LIST = "/exchange/config/controller/website/marketcontroller/getByWebId"

# url获取资金列表
API_GET_CURRENCY_LIST = "/exchange/config/controller/website/currencycontroller/getCurrencyList"

# url新增委托
API_ADD_ENTRUST = "/exchange/entrust/controller/website/EntrustController/addEntrust"

# url取消委托
API_CANCEL_ENTRUST = "/exchange/entrust/controller/website/EntrustController/cancelEntrust"

# url 根据委托单ID查询委托单信息
API_USER_ENTRUST_BY_ID = "/exchange/entrust/controller/website/EntrustController/getEntrustById"

# url 分页获取用户的委托记录
API_GET_USER_ENTRUST_LIST = "/exchange/entrust/controller/website/EntrustController/getUserEntrustList"

# url从缓存中获取用户还未成交的委托记录，新版，支持分页
API_GET_USER_ENTRUST_FROM_CACHE_WITH_PAGE = "/exchange/entrust/controller/website/EntrustController" \
                                            "/getUserEntrustRecordFromCacheWithPage"

# url从缓存中获取用户还未成交的委托记录(旧版)，无分页，最多获取20条
API_GET_USER_ENTRUST_FROM_CACHE = "/exchange/entrust/controller/website/EntrustController/getUserEntrustRecordFromCache"

# url获取充币地址
API_PAYIN_ADDRESS = "/exchange/fund/controller/website/fundcontroller/getPayinAddress"

# url查询充币记录
API_PAYIN_CION_RECORD = "/exchange/fund/controller/website/fundcontroller/getPayinCoinRecord"

# url查询提币记录
API_PAYOUT_CION_RECORD = "/exchange/fund/controller/website/fundwebsitecontroller/getpayoutcoinrecord"

# url获取用户所有资金信息
API_FUND_FIND_BY_PAGE = "/exchange/fund/controller/website/fundcontroller/findbypage"

# url查询提币地址
API_FUND_WITHDRAW_ADDRESS = "/exchange/fund/controller/website/fundwebsitecontroller/getwithdrawaddress"

# url查询所有市场行情
API_GET_TICKERS = "/api/data/v1/tickers"

# url查询单个市场行情
API_GET_TICKER = "/api/data/v1/ticker"

# url查询k线列表
API_GET_KILNES = "/api/data/v1/klines"

# url查询交易记录
API_GET_TRADES = "/api/data/v1/trades"

# url获取盘口（市场深度）
API_GET_ENTRUSTS = "/api/data/v1/entrusts"
