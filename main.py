import telegram
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
from bs4 import BeautifulSoup

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
GROUP_ID = 'YOUR_GROUP_ID'

def get_exchange_rate():
    url = 'https://www.google.com/search?q=chf+to+tl&oq=chf+to+tl&aqs=chrome..69i57.1065j0j7&sourceid=chrome&ie=UTF-8'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    rate_element = soup.find('span', class_='DFlfde SwHCTb')
    if rate_element:
        rate = rate_element.text
        return float(rate.replace(' CHF', ''))
    return None

def check_exchange_rate(context: CallbackContext):
    rate = get_exchange_rate()
    if rate is not None:
        context.bot.send_message(chat_id=context.job.context, text=f"Exchange rate: {rate} CHF to TL")

def start(update: telegram.Update, context: CallbackContext):
    if update.message.chat.type == 'group':
        context.job_queue.run_repeating(check_exchange_rate, interval=60, first=0, context=update.message.chat_id)
        update.message.reply_text("Exchange rate updates enabled for this group!")
    else:
        context.job_queue.run_repeating(check_exchange_rate, interval=60, first=0, context=update.message.chat_id)
        update.message.reply_text("Exchange rate updates enabled for you!")

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
