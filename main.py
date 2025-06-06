import requests
import schedule
import time
from config import channelId, botToken, ownerId, crypto
from setup import main as checkFileExist
from stock import totalCapital
from cryptoCurrency import cryptoCurrencyInfo

def send_text(text, chat, token):
    requests.post(
        url=f"https://api.telegram.org/bot{token}/sendMessage",
        data = {
            "chat_id":chat,
            "text":text
        })    


def main():
    capital= totalCapital()
    send_text(capital, ownerId, botToken)
    send_text(capital, channelId, botToken)
    if crypto:
        cryptoInfo=cryptoCurrencyInfo()
        send_text(cryptoInfo, ownerId, botToken)
        send_text(cryptoInfo, channelId, botToken)



if __name__ == '__main__':
    checkFileExist()
    main()
    print("start")

    schedule.every().day.at("08:00").do(main)
    schedule.every().day.at("12:00").do(main)
    schedule.every().day.at("16:00").do(main)
    schedule.every().day.at("20:00").do(main)
    schedule.every().day.at("00:00").do(main)

    print("set time")
    while True:
        schedule.run_pending()
        time.sleep(1)
