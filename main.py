import telebot
from telebot import types
from dolar_price import get_price

bot = telebot.TeleBot("8771699547:AAGn8zTo6cp4qgGRxYeLelLp-R7NHNUU18g", parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    btn_dolar = types.KeyboardButton("💸 Ver Precio Dólar y Euro")

    markup.add(btn_dolar)

    bot.reply_to(message, "Hola, ¿en qué puedo ayudarte?", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "💸 Ver Precio Dólar y Euro":
	    bot.reply_to(message, f"Precio actual USD/EUR tasa BCV: {get_price()}")
    
    else:
        bot.reply_to(message, "Usa el botón de abajo para consultar el precio.")

bot.infinity_polling()