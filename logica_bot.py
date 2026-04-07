import telebot
from telebot import types
from get_prices import get_dolar_prices, get_last_price
from services.calculadoras import *

bot = telebot.TeleBot("8771699547:AAGn8zTo6cp4qgGRxYeLelLp-R7NHNUU18g", parse_mode=None)

# Registrar comandos en el menú azul de Telegram (Discoverability)
bot.set_my_commands([
    types.BotCommand("start", "Reiniciar el bot"),
    types.BotCommand("usd", "Conversión rápida USD a Bs (ej: /usd 100)"),
    types.BotCommand("eur", "Conversión rápida EUR a Bs (ej: /eur 10)"),
    types.BotCommand("usdt", "Conversión rápida USDT a Bs (ej: /usdt 50)"),
])

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    btn_precios = types.KeyboardButton("📊 Ver Precios Actuales")
    markup.add(btn_precios)

    btn_calculadoras = types.KeyboardButton("📱 Calculadoras")
    markup.add(btn_calculadoras)

    btn_tasa_anterior = types.KeyboardButton("🔙 Consultar Tasa Anterior")
    markup.add(btn_tasa_anterior)
    
    welcome_text = (
        "¡Hola! Bienvenido a *Dolar Actual VE*.\n\n"
        "Consulta tasas oficiales BCV y paralelo en tiempo real.\n\n"
        "💡 *Tip para expertos:* Puedes escribir directamente `/usd 100` para convertir sin usar los botones."
    )
    
    bot.reply_to(message, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['usd', 'eur', 'usdt'])
def quick_calc(message):
    command = message.text.split()[0].replace('/', '').lower()
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, f"Uso: /{command} [monto]\nEjemplo: /{command} 100")
            return
            
        # Limpieza de símbolos comunes ($, €, Bs, USDT) para robustez
        monto_str = args[1].replace(',', '.').replace('$', '').replace('€', '').replace('Bs', '').lower().replace('usdt', '').strip()
        monto = float(monto_str)
        dolar, euro, usdt, _, _ = get_dolar_prices()
        
        if command == 'usd':
            res = monto * dolar
            bot.reply_to(message, f"💵 {monto} USD = {res:.2f} Bs\n(Tasa: {dolar:.2f})")
        elif command == 'eur':
            res = monto * euro
            bot.reply_to(message, f"💶 {monto} EUR = {res:.2f} Bs\n(Tasa: {euro:.2f})")
        elif command == 'usdt':
            res = monto * usdt
            bot.reply_to(message, f"🪙 {monto} USDT = {res:.2f} Bs\n(Tasa: {usdt:.2f})")
            
    except ValueError:
        bot.reply_to(message, "Por favor, ingresa un número válido después del comando.")
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "📊 Ver Precios Actuales":
        dolar, euro, usdt, fecha_bcv, fecha_usdt_str = get_dolar_prices()
        response = (
            f"📈 *Precios Actuales*\n\n"
            f"💵 USD: {dolar:.2f} Bs\n"
            f"💶 EUR: {euro:.2f} Bs\n"
            f"🪙 USDT: {usdt:.2f} Bs\n\n"
            f"🕒 BCV: {fecha_bcv}\n"
            f"🕒 USDT: {fecha_usdt_str}\n\n"
            f"⚡ *Convertir rápido:* Escribe `/usd 100`"
        )
        bot.reply_to(message, response, parse_mode="Markdown")

    elif message.text == "📱 Calculadoras":
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_actual = types.InlineKeyboardButton("✨ Tasa Actual", callback_data="menu_calc_actual")
        btn_anterior = types.InlineKeyboardButton("🔙 Tasa Anterior", callback_data="menu_calc_ant")
        markup.add(btn_actual, btn_anterior)
        bot.reply_to(message, "Selecciona qué calculadora deseas usar:", reply_markup=markup)
        
    elif message.text == "🔙 Consultar Tasa Anterior":
        bot.reply_to(message, "Selecciona una opción de la tasa anterior:", reply_markup=menu_tasa_anterior())
    
    else:
        bot.reply_to(message, "Usa los botones del menú o los comandos como /usd 100 para calcular.")

@bot.callback_query_handler(func=lambda call: True)
def callback_universal(call):
    # --- Navegación de Menús ---
    if call.data == "menu_calc_actual":
        bot.edit_message_text("📱 Calculadora (Tasa Actual):", call.message.chat.id, call.message.message_id, reply_markup=menu_calculadora_tasa_actual())
    
    elif call.data == "menu_calc_ant":
        bot.edit_message_text("🔙 Calculadora (Tasa Anterior):", call.message.chat.id, call.message.message_id, reply_markup=menu_calculadora_tasa_anterior())

    # --- Calculadora Tasa Actual ---
    elif call.data == "calc_bs_eur_usd_usdt":
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
        dolar_ant, euro_ant, _, fecha_bcv_ant, _ = get_last_price()
        bot.send_message(call.message.chat.id, f"📈 Tasa anterior:\n\n💵 EUR: {euro_ant:.2f} Bs\n💶 USD: {dolar_ant:.2f} Bs\n\nFecha: {fecha_bcv_ant}")

    elif call.data == "tasa_usdt_ant":
        bot.answer_callback_query(call.id)
        _, _, usdt_ant, _, fecha_usdt_ant = get_last_price()
        bot.send_message(call.message.chat.id, f"Tasa anterior:\n\n🪙 USDT: {usdt_ant:.2f} Bs\n\nFecha: {fecha_usdt_ant}")

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