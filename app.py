import pykis
import yfinance as yf
import pandas as pd
from allocation import baa_aggressive
from config import APP_KEY, APP_SECRET, CANO, ACNT_PRDT_CD, VIRTUAL
from datetime import datetime
from kis import get_cash_balance

market_codes = {'SPY': "AMS", 'EFA': "AMS", 'EEM': "AMS", 'AGG': "AMS", 'QQQ': "NAS", 'EEM': "AMS", 'EFA': "AMS", 'AGG': "AMS", 'TIP': "AMS", 'DBC': "AMS", 'BIL': "AMS", 'IEF': "NAS", 'TLT': "NAS", 'LQD': "AMS", 'AGG': "AMS", "TSLA": "NAS", "QRFT": "AMS"}

key_info = {		# KIS Developers 서비스 신청을 통해 발급받은 API key 정보
    "appkey": APP_KEY,
    "appsecret": APP_SECRET
}

account_info = {  # 사용할 계좌 정보
    "account_code": CANO,
    "product_code": ACNT_PRDT_CD
}

# API 객체 생성
domain_info = pykis.DomainInfo(kind="virtual" if VIRTUAL else "real")
api = pykis.Api(domain_info=domain_info, key_info=key_info,
                account_info=account_info)
stocks_os = api.get_os_stock_balance()

# 현재 총 자산을 파악
stock_usd = 0
if len(stocks_os) > 0:
    stocks_os.loc[:, "총액"] = stocks_os.loc[:, "현재가"] * stocks_os.loc[:, "보유수량"]
    stock_usd = stocks_os.loc[:, "총액"].sum()
cash_usd = get_cash_balance(api)
asset_usd = stock_usd + cash_usd
print("현재 총 자산: ", asset_usd)

# 자산배분 비율을 파악
allocation_ratio = baa_aggressive(datetime.now())

# 현재 얼로케이션을 파악
if len(stocks_os) > 0:
    current_allocation = stocks_os.loc[:,['보유수량']]
else:
    current_allocation = pd.DataFrame(columns=["보유수량"])

# 목표 얼로케이션을 파악
allocation_goal = pd.DataFrame(data=
    {"보유수량": [allocation_ratio[stock] * asset_usd // api.get_os_current_price(stock, market_codes[stock]) for stock in allocation_ratio.index], "목표비중": allocation_ratio.values}, index=allocation_ratio.index)

diff = allocation_goal.sub(current_allocation, fill_value=0).rename(columns={"보유수량": "매매계획수량"})
print(diff)

# 매수/매도
for stock in diff.loc[diff.loc[:,"매매계획수량"] < 0].index:
    api.sell_os_stock(market_codes[stock], stock, int(abs(diff.loc[stock, "매매계획수량"])), round(api.get_os_current_price(stock, market_codes[stock]) * 0.99, 2))
for stock in diff.loc[diff.loc[:,"매매계획수량"] > 0].index:
    api.buy_os_stock(market_codes[stock], stock, int(abs(diff.loc[stock, "매매계획수량"])), round(api.get_os_current_price(stock, market_codes[stock]) * 1.01, 2))

stocks_os = api.get_os_stock_balance()
print(stocks_os)