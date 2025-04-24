import telebot
from telebot import types
from stocks import getNameFromMOEX, totalCapital
from cryptoCurrency import getNameFromKucoin, cryptoCurrencyInfo, formatZero
from rwControl import rwControler
from valid import Valid
from config import botToken, dirStocks
from setup import main as checkFileExist


bot = telebot.TeleBot(botToken)
valid = Valid(bot=bot)

markup_inline = types.ReplyKeyboardMarkup(resize_keyboard=True)

buy = types.KeyboardButton(text='Покупка')
helpBtn = types.KeyboardButton(text='/help')
sell = types.KeyboardButton(text='Продажа')
refill_btn = types.KeyboardButton(text='/refill')
stocks_btn = types.KeyboardButton(text='/stocks')
spending_btn = types.KeyboardButton(text='/spending')

markup_inline.add(buy, sell)
markup_inline.add(stocks_btn, helpBtn)
markup_inline.add(refill_btn, spending_btn)


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
    status=message.text
    if status not in ("Покупка", "Продажа","покупка", "продажа"):
        return 

    types_stocks=types.InlineKeyboardMarkup()
    crypto=types.InlineKeyboardButton(text="Криптовалюта", callback_data='currency_Crypto_'+status)
    stock=types.InlineKeyboardButton(text="Акции", callback_data='currency_Stocks_'+status)
    bond=types.InlineKeyboardButton(text="Облигации", callback_data='currency_Bonds_'+status)
    metal=types.InlineKeyboardButton(text="Металлы", callback_data='currency_Metals_'+status)
    types_stocks.row(crypto, stock).add(bond, metal)
    
    bot.send_message(message.chat.id, "Выберите тип актива для действия:", reply_markup=types_stocks)

#call of button
@bot.callback_query_handler(func=lambda call: True)
def step2(call):
    assetType=call.data.split("_")[1]
    action=call.data.split("_")[2]
    bot.send_message(call.message.chat.id, "Введите тикет (короткое название) компании:")
    if call.data.split("_")[0]=="currency":
        message = call.message
        bot.register_next_step_handler(message, getTicket, assetType, action)
def getTicket(message, assetType, action):
    shortName=message.text
    if shortName in ("Стоп", "стоп", "cnjp", "Cnjp", "Ыещз", "Ыещз", "Stop", "stop"):
        bot.send_message(message.chat.id, "СТОП!")
        return
    if shortName.isupper()!=True:
        shortName=shortName.upper()
    bot.send_message(message.chat.id, "Введите количество:")
    bot.register_next_step_handler(message, getCountStock, shortName, assetType, action)
def getCountStock(message, shortName, assetType, action):
    if message.text in ("Стоп", "стоп", "cnjp", "Cnjp", "Ыещз", "Ыещз", "Stop", "stop"):
        bot.send_message(message.chat.id, "СТОП!")
        return
    count=float(message.text)
    bot.send_message(message.chat.id, "Введите цену:")
    bot.register_next_step_handler(message, getPriceStock, shortName, count, assetType, action)
def getPriceStock(message, shortName, count, assetType, action):
    if message.text in ("Стоп", "стоп", "cnjp", "Cnjp", "Ыещз", "Ыещз", "Stop", "stop"):
        bot.send_message(message.chat.id, "СТОП!")
        return
    price=float(message.text)
    ccount=count
    file = rwControler(dirStocks)
    data = file.readStocks()
    
    if assetType != "Crypto":
        if shortName not in data["tickets"]:
            data["tickets"].append(shortName)
            data[assetType].append({"name":getNameFromMOEX(shortName), "stock":shortName, "buy_price":[]})            
        if action in ("Продажа", "продажа"):
            ccount=float("-"+str(ccount))
            data["Currency"][0]["RUB"]=float(data["Currency"][0]["RUB"])+price*count
        else:
            data["Currency"][0]["RUB"]=float(data["Currency"][0]["RUB"])-price*count
        
        for stock in data[assetType]:
            if stock["stock"]==shortName:
                index=data[assetType].index(stock)
                buy_list = data[assetType][index]["buy_price"]
                buy_list.append({"count":ccount, "price":price})
                all_count_stock=0
                for item in buy_list:
                    all_count_stock+=item["count"]
                if all_count_stock==0:
                    data[assetType].pop(index)
                    data["tickets"].remove(shortName)   
        text=f"{action} : {shortName} - {str(formatZero(count))} шт по {str(formatZero(price))}\nОстаток на счёте: {data['Currency'][0]['RUB']}р"
        
    else:
        if shortName not in data["ticketsCrypto"]:
            data["ticketsCrypto"].append(shortName)
            data["Crypto"].append({"name":getNameFromKucoin(shortName), "stock":shortName, "buy_price":[]})
        if action in ("Продажа", "продажа"):
            ccount=float("-"+str(ccount))
            data["Currency"][1]["USDT"]=float(data["Currency"][1]["USDT"])+price*count
        else:
            data["Currency"][1]["USDT"]=float(data["Currency"][1]["USDT"])-price*count
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
        text=f"{action} : {shortName} - {str(formatZero(count))} шт по {str(formatZero(price))}\nОстаток на счёте: {data['Currency'][1]['USDT']}р"
    
    bot.send_message(message.chat.id, text, reply_markup=markup_inline)
    file.writeStocks(data)

def main():
    checkFileExist()
    bot.infinity_polling()

if __name__ == '__main__':
    main()