import telebot
from forex_python.converter import CurrencyRates, CurrencyCodes
from forex_python.bitcoin import BtcConverter

bot = telebot.TeleBot('YOUR_BOT_TOKEN_HERE')
c = CurrencyRates()
cc = CurrencyCodes()
b = BtcConverter()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для конвертации валют и криптовалют. Чтобы узнать курс обмена, отправьте мне сообщение в формате '10 USD в RUB' или '0.5 BTC в USD'.")

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        amount, base_currency, _, target_currency = message.text.split()
        amount = float(amount)
        if base_currency == "BTC":
            result = b.convert_btc_to_cur(amount, target_currency)
            symbol = cc.get_symbol(target_currency)
            bot.reply_to(message, f"{amount} {base_currency} = {symbol}{result:.2f}")
        elif target_currency == "BTC":
            result = b.convert_to_btc(amount, base_currency)
            bot.reply_to(message, f"{amount} {base_currency} = {result:.8f} {target_currency}")
        else:
            result = c.convert(base_currency, target_currency, amount)
            symbol = cc.get_symbol(target_currency)
            bot.reply_to(message, f"{amount} {base_currency} = {symbol}{result:.2f}")
    except:
        bot.reply_to(message, "Извините, я не понимаю. Пожалуйста, отправьте сообщение в формате '10 USD в RUB' или '0.5 BTC в USD'.")

bot.polling()
