import telebot
from telebot import types
from stocks import getNameFromMOEX, totalCapital
from cryptoCurrency import getNameFromKucoin, cryptoCurrencyInfo, formatZero
from rwControl import rwControler
from valid import Valid
from config import botToken, dirStocks
from setup import main as checkFileExist


bot = telebot.TeleBot(botToken)
markup_inline = types.ReplyKeyboardMarkup(resize_keyboard=True)
valid = Valid(bot=bot)

buy = types.KeyboardButton(text='Покупка')
helpBtn = types.KeyboardButton(text='/help')
sell = types.KeyboardButton(text='Продажа')
buyCrypto = types.KeyboardButton(text='Покупка крипта')
sellCrypto  = types.KeyboardButton(text='Продажа крипта')
refill_btn = types.KeyboardButton(text='/refill')
stocks_btn = types.KeyboardButton(text='/stocks')
spending_btn = types.KeyboardButton(text='/spending')
refillCrypto_btn = types.KeyboardButton(text='/refillCrypto')
spendingCrypto_btn = types.KeyboardButton(text='/spendingCrypto')

markup_inline.add(buy, sell)
markup_inline.add(buyCrypto, sellCrypto)
markup_inline.add(stocks_btn, helpBtn)
markup_inline.add(refill_btn, spending_btn)
markup_inline.add(refillCrypto_btn, spendingCrypto_btn)



@bot.message_handler(commands=['start', 'help'])
@valid.official
def start(message):
    text="/stocks - показать текущее состояние портфеля\n/refill - пополнение\n/spending - трата (коммиссия, налоги, снять со счёта)"
    bot.send_message(message.chat.id, text, parse_mode= 'Markdown', reply_markup=markup_inline)


@bot.message_handler(commands=['stocks'])
@valid.official
def getStocks(message):
    bot.send_message(message.chat.id, totalCapital())
    try:
        bot.send_message(message.chat.id, cryptoCurrencyInfo())
    except telebot.apihelper.ApiTelegramException:
        pass

@bot.message_handler(commands=['refill'])
@valid.official
def getRefill(message):
    bot.send_message(message.chat.id, "Введите сумму пополнения")
    bot.register_next_step_handler(message, getRefilling)
def getRefilling(message):
    money=float(message.text)
    file = rwControler(dirStocks)
    data = file.readStocks()
    data["Currency"][0]["RUB"]=float(data["Currency"][0]["RUB"])+money
    bot.send_message(message.chat.id, "Свободные средства: "+str(data["Currency"][0]["RUB"]))
    file.writeStocks(data)


@bot.message_handler(commands=['spending'])
@valid.official
def getSpend(message):
    bot.send_message(message.chat.id, "Введите сумму траты (налога, коммисии)")
    bot.register_next_step_handler(message, getSpending)
def getSpending(message):
    money=float(message.text)
    file = rwControler(dirStocks)
    data = file.readStocks()
    data["Currency"][0]["RUB"]=float(data["Currency"][0]["RUB"])-money
    bot.send_message(message.chat.id, "Свободные средства: "+str(data["Currency"][0]["RUB"]))
    file.writeStocks(data)

@bot.message_handler(commands=['refillCrypto'])
@valid.official
def getRefillCrypto(message):
    bot.send_message(message.chat.id, "Введите сумму пополнения")
    bot.register_next_step_handler(message, getRefillingCrypto)
def getRefillingCrypto(message):
    money=float(message.text)
    file = rwControler(dirStocks)
    data = file.readStocks()
    data["Currency"][1]["USDT"]=float(data["Currency"][1]["USDT"])+money
    bot.send_message(message.chat.id, "Свободные средства: $"+str(data["Currency"][1]["USDT"]))
    file.writeStocks(data)


@bot.message_handler(commands=['spendingCrypto'])
@valid.official
def getSpendCrypto(message):
    bot.send_message(message.chat.id, "Введите сумму траты (налога, коммисии)")
    bot.register_next_step_handler(message, getSpendingCrypto)
def getSpendingCrypto(message):
    money=float(message.text)
    file = rwControler(dirStocks)
    data = file.readStocks()
    data["Currency"][1]["USDT"]=float(data["Currency"][1]["USDT"])-money
    bot.send_message(message.chat.id, "Свободные средства: $"+str(data["Currency"][1]["USDT"]))
    file.writeStocks(data)


@bot.message_handler(content_types=["text"])
@valid.official
def handle_text(message):
    try:
        status, cryptoStatus = message.text.split(" ")
    except ValueError:
        status= message.text
        cryptoStatus=None
    if status not in ("Покупка", "Продажа","покупка", "продажа"):
        return 
    
    bot.send_message(message.chat.id, "Введите тикет (короткое название) компании:")
    bot.register_next_step_handler(message, getShortName, status, cryptoStatus)
def getShortName(message, status, cryptoStatus):
    if status not in ("Покупка", "Продажа","покупка", "продажа", "cnjg", "Cnjg"):
        bot.send_message(message.chat.id, "Отмена!")
        return
    shortName=message.text
    if shortName.isupper()!=True:
        shortName=shortName.upper()
    bot.send_message(message.chat.id, "Введите количество:")
    bot.register_next_step_handler(message, getCountStock, shortName, status, cryptoStatus)
def getCountStock(message, shortName, status, cryptoStatus):
    if status not in ("Покупка", "Продажа","покупка", "продажа", "cnjg", "Cnjg"):
        bot.send_message(message.chat.id, "Отмена!")
        return
    count=float(message.text)
    bot.send_message(message.chat.id, "Введите цену:")
    bot.register_next_step_handler(message, getPriceStock, shortName, count, status, cryptoStatus)
def getPriceStock(message, shortName, count, status, cryptoStatus):
    if status not in ("Покупка", "Продажа","покупка", "продажа", "cnjg", "Cnjg"):
        bot.send_message(message.chat.id, "Отмена!")
        return
    price=float(message.text)
    ccount=count
    file = rwControler(dirStocks)
    data = file.readStocks()
    if (cryptoStatus!="крипта" and shortName not in data["tickets"]):
        data["tickets"].append(shortName)
        data["Stocks"].append({"name":getNameFromMOEX(shortName), "stock":shortName, "buy_price":[]})
    if (cryptoStatus=="крипта" and shortName not in data["ticketsCrypto"]):
        data["ticketsCrypto"].append(shortName)
        data["Crypto"].append({"name":getNameFromKucoin(shortName), "stock":shortName, "buy_price":[]})
    if status in ("Продажа", "продажа"):
        ccount=float("-"+str(ccount))
        if (cryptoStatus == 'крипта'):
            data["Currency"][1]["USDT"]=float(data["Currency"][1]["USDT"])+price*count
        else:
            data["Currency"][0]["RUB"]=float(data["Currency"][0]["RUB"])+price*count
    else:
        if (cryptoStatus == 'крипта'):
            data["Currency"][1]["USDT"]=float(data["Currency"][1]["USDT"])-price*count
        else:
            data["Currency"][0]["RUB"]=float(data["Currency"][0]["RUB"])-price*count

    if (cryptoStatus != 'крипта'):
        for stock in data["Stocks"]:
            if stock["stock"]==shortName:
                index=data["Stocks"].index(stock)
                buy_list = data["Stocks"][index]["buy_price"]
                buy_list.append({"count":ccount, "price":price})
                all_count_stock=0
                for item in buy_list:
                    all_count_stock+=item["count"]
                if all_count_stock==0:
                    data["Stocks"].pop(index)
                    data["tickets"].remove(shortName)
        bot.send_message(message.chat.id, status+" : "+shortName+" - "+str(formatZero(count))+" шт по  "+str(formatZero(price))+f'\nОстаток на счёте: {data["Currency"][0]["RUB"]}р', parse_mode= 'Markdown', reply_markup=markup_inline)
        
    else:
        for stock in data["Crypto"]:
            if stock["stock"]==shortName:
                index=data["Crypto"].index(stock)
                buy_list = data["Crypto"][index]["buy_price"]
                buy_list.append({"count":float(ccount), "price":price})
                all_count_stock=0
                for item in buy_list:
                    all_count_stock+=item["count"]
                if all_count_stock==0:
                    data["Crypto"].pop(index)
                    data["ticketsCrypto"].remove(shortName)
        bot.send_message(message.chat.id, status+" : "+shortName+" - "+str(formatZero(count))+" шт по  "+str(formatZero(price))+f'\nОстаток на счёте: ${data["Currency"][1]["USDT"]}', parse_mode= 'Markdown', reply_markup=markup_inline)
    
    
    file.writeStocks(data)

def main():
    checkFileExist()
    bot.infinity_polling()

if __name__ == '__main__':
    main()