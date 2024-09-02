import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TELEGRAM_TOKEN = '7500561846:AAGCpSlTDI6TaRJ5iNgfomY7E-6eTzxcJLA'

currency = 'usd'

def get_bitcoin_price(currency='usd'):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": currency
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    price = data.get("bitcoin", {}).get(currency, "Цена не найдена")
    return price

def start(update: Update, context: CallbackContext):
    keyboard = [
        [KeyboardButton("Получить цену биткоина")],
        [KeyboardButton("Изменить валюту")],
        [KeyboardButton("Цена за 1 BTC"), KeyboardButton("Цена за 5 BTC")],
        [KeyboardButton("Цена за 10 BTC")],
        [KeyboardButton("О боте"), KeyboardButton("Помощь")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text('Добро пожаловать! Выберите опцию:', reply_markup=reply_markup)

def handle_message(update: Update, context: CallbackContext):
    global currency

    text = update.message.text

    if text == "Получить цену биткоина":
        price = get_bitcoin_price(currency)
        update.message.reply_text(f"Текущая цена биткоина в {currency.upper()}: {price}")

    elif text == "Изменить валюту":
        keyboard = [
            [KeyboardButton("USD"), KeyboardButton("EUR")],
            [KeyboardButton("RUB"), KeyboardButton("Назад")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.message.reply_text("Выберите валюту:", reply_markup=reply_markup)
    
    elif text in ["USD", "EUR", "RUB"]:
        currency = text.lower()
        update.message.reply_text(f"Валюта изменена на {currency.upper()}")

    elif text == "Цена за 1 BTC":
        price = get_bitcoin_price(currency)
        update.message.reply_text(f"Цена за 1 BTC в {currency.upper()}: {price}")
    
    elif text == "Цена за 5 BTC":
        price = get_bitcoin_price(currency)
        total_price = float(price) * 5
        update.message.reply_text(f"Цена за 5 BTC в {currency.upper()}: {total_price}")
    
    elif text == "Цена за 10 BTC":
        price = get_bitcoin_price(currency)
        total_price = float(price) * 10
        update.message.reply_text(f"Цена за 10 BTC в {currency.upper()}: {total_price}")

    elif text == "О боте":
        update.message.reply_text("Этот бот предоставляет текущие цены на биткоин и может отображать цены в различных валютах.")

    elif text == "Помощь":
        update.message.reply_text("Используйте кнопки для получения текущей цены, изменения валюты или получения цен на разные количества биткоинов.")
    
    elif text == "Назад":
        start(update, context)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
