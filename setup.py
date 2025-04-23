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
        with open(dirStocks, "wt", encoding="utf-8") as file:
            file.write(data)

if __name__ == '__main__':
    main()