# cookies.py
# управляет всеми куками, возвращает cookie
# made by soylir

import requests
r = requests.get("https://tradeback.io/")

__session = r.cookies.get_dict()
__steam = {
  "session": '',
  "remember_web_": ''
}
__selenium = {
  'name': '',
  'value': ''
}

__cstrade = {
  "PHPSESSID": ''
}

def get_cookies():
    return __session, __steam, __cstrade, __selenium
