import yfinance as yf
import pandas as pd
# from datetime import datetime

def baa_aggressive(date=pd.Timestamp.now()):
	date = pd.Timestamp(date, tz='America/New_York')

	# BAA-Aggressive 구현
	canary = ["SPY", "EFA", "EEM", "AGG"]
	offensive = ["QQQ", "EEM", "EFA", "AGG"]
	defensive = ["TIP", "DBC", "BIL", "IEF", "TLT", "LQD", "AGG"]
	tickers = canary + offensive + defensive
	datas = yf.download(tickers, start=date-pd.DateOffset(months=14), interval="1mo", end=date, group_by="ticker")
	# print(datas)

	# Momentum Score, 12MA Momentum 계산
	'''
	Calculate the “13612W” momentum of each asset. This is a multi-timeframe measure of momentum, calculated as follows:
	(12 * (p0 / p1 – 1)) + (4 * (p0 / p3 – 1)) + (2 * (p0 / p6 – 1)) + (p0 / p12 – 1)
	Where p0 = the price at today’s close, p1 = the price at the close of the previous month, etc.
	'''
	for ticker in tickers:
		month_offsets = [1, 3, 6, 12]
		month_weights = [12, 4, 2, 1]
		datas.loc[:, (ticker, "momentum_score")] = \
			sum([datas[ticker]["Adj Close"].pct_change(month_offset) * month_weight for month_offset, month_weight in zip(month_offsets, month_weights)])
		datas.loc[:, (ticker, "relative_momentum")] =\
			datas[ticker]["Adj Close"][-1] / datas[ticker]["Adj Close"].mean()

	momenta = datas.tail(1).loc[:, (tickers, ["Adj Close", "momentum_score",
		"relative_momentum"])].stack().transpose() 
	print(momenta)
	momenta = momenta.droplevel(level=0, axis=1)

	# Canary asset의 momentum score가 모두 양수이면 aggressive, 아니면 defensive
	aggresive = (momenta.loc[canary]["momentum_score"] > 0).all()
	if aggresive:
		'''
		If selecting from the offensive universe, select the 6 assets (balanced version) or 1 asset (aggressive version) with the highest relative momentum.
		'''
		allocation = pd.Series(index=[momenta.loc[offensive]['relative_momentum'].idxmax()], data=[1])
	else:
		'''
		If selecting from the defensive universe, select the 3 assets with the highest relative momentum. 
		If the relative momentum of the asset is less than that of US T-Bills (represented by ETF: BIL), instead place that portion of the portfolio in cash.
		'''
		top_defensives = momenta.loc[defensive].sort_values('relative_momentum', ascending=False).head(3)
		asset_to_buy = top_defensives[top_defensives['relative_momentum'] > momenta.loc['BIL', 'relative_momentum']].index
		num_asset_to_buy = len(asset_to_buy)
		if num_asset_to_buy == 0:
			allocation = pd.Series(dtype="float64")
		else:
			allocation = pd.Series(index=asset_to_buy, data=[1/3]*asset_to_buy.size)

	return allocation