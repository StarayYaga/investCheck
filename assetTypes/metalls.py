import requests
import time

def getMetallInfo(data):
    start_price=0
    count=0
    last_price=0

    url=f"https://iss.moex.com/iss/engines/currency/markets/selt/securities/{data["stock"]}.json"
    try:
        req = requests.get(url).json()
    except requests.exceptions.SSLError:
        time.sleep(1000)
        req = requests.get(url).json()
    last_price=req["marketdata"]["data"][0][8]
    if last_price==None:
        last_price=req["securities"]["data"][0][14]

    for item in data["buy_price"]:
        count += item["count"]
        start_price += item["price"]*item["count"]
    
    start_price=start_price/count


    return [last_price, start_price, count]
