import requests
import schedule
import time
from config import channelId, botToken, ownerId
from setup import main as checkFileExist
from stocks import totalCapital
from cryptoCurrency import cryptoCurrencyInfo

def send_text(text, chat, token):
    requests.post(
        url=f"https://api.telegram.org/bot{token}/sendMessage",
        data = {
            "chat_id":chat,
            "text":text
        })    


def main():
    send_text(totalCapital(), ownerId, botToken)
    send_text(cryptoCurrencyInfo(), ownerId, botToken)
    send_text(totalCapital(), channelId, botToken)
    send_text(cryptoCurrencyInfo(), channelId, botToken)


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
