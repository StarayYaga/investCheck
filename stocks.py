from rwControl import rwControler
import requests
import datetime
import time
from config import dirStocks

def getNameFromMOEX(shortName):
    url=f"https://iss.moex.com/iss/securities/{shortName}.json"
    req=requests.get(url).json()
    return req["description"]["data"][2][2]

def getStockPrice(shortName):
    url = f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{shortName}.json"
    try:
        req = requests.get(url).json()
    except requests.exceptions.SSLError:
        time.sleep(1000)
        req = requests.get(url).json()
    data=req["marketdata"]["data"][-1][12]
    if data==None:
        data=req["securities"]["data"][-1][3]
    return float(data)

def getDividendsPrice(shortName):
    url = f"https://iss.moex.com/iss/securities/{shortName}/dividends.json"
    req = requests.get(url).json()
    data=req["dividends"]["data"]
    if data==[]:
        data=False
    return data

def customRound(data):
    return float("{:.2f}".format(data))


def totalCapital():
    file = rwControler(dirStocks)
    year = int(str(datetime.date.today()).split('-')[0]) # вычисление текущего года
    data = []
    text=f"Состав портфеля\n\n"
    stocks = file.readStocks()["Stocks"]
    total_price=0 #итоговыя цена портфеля без учета профита
    price_now_total=0
    divs=0

    for stock in stocks:
        total_divs=0
        stock_prices_total=0 # итоговая средняя цена всех акций компании в портфейле
        stock_count_total=0 # итоговое 
        total_price_now=0
        price_now=getStockPrice(stock['stock']) #цена акций сейчас
        prices=stock["buy_price"] #цены и количество акций при покупке
        all_divs=getDividendsPrice(stock["stock"])

        for item in prices:
            stock_total = item["count"]
            stock_price = item["price"]*stock_total
            stock_prices_total += stock_price
            stock_count_total += stock_total

        if all_divs!=False:  # вычисление дивидендов на общие колличество акций опр. компании
            for div in all_divs:
                date=int(str(datetime.date(year, 1, 1)-datetime.date.fromisoformat(div[2])).split(' ')[0])
                if date <0 :
                    total_divs+=div[3]*stock_count_total

        total_price += stock_prices_total
        profit = customRound((stock_count_total*price_now)-stock_prices_total)
        profit_in_procent=customRound((profit/stock_prices_total)*100)
        total_price_now+=stock_count_total*price_now
        price_now_total+=total_price_now
        text+=f'{stock["name"]} : {stock["stock"]}   Профит: {profit_in_procent}%\nЦена: {price_now}   Кол-во: {stock_count_total}\n======================\n\n'
        divs+=total_divs

        data.append({
            "name":stock["name"],
            "shortName":stock["stock"],
            "count": stock_count_total,
            "price_now": price_now,
            "procent": profit_in_procent,
            "profit": profit,
            "total_price_stock": stock_prices_total,
            "total_price_now": total_price_now,
            "total_divs": customRound(total_divs),
        })
    
    try:
        procent_briefcase=((total_price_now-stock_prices_total)/stock_prices_total)*100
    except ZeroDivisionError:
        procent_briefcase=0
    try:
        procent_div=(total_divs/total_price_now*100)
    except ZeroDivisionError:
        procent_div=0
    text += f"\n\nЦена портфеля сейчас: {customRound(total_price_now)}  {customRound(procent_briefcase)}%\nЦена покупки портфеля: {customRound(stock_prices_total)}"
    text += f"\nДивиденды за {year} год: {customRound(year)}р {customRound(procent_div)}%"
    text += f"\nСвободные средства: {customRound(file.readStocks()["Currency"][0]["RUB"])}"

    return text

if __name__ == "__main__":
    print(totalCapital())
