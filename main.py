import telebot
from telebot import types
from dolar_price import get_price, get_numeric_prices

bot = telebot.TeleBot("8771699547:AAGn8zTo6cp4qgGRxYeLelLp-R7NHNUU18g", parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)

    btn_dolar = types.KeyboardButton("💸 Ver Precio Dólar y Euro")
    markup.add(btn_dolar)

    btn_calcular_bs = types.KeyboardButton("📱 Calcular Bs a USD/EUR")
    markup.add(btn_calcular_bs)

    btn_calcular_usd = types.KeyboardButton("📱 Calcular USD a Bs")
    markup.add(btn_calcular_usd)

    btn_calcular_eur = types.KeyboardButton("📱 Calcular EUR a Bs")
    markup.add(btn_calcular_eur)
    
    bot.reply_to(message, "Hola, ¿en qué puedo ayudarte?", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "💸 Ver Precio Dólar y Euro":
	    bot.reply_to(message, f"Precio actual USD/EUR tasa BCV: {get_price()}")

    elif message.text == "📱 Calcular Bs a USD/EUR":
        bot.reply_to(message, "¿Qué monto quieres calcular?")
        bot.register_next_step_handler(message, calculadora_bs_usd_eur, *get_numeric_prices())
    
    elif message.text == "📱 Calcular USD a Bs":
        bot.reply_to(message, "¿Qué monto quieres calcular?")
        bot.register_next_step_handler(message, calculadora_usd_bs, *get_numeric_prices())
    
    elif message.text == "📱 Calcular EUR a Bs":
        bot.reply_to(message, "¿Qué monto quieres calcular?")
        bot.register_next_step_handler(message, calculadora_eur_bs, *get_numeric_prices())
    
    else:
        bot.reply_to(message, "Usa el botón de abajo para consultar el precio.")

def calculadora_bs_usd_eur(message, euro_numeric, dolar_numeric):
    try:
        amount = float(message.text)
        euro = amount / euro_numeric
        dolar = amount / dolar_numeric
        bot.reply_to(message, f"{amount} Bs son:\n{euro:.2f} €\n{dolar:.2f} $")
    except ValueError:
        bot.reply_to(message, "Por favor, ingresa un número válido.")

def calculadora_usd_bs(message, euro_numeric, dolar_numeric):
    try:
        amount = float(message.text)
        bolivares = amount * dolar_numeric
        bot.reply_to(message, f"{amount} USD son:\n{bolivares:.2f} Bs")
    except ValueError:
        bot.reply_to(message, "Por favor, ingresa un número válido.")

def calculadora_eur_bs(message, euro_numeric, dolar_numeric):
    try:
        amount = float(message.text)
        bolivares = amount * euro_numeric
        bot.reply_to(message, f"{amount} EUR son:\n{bolivares:.2f} Bs")
    except ValueError:
        bot.reply_to(message, "Por favor, ingresa un número válido.")