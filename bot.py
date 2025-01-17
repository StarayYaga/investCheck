import telebot
from telebot import types
from main import rwControl
from main import getStock
from valid import Valid
from config import botToken, dirStocks


bot = telebot.TeleBot(botToken)
markup_inline = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
valid = Valid(bot=bot)

buy = types.KeyboardButton(text='Покупка')
sell = types.KeyboardButton(text='Продажа')

markup_inline.row(buy, sell)

@bot.message_handler(commands=['start', 'help'])
@valid.official
def start(message):
    text="/stocks - показать текущее состояние портфеля\n/refill - пополнение\n/spending - трата (коммиссия, налоги, снять со счёта)"
    bot.send_message(message.chat.id, text, parse_mode= 'Markdown', reply_markup=markup_inline)


@bot.message_handler(commands=['stocks'])
@valid.official
def getStocks(message):
    bot.send_message(message.chat.id, getStock())


@bot.message_handler(commands=['refill'])
@valid.official
def getRefill(message):
    bot.send_message(message.chat.id, "Введите сумму пополнения")
    bot.register_next_step_handler(message, getRefilling)
def getRefilling(message):
    money=float(message.text)
    file = rwControl(dirStocks)
    data = file.readStocks()
    data["Currency"][0]["RUB"]=str(float(data["Currency"][0]["RUB"])+money)
    bot.send_message(message.chat.id, "Свободные средства: "+data["Currency"][0]["RUB"])
    file.writeStocks(data)


@bot.message_handler(commands=['spending'])
@valid.official
def getSpend(message):
    bot.send_message(message.chat.id, "Введите сумму траты (налога, коммисии)")
    bot.register_next_step_handler(message, getSpending)
def getSpending(message):
    money=float(message.text)
    file = rwControl(dirStocks)
    data = file.readStocks()
    data["Currency"][0]["RUB"]=str(float(data["Currency"][0]["RUB"])-money)
    file.writeStocks(data)


@bot.message_handler(content_types=["text"])
@valid.official
def handle_text(message):
    status = message.text

    if status not in ("Покупка", "Продажа","покупка", "продажа"):
        return 
    
    bot.send_message(message.chat.id, "Введите тикет (короткое название) компании:")
    bot.register_next_step_handler(message, getShortName, status)
def getShortName(message, status):
    shortName=message.text
    if shortName.isupper()!=True:
        shortName=shortName.upper()
    
    bot.send_message(message.chat.id, "Введите количество:")
    bot.register_next_step_handler(message, getCountStock, shortName, status)
def getCountStock(message, shortName, status):
    count=message.text
    bot.send_message(message.chat.id, "Введите цену:")
    bot.register_next_step_handler(message, getPriceStock, shortName, count, status)
def getPriceStock(message, shortName, count, status):
    price=float(message.text)
    ccount=count
    file = rwControl(dirStocks)
    data = file.readStocks()
    if status in ("Продажа", "продажа"):
        ccount="-"+ccount
        data["Currency"][0]["RUB"]=str(float(data["Currency"][0]["RUB"])+price*float(count))
    else:
        data["Currency"][0]["RUB"]=str(float(data["Currency"][0]["RUB"])-price*float(count))

    for stock in data["Stocks"]:
        if stock["stock"]==shortName:
            data["Stocks"][data["Stocks"].index(stock)]["buy_price"].append({"count":ccount, "price":str(price)})

    bot.send_message(message.chat.id, status+" : "+shortName+" - "+str(count)+" шт по  "+str(price)+f'\nОстаток на счёте: {float(data["Currency"][0]["RUB"])}р', parse_mode= 'Markdown', reply_markup=markup_inline)
    file.writeStocks(data)

def main():
    bot.infinity_polling()

if __name__ == '__main__':
    main()