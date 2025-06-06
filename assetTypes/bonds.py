import requests
import time

def getBondInfo(data):
    total_coupon=0
    start_price=0
    count=0
    last_price=0
    url=f"https://iss.moex.com/iss/engines/stock/markets/bonds/securities/{data["stock"]}.json"
    try:
        req = requests.get(url).json()
    except requests.exceptions.SSLError:
        time.sleep(1000)
        req = requests.get(url).json()

    for item in data["buy_price"]:
        count += item["count"]
        start_price += item["price"]*item["count"]

    start_price=start_price/count

    last_price=req["marketdata"]["data"][-1][11]
    if last_price==None:
        last_price=req["securities"]["data"][-1][3]
    print(last_price)
    last_price = last_price*10

    total_coupon=req["securities"]["data"][0][5]*2
    print([last_price, total_coupon, start_price, count])
    return [last_price, total_coupon, start_price, count]

