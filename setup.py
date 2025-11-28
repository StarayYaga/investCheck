from config import dirStocks, dirDB
import os


def main():
    data = '''{
    "tickets":[],
    "ticketsCrypto":[],
    "Stocks": [],
    "Crypto": [],
    "Currency": [{"RUB": "0"}, {"USDT": 0}],
    "Metals":[],
    "Bonds":[],
    "replenishments": 0.0
}'''
    if os.path.exists(dirStocks)==False:
        if "data" not in  os.listdir(path="."):
            os.mkdir("data")
        with open(dirStocks, "wt", encoding="utf-8") as file:
            file.write(data)
    if os.path.exists(dirDB)==False:
        with open(dirDB, "wt", encoding="utf-8") as file:
            file.write(data)

if __name__ == '__main__':
    main()