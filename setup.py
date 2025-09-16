from config import dirStocks
import os


def main():
    data = '''{
    "tickets":[],
    "ticketsCrypto":[],
    "Stocks": [],
    "Crypto": [],
    "Currency": [{"RUB": "0"}, {"USDT": 0}],
    "Metals":[],
    "Bonds":[]
}'''
    if os.path.exists(dirStocks)==False:
        if "data" not in  os.listdir(path="."):
            os.mkdir("data")
        with open(dirStocks, "wt", encoding="utf-8") as file:
            file.write(data)

if __name__ == '__main__':
    main()