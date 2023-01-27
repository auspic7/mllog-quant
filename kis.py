import pykis
from pykis import APIRequestParameter

def get_cash_balance(api):
  """
  구매 가능 현금(달러) 조회
  return: 해당 계좌의 구매 가능한 현금(달러)
  """
  url_path = "/uapi/overseas-stock/v1/trading/inquire-present-balance"
  is_virtual = api.domain.is_virtual()
  tr_id = "VTRP6504R" if is_virtual else "CTRP6504R"

  if api.account is None:
      msg = "계좌가 설정되지 않았습니다. set_account를 통해 계좌 정보를 설정해주세요."
      raise RuntimeError(msg)

  params = {
      "CANO": api.account.account_code,
      "ACNT_PRDT_CD": api.account.product_code,
      "WCRC_FRCR_DVSN_CD": "00",
      "NATN_CD": "840",
      "TR_MKET_CD": "00",
      "INQR_DVSN_CD": "00",
  }

  req = APIRequestParameter(url_path, tr_id, params)
  res = api._send_get_request(req)

  return float(res.outputs[1][0]['frcr_dncl_amt_2']) if len(res.outputs[1]) > 0 else 0

# import pykis
# import yfinance as yf
# import pandas as pd
# from allocation import baa_aggressive
# from config import APP_KEY, APP_SECRET, CANO, ACNT_PRDT_CD, VIRTUAL
# from datetime import datetime

# market_codes = {'SPY': "AMS", 'EFA': "AMS", 'EEM': "AMS", 'AGG': "AMS", 'QQQ': "NAS", 'EEM': "AMS", 'EFA': "AMS", 'AGG': "AMS",
#                 'TIP': "AMS", 'DBC': "AMS", 'BIL': "AMS", 'IEF': "NAS", 'TLT': "NAS", 'LQD': "AMS", 'AGG': "AMS", "TSLA": "NAS"}

# key_info = {		# KIS Developers 서비스 신청을 통해 발급받은 API key 정보
#     "appkey": APP_KEY,
#     "appsecret": APP_SECRET
# }

# account_info = {  # 사용할 계좌 정보
#     "account_code": CANO,
#     "product_code": ACNT_PRDT_CD
# }

# # API 객체 생성
# domain_info = pykis.DomainInfo(kind="real" if not VIRTUAL else "virtual")
# api = pykis.Api(domain_info=domain_info, key_info=key_info,
#                 account_info=account_info)
# stocks_os = api.get_os_stock_balance()

# url_path = "/uapi/overseas-stock/v1/trading/inquire-present-balance"
# is_virtual = api.domain.is_virtual()
# tr_id = "VTRP6504R" if is_virtual else "CTRP6504R"

# if api.account is None:
#     msg = "계좌가 설정되지 않았습니다. set_account를 통해 계좌 정보를 설정해주세요."
#     raise RuntimeError(msg)

# stock_code = ""
# qry_price = 0

# params = {
#     "CANO": api.account.account_code,
#     "ACNT_PRDT_CD": api.account.product_code,
#     "WCRC_FRCR_DVSN_CD": "00",
#     "NATN_CD": "840",
#     "TR_MKET_CD": "00",
#     "INQR_DVSN_CD": "00",
# }

# req = APIRequestParameter(url_path, tr_id, params)
# res = api._send_get_request(req)
# print(res.outputs[1][0]['frcr_dncl_amt_2'])