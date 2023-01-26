import pykis
import yfinance as yf
import pandas as pd
from allocation import baa_aggressive
from config import APP_KEY, APP_SECRET, CANO, ACNT_PRDT_CD
from datetime import datetime

market_codes = {'SPY': "AMS", 'EFA': "AMS", 'EEM': "AMS", 'AGG': "AMS", 'QQQ': "NAS", 'EEM': "AMS", 'EFA': "AMS", 'AGG': "AMS", 'TIP': "AMS", 'DBC': "AMS", 'BIL': "AMS", 'IEF': "NAS", 'TLT': "NAS", 'LQD': "AMS", 'AGG': "AMS", "TSLA": "NAS"}

key_info = {		# KIS Developers 서비스 신청을 통해 발급받은 API key 정보
    "appkey": APP_KEY,
    "appsecret": APP_SECRET
}

account_info = {  # 사용할 계좌 정보
    "account_code": CANO,
    "product_code": ACNT_PRDT_CD
}

# API 객체 생성
domain_info = pykis.DomainInfo(kind="virtual")
api = pykis.Api(domain_info=domain_info, key_info=key_info,
                account_info=account_info)
stocks_os = api.get_os_stock_balance()
print(stocks_os)

asset_usd = 1000
allocation_ratio = baa_aggressive(datetime.now())

# 현재 얼로케이션을 파악
current_allocation = api.get_os_stock_balance().loc[:,['보유수량']]

# 목표 얼로케이션을 파악
allocation_goal = pd.DataFrame(data=
    {"보유수량": [allocation_ratio[stock] * asset_usd // api.get_os_current_price(stock, market_codes[stock]) for stock in allocation_ratio.index], "목표비중": allocation_ratio.values}, index=allocation_ratio.index)

diff = allocation_goal.sub(current_allocation, fill_value=0)
print(diff)

# 매수/매도
for stock in diff.loc[diff.loc[:,"보유수량"] < 0].index:
    api.sell_os_stock(market_codes[stock], stock, int(abs(diff.loc[stock, "보유수량"])), round(api.get_os_current_price(stock, market_codes[stock]) * 0.99, 2))
for stock in diff.loc[diff.loc[:,"보유수량"] > 0].index:
    api.buy_os_stock(market_codes[stock], stock, int(abs(diff.loc[stock, "보유수량"])), round(api.get_os_current_price(stock, market_codes[stock]) * 1.01, 2))

stocks_os = api.get_os_stock_balance()
print(stocks_os)