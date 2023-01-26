import pykis
import yfinance as yf
from config import APP_KEY, APP_SECRET, CANO, ACNT_PRDT_CD

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

# BAA-Aggressive 구현
canary = ["SPY", "EFA", "EEM", "AGG"]
offensive = ["QQQ", "EEM", "EFA", "AGG"]
defensive = ["TIP", "DBC", "BIL", "IEF", "TLT", "LQD", "AGG"]
tickers = canary + offensive + defensive

datas = yf.download(tickers, period="13mo", group_by="ticker")

# Momentum Score, 12MA Momentum 계산
'''
Calculate the “13612W” momentum of each asset. This is a multi-timeframe measure of momentum, calculated as follows:
(12 * (p0 / p1 – 1)) + (4 * (p0 / p3 – 1)) + (2 * (p0 / p6 – 1)) + (p0 / p12 – 1)
Where p0 = the price at today’s close, p1 = the price at the close of the previous month, etc.
'''
for ticker in tickers:
    datas.loc[:, (ticker, "momentum_score")] = \
        datas[ticker]["Adj Close"].pct_change(21) * 12 +\
        datas[ticker]["Adj Close"].pct_change(63) * 4 +\
        datas[ticker]["Adj Close"].pct_change(126) * 2 +\
        datas[ticker]["Adj Close"].pct_change(252)
    datas.loc[:, (ticker, "relative_momentum")] =\
        datas[ticker]["Adj Close"][-1] / datas[ticker]["Adj Close"].mean()

momenta = datas.tail(1).loc[:, (tickers, ["Adj Close", "momentum_score",
      "relative_momentum"])].stack().transpose() 
print(momenta)
momenta = momenta.droplevel(level=0, axis=1)

# If all canary assets have positive momentum, select from the offensive universe, otherwise select from the defensive universe.
if (momenta.loc[canary]["momentum_score"] > 0).all():
    print(f"Buy an aggressive: {momenta.loc[offensive]['relative_momentum'].idxmax()}")
else:
    '''
    If selecting from the defensive universe, select the 3 assets with the highest relative momentum. 
    If the relative momentum of the asset is less than that of US T-Bills (represented by ETF: BIL), instead place that portion of the portfolio in cash.
    '''
    top_defensives = momenta.loc[defensive].sort_values('relative_momentum', ascending=False).head(3)
    print(f"Buy defensive(s): {top_defensives[top_defensives['relative_momentum'] > momenta.loc['BIL', 'relative_momentum']].index.tolist()}")

