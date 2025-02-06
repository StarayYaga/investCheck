import json

# {"name":"", "stock":"", "count":"", "buy_price":[{"count":"", "price":""}]}

class rwControler:
    def __init__(self, path):
        self.path = path

    def readStocks(self):
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)
    def writeStocks(self,data):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file ,indent=4, ensure_ascii=False)