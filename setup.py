from config import dirStocks
import os
import json


def main():
    data = '''{
    "tickets":[""],
    "Stocks": [],
    "Crypto": [{"USDT": 0}],
    "Currency": [{"RUB": "0"}]
}'''
    if os.path.exists(dirStocks)==False:
        with open(dirStocks, "wt", encoding="utf-8") as file:
            file.write(data)

if __name__ == '__main__':
    main()