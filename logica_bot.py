import telebot
from telebot import types
from get_prices import get_dolar_prices, get_last_price
from services.calculadoras import *

bot = telebot.TeleBot("8771699547:AAGn8zTo6cp4qgGRxYeLelLp-R7NHNUU18g", parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    btn_dolar = types.KeyboardButton("💸 Ver Precio Dólar y Euro")
    markup.add(btn_dolar)

    btn_usdt = types.KeyboardButton("💸 Ver Precio USDT")
    markup.add(btn_usdt)

    btn_calculadora_tasa_actual = types.KeyboardButton("📱 Calculadora Tasa Actual")
    markup.add(btn_calculadora_tasa_actual)
    
    btn_calculadora_tasa_anterior = types.KeyboardButton("📱 Calculadora Tasa Anterior")
    markup.add(btn_calculadora_tasa_anterior)

    btn_tasa_anterior = types.KeyboardButton("🔙 Tasa anterior")
    markup.add(btn_tasa_anterior)
    
    bot.reply_to(message, "Hola, ¿en qué puedo ayudarte?", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "💸 Ver Precio Dólar y Euro":
        dolar, euro, _, fecha_bcv, _ = get_dolar_prices()
        bot.reply_to(message, f"📈 Precios Actuales:\n\n💵 EUR (BCV): {euro} Bs\n💶 USD (BCV): {dolar} Bs\n\nFecha: {fecha_bcv}")

    elif message.text == "💸 Ver Precio USDT":
        _, _, usdt, _, fecha_usdt_str = get_dolar_prices()
        bot.reply_to(message, f"📈 Precio Actual:\n\n🪙 USDT: {usdt} Bs\n\nFecha: {fecha_usdt_str}")

    elif message.text == "📱 Calculadora Tasa Actual":
        bot.reply_to(message, "Selecciona una opción:", reply_markup=menu_calculadora_tasa_actual())
        
    elif message.text == "📱 Calculadora Tasa Anterior":
        bot.reply_to(message, "Selecciona una opción:", reply_markup=menu_calculadora_tasa_anterior())
    
    elif message.text == "🔙 Tasa anterior":
        bot.reply_to(message, "Selecciona una opción de la tasa anterior:", reply_markup=menu_tasa_anterior())
    
    else:
        bot.reply_to(message, "Usa el botón de abajo para consultar el precio.")

@bot.callback_query_handler(func=lambda call: True)
def callback_universal(call):
    # --- Calculadora Tasa Actual ---
    if call.data == "calc_bs_eur_usd_usdt":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "¿Qué monto quieres calcular?")
        bot.register_next_step_handler(call.message, calculadora_bs_eur_usd_usdt)

    elif call.data == "calc_eur_bs":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "¿Qué monto quieres calcular?")
        bot.register_next_step_handler(call.message, calculadora_eur_bs)

    elif call.data == "calc_usd_bs":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "¿Qué monto quieres calcular?")
        bot.register_next_step_handler(call.message, calculadora_usd_bs)

    elif call.data == "calc_usdt_bs":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "¿Qué monto quieres calcular?")
        bot.register_next_step_handler(call.message, calculadora_usdt_bs)

    # --- Calculadora Tasa Anterior ---
    elif call.data == "calc_bs_eur_usd_usdt_ant":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "¿Qué monto quieres calcular?")
        bot.register_next_step_handler(call.message, calculadora_bs_eur_usd_usdt_ant)

    elif call.data == "calc_eur_bs_ant":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "¿Qué monto quieres calcular?")
        bot.register_next_step_handler(call.message, calculadora_eur_bs_ant)

    elif call.data == "calc_usd_bs_ant":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "¿Qué monto quieres calcular?")
        bot.register_next_step_handler(call.message, calculadora_usd_bs_ant)

    elif call.data == "calc_usdt_bs_ant":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "¿Qué monto quieres calcular?")
        bot.register_next_step_handler(call.message, calculadora_usdt_bs_ant)

    # --- Ver Tasa Anterior (Precios) ---
    elif call.data == "tasa_dolar_euro_ant":
        bot.answer_callback_query(call.id)
        val_dolar, val_euro, _, fecha_bcv_ant, _ = get_last_price()
        bot.send_message(call.message.chat.id, f"📈 Tasa anterior:\n\n💵 EUR: {val_euro} Bs\n💶 USD: {val_dolar} Bs\n\nFecha: {fecha_bcv_ant}")

    elif call.data == "tasa_usdt_ant":
        bot.answer_callback_query(call.id)
        _, _, val_usdt, _, fecha_usdt_ant = get_last_price()
        bot.send_message(call.message.chat.id, f"Tasa anterior:\n\n🪙 USDT: {val_usdt} Bs\n\nFecha: {fecha_usdt_ant}")

def menu_calculadora_tasa_actual():
    markup = types.InlineKeyboardMarkup(row_width=1)

    btn_calc_bs = types.InlineKeyboardButton("📱 Calcular Bs a EUR/USD/USDT", callback_data="calc_bs_eur_usd_usdt")
    markup.add(btn_calc_bs)

    btn_calc_eur = types.InlineKeyboardButton("📱 Calcular EUR a Bs", callback_data="calc_eur_bs")
    markup.add(btn_calc_eur)

    btn_calc_usd = types.InlineKeyboardButton("📱 Calcular USD a Bs", callback_data="calc_usd_bs")
    markup.add(btn_calc_usd)

    btn_calc_usdt = types.InlineKeyboardButton("📱 Calcular USDT a Bs", callback_data="calc_usdt_bs")
    markup.add(btn_calc_usdt)
    return markup

def menu_calculadora_tasa_anterior():
    markup = types.InlineKeyboardMarkup(row_width=1)

    btn_calc_bs_eur_usd_usdt_ant = types.InlineKeyboardButton("📱 Calcular Bs a EUR/USD/USDT", callback_data="calc_bs_eur_usd_usdt_ant")
    markup.add(btn_calc_bs_eur_usd_usdt_ant)

    btn_calc_eur_bs_ant = types.InlineKeyboardButton("📱 Calcular EUR a Bs", callback_data="calc_eur_bs_ant")
    markup.add(btn_calc_eur_bs_ant)

    btn_calc_usd_bs_ant = types.InlineKeyboardButton("📱 Calcular USD a Bs", callback_data="calc_usd_bs_ant")
    markup.add(btn_calc_usd_bs_ant)

    btn_calc_usdt_bs_ant = types.InlineKeyboardButton("📱 Calcular USDT a Bs", callback_data="calc_usdt_bs_ant")
    markup.add(btn_calc_usdt_bs_ant)

    return markup

def menu_tasa_anterior():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_tasa_dolar_euro_ant = types.InlineKeyboardButton("💸 Ver tasa anterior USD/EUR", callback_data="tasa_dolar_euro_ant")
    markup.add(btn_tasa_dolar_euro_ant)
    btn_tasa_usdt_ant = types.InlineKeyboardButton("💸 Ver tasa anterior USDT", callback_data="tasa_usdt_ant")
    markup.add(btn_tasa_usdt_ant)
    return markup