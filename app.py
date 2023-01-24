import requests
import json
from config import APP_KEY, APP_SECRET, URL_BASE

headers = {"content-type":"application/json"}
body = {"grant_type":"client_credentials",
        "appkey":APP_KEY, 
        "appsecret":APP_SECRET}

PATH = "oauth2/token"
URL = f"{URL_BASE}/{PATH}"
print(URL)

res = requests.post(URL, headers=headers, data=json.dumps(body))
print(res.text)