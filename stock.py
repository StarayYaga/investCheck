from rwControl import rwControler
import requests
import datetime
from config import dirStocks
from assetTypes.stocks import getStockInfo
from assetTypes.metalls import getMetallInfo
from assetTypes.bonds import getBondInfo



def getNameFromMOEX(shortName):
    url=f"https://iss.moex.com/iss/securities/{shortName}.json"
    req=requests.get(url).json()
    return req["description"]["data"][2][2]


def customRound(data):
    return float("{:.2f}".format(float(data)))


def totalCapital():
    file = rwControler(dirStocks)
    year = int(str(datetime.date.today()).split('-')[0])
    text=f"Состав портфеля\n\n"
    price_of_capital=0
    price_of_capital_now=0
    dividends=0
    for asssetType in ("Stocks", "Metals", "Bonds"):
        stocks = file.readStocks()[asssetType]
        if asssetType=="Stocks":
            text+=f"Акции:\n"
            for asset in stocks:
                last_price, total_divs, start_price, count=getStockInfo(asset, year)
                price_of_capital+=start_price*count
                price_of_capital_now+=last_price*count
                dividends+=total_divs*count
                profit_in_procent=customRound(((last_price-start_price)/start_price)*100)
                text+=f'{asset["name"]} : {asset["stock"]}   Профит: {profit_in_procent}%\nЦена: {last_price}   Кол-во: {count}\n======================\n\n'
        if asssetType=="Metals":
            text+=f"Драгоценные металлы:\n"
            for asset in stocks:
                last_price, start_price, count=getMetallInfo(asset)
                price_of_capital+=start_price*count
                price_of_capital_now+=last_price*count
                profit_in_procent=customRound(((last_price-start_price)/start_price)*100)
                text+=f'{asset["name"]} : {asset["stock"]}   Профит: {profit_in_procent}%\nЦена: {last_price}   Кол-во: {count}\n======================\n\n'
        if asssetType=="Bonds":
            text+=f"Облигации:\n"
            for asset in stocks:
                last_price, total_coupon, start_price, count=getBondInfo(asset)
                price_of_capital+=start_price*count
                price_of_capital_now+=last_price*count
                dividends+=total_coupon*count
                profit_in_procent=customRound(((last_price-start_price)/start_price)*100)
                text+=f'{asset["name"]} : {asset["stock"]}   Профит: {profit_in_procent}%\nЦена: {last_price}   Кол-во: {count}\n======================\n\n'
    

    try:
        procent_briefcase=((price_of_capital_now-price_of_capital)/price_of_capital)*100
    except ZeroDivisionError:
        procent_briefcase=0
    try:
        procent_div=(dividends/price_of_capital_now*100)
    except ZeroDivisionError:
        procent_div=0
    text += f"\n\nЦена портфеля сейчас: {customRound(price_of_capital_now)}  {customRound(procent_briefcase)}%\nЦена покупки портфеля: {customRound(price_of_capital)}"
    text += f"\nДивиденды и купоны за {year} год: {customRound(dividends)}р {customRound(procent_div)}%"
    text += f"\nСвободные средства: {customRound(file.readStocks()['Currency'][0]['RUB'])}"

    return text

if __name__ == "__main__":
    print(totalCapital())
