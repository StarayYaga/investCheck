import requests
import time
from assetTypes.sql_module import main as db

def getBondInfo(data):
    total_coupon=0
    start_price=0
    count=0
    last_price=0
    url=f"https://iss.moex.com/iss/securities/{data['stock']}.json?iss.meta=off"
    url_price=f"https://iss.moex.com/iss/engines/stock/markets/bonds/securities/{data['stock']}.json"
    try:
        req = requests.get(url).json()
    except requests.exceptions.SSLError:
        time.sleep(1000)
        req = requests.get(url).json()
    
    try:
        req_price = requests.get(url_price).json()
    except requests.exceptions.SSLError:
        time.sleep(1000)
        req_price = requests.get(url_price).json()

    for item in data["buy_price"]:
        count += item["count"]
        start_price += item["price"]*item["count"]

    start_price=start_price/count

    last_price=req_price["marketdata"]["data"][-1][11]
    if last_price==None:
        last_price=req_price["securities"]["data"][-1][3]
    last_price = last_price*10

    total_coupon=req_price["securities"]["data"][0][5]
    for info in req["description"]["data"]:
        if info[0]=="COUPONFREQUENCY":
            COUPONFREQUENCY=int(info[2])
    db(data['stock'], last_price)
    return [last_price, total_coupon, start_price, count, COUPONFREQUENCY]

