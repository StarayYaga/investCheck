from rwControl import rwControler
import ccxt
from config import dirStocks


def customRound(data):
    return float("{:.2f}".format(data))

def formatZero(data: float):
    return '{:.8f}'.format(data).rstrip('.0')

def getNameFromKucoin(shortName):
    name = shortName.split('/')[0]
    data=ccxt.kucoin().fetch_currencies()
    for currrency in data:
        if currrency==name:
            return data[currrency]["info"]["fullName"]


def cryptoCurrencyInfo():
    file = rwControler(dirStocks)
    data = []
    total_price=0 #итоговыя цена портфеля без учета профита
    price_now_total=0
    text=f"Состав криптовалютного портфеля\n\n"
    currencyes = file.readStocks()["Crypto"]
    for currency in currencyes:
        total_currency_count=0
        total_currency_price=0
        name=currency["stock"]
        price_now=ccxt.kucoin().fetch_ticker(name)['last']
        prices=currency["buy_price"]
        for price in prices:
            currency_count = price["count"]
            currency_price = price["price"]*currency_count
            total_currency_count+=currency_count
            total_currency_price+=currency_price
        total_price+=total_currency_price
        total_price_now=total_currency_count*price_now
        price_now_total+=total_price_now
        profit=customRound((total_price_now)-total_currency_price)
        profit_in_procent=customRound((profit/total_currency_price)*100)
        total_currency_count=formatZero(total_currency_count)
        total_currency_price=formatZero(total_currency_price)
        text+=f'{currency["name"]} : {currency["stock"]}   Профит: {profit_in_procent}%\nЦена: {price_now}   Кол-во: {total_currency_count}\n======================\n\n'
        
        data.append({
            "name":currency["name"],
            "shortName":currency["stock"],
            "count": total_currency_count,
            "price_now": price_now,
            "procent": profit_in_procent,
            "profit": profit,
            "total_price_stock": total_currency_price,
            "total_price_now": total_price_now,
        })
    try:
        procent_briefcase=((total_price_now-total_price)/total_price)*100
    except ZeroDivisionError:
        procent_briefcase=0
    text += f"\n\nЦена портфеля сейчас: {customRound(total_price_now)}  {customRound(procent_briefcase)}%\nЦена покупки портфеля: {customRound(total_price)}"
    text += f"\nСвободные средства: {customRound(file.readStocks()["Currency"][1]["USDT"])}"

    return text

if __name__ == "__main__":
    print(cryptoCurrencyInfo())
    # print(getNameFromKucoin("ETH"))