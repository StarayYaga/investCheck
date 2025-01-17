import requests
import json
import schedule
import time
import datetime
from config import channelId, botToken, ownerId, dirStocks
from setup import main as checkFileExist


# {"name":"", "stock":"", "count":"", "buy_price":[{"count":"", "price":""}]}

class rwControl:
    def __init__(self, path):
        self.path = path

    def readStocks(self):
        with open(self.path, encoding="utf-8") as file:
            return json.load(file,)
    def writeStocks(self,data):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file ,indent=4, ensure_ascii=False)

def getNameFromMOEX(shortName):
    url=f"https://iss.moex.com/iss/securities/{shortName}.json"
    req=requests.get(url).json()
    return req["description"]["data"][2][2]

def getStockPrice(shortName):
    url = f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{shortName}.json"
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

def getCryptoPrice():
    url = f"https://min-api.cryptocompare.com/data/pricemulti?fsyms=ETH,BTC,XMR,RUB&tsyms=USD&api_key=INSERT-cf0ef631d331819030a8ee6cfed755341ee2ee5f5310db8ca3fbe634db7620a9"
    req = requests.get(url).json()
    return req

file = rwControl(dirStocks)


def send_text(text, chat, token):
    requests.post(
        url=f"https://api.telegram.org/bot{token}/sendMessage",
        data = {
            "chat_id":chat,
            "text":text
        })

def cryptocurrency(file):
    data = getCryptoPrice()
    stocks = file.readStocks()["Crypto"]
    return f"""USDT: ${stocks[0]["USDT"]} - ₽{round(stocks[0]["USDT"]/float(data["RUB"]["USD"]),2)}
======================

USDT/RUB - ₽{round(1/float(data["RUB"]["USD"]), 2)}
BTC/USDT - ${data["BTC"]["USD"]}
ETH/USDT - ${data["ETH"]["USD"]}
XMR/USDT - ${data["XMR"]["USD"]}
"""

def customRound(data):
    return float("{:.2f}".format(data))

def totalCapital(file, year):
    data = []
    text=f""
    stocks = file.readStocks()["Stocks"]
    currency = 0
    total_price=currency #итоговыя цена портфеля без учета профита
    price_now_total=currency
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
            stock_total = float(item["count"])
            stock_price = float(item["price"])*stock_total
            stock_prices_total += stock_price
            stock_count_total += stock_total

        if all_divs!=False:  # вычисление дивидендов на общие колличество акций опр. компании
            for div in all_divs:
                date=int(str(datetime.date(year, 1, 1)-datetime.date.fromisoformat(div[2])).split(' ')[0])
                if date <0 :
                    total_divs+=div[3]*stock_count_total

        total_price += stock_prices_total
        profit = (stock_count_total*price_now)-stock_prices_total
        profit_in_procent=(profit/stock_prices_total)*100
        total_price_now+=stock_count_total*price_now
        price_now_total+=total_price_now
        text+=f'{stock["name"]} : {stock["stock"]}   Профит: {customRound(profit_in_procent)}%\nЦена: {price_now}   Кол-во: {stock_count_total}\n======================\n\n'
        divs+=total_divs

        data.append({
            "name":stock["name"],
            "shortName":stock["stock"],
            "count": stock_count_total,
            "price_now": price_now,
            "procent": customRound(profit_in_procent,),
            "profit": customRound(profit),
            "total_price_stock": stock_prices_total,
            "total_price_now": total_price_now,
            "total_divs": customRound(total_divs),
        })
    
    return [data, price_now_total, total_price, divs*87/100, text, float(file.readStocks()["Currency"][0]["RUB"])]


def main():
    year = int(str(datetime.date.today()).split('-')[0]) # вычисление текущего года
    data = totalCapital(file, year)
    text ='Состав портфеля\n\n'
    text += data[4] + cryptocurrency(file)
    text += f"\n\nЦена портфеля сейчас: {customRound(data[1])}  {customRound(((data[1]-data[2])/data[2])*100)}%\nЦена покупки портфеля: {customRound(data[2])}"
    text += f"\nДивиденды за {year} год: {customRound(data[3])}р {customRound(((data[3])/data[1]*100))}%"
    text += f"\nСвободные средства: {customRound(data[-1])}"
    send_text(text, ownerId, botToken)
    send_text(text, channelId, botToken)



def getStock():
    year = int(str(datetime.date.today()).split('-')[0]) # вычисление текущего года
    data = totalCapital(file, year)
    text ='Состав портфеля\n\n'
    text += data[4] + cryptocurrency(file)
    text += f"\n\nЦена портфеля сейчас: {customRound(data[1])}  {customRound(((data[1]-data[2])/data[2])*100)}%\nЦена покупки портфеля: {customRound(data[2])}"
    text += f"\nДивиденды за {year} год: {customRound(data[3])}р {customRound(((data[3])/data[1]*100))}%"
    text += f"\nСвободные средства: {customRound(data[-1])}"
    return text

if __name__ == '__main__':
    checkFileExist()
    main()
    print("start")

    schedule.every().day.at("08:00").do(main)
    schedule.every().day.at("12:00").do(main)
    schedule.every().day.at("16:00").do(main)
    schedule.every().day.at("20:00").do(main)
    schedule.every().day.at("00:00").do(main)

    print("set time")
    while True:
        schedule.run_pending()
        time.sleep(1)
