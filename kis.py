import requests, json
from config import URL_BASE, APP_KEY, APP_SECRET

def hashkey(datas):
  PATH = "uapi/hashkey"
  URL = f"{URL_BASE}/{PATH}"
  headers = {
    'content-Type' : 'application/json',
    'appKey' : APP_KEY,
    'appSecret' : APP_SECRET,
    }
  res = requests.post(URL, headers=headers, data=json.dumps(datas))
  hashkey = res.json()["HASH"]

  return hashkey