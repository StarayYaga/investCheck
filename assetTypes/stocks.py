import requests
import time
import datetime
from assetTypes.sql_module import main as db 

def getStockInfo(data,year):
    total_divs=0
    start_price=0
    count=0
    last_price=0
    stock_url=f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{data['stock']}.json"
    dividend_url = f"https://iss.moex.com/iss/securities/{data['stock']}/dividends.json"

    try:
        stock_req = requests.get(stock_url).json()
    except requests.exceptions.SSLError:
        time.sleep(1000)
        stock_req = requests.get(stock_url).json()

    dividend_req = requests.get(dividend_url).json()
    dividends=dividend_req["dividends"]["data"]
    
    for item in data["buy_price"]:
        count += item["count"]
        start_price += item["price"]*item["count"]

    start_price=start_price/count

    if dividends!=[]:
        for div in dividends:
            date=int(str(datetime.date(year, 1, 1)-datetime.date.fromisoformat(div[2])).split(' ')[0])
            if date <0 :
                total_divs+=div[3]

    

    last_price=stock_req["marketdata"]["data"][-1][12]
    if last_price==None:
        last_price=stock_req["securities"]["data"][-1][3]

    db(data['stock'], last_price)
    return [last_price, total_divs, start_price, count]
