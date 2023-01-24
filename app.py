import requests
import json
from config import ACNT_PRDT_CD, APP_KEY, APP_SECRET, CANO, URL_BASE
from kis import hashkey

# 토큰 
headers = {"content-type":"application/json"}
body = {"grant_type":"client_credentials",
        "appkey":APP_KEY, 
        "appsecret":APP_SECRET}

PATH = "oauth2/tokenP"
URL = f"{URL_BASE}/{PATH}"

res = requests.post(URL, headers=headers, data=json.dumps(body))
print(res.text)
ACCESS_TOKEN = res.json()["access_token"]


# 주문
PATH = "uapi/overseas-stock/v1/trading/order"
URL = f"{URL_BASE}/{PATH}"
print(URL)
data = {
    "CANO": CANO,
    "ACNT_PRDT_CD": ACNT_PRDT_CD,
    "OVRS_EXCG_CD": "NASD",
    "PDNO": "GOOGL",
    "OVRS_ORD_UNPR": "0",
    "ORD_DVSN": "00",
    "ORD_QTY": "1",



    "CTAC_TLNO": "",
    "ORD_SVR_DVSN_CD": "0",
    "MGCO_APTM_ODNO": "",
}
headers = {"Content-Type":"application/json", 
           "authorization":f"Bearer {ACCESS_TOKEN}",
           "appKey":APP_KEY,
           "appSecret":APP_SECRET,
           "tr_id":"VTTT1002U",
           "custtype":"P",
           "hashkey" : hashkey(data)}

res = requests.post(URL, headers=headers, data=json.dumps(data))
print(res.json())
