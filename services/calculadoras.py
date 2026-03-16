from get_prices import get_dolar_prices, get_last_price

# --- Calculadoras de Tasa Actual ---

def calculadora_bs_eur_usd_usdt(message):
    from main import bot
    try:
        dolar, euro, usdt, _, _ = get_dolar_prices()
        if dolar == 0 or euro == 0 or usdt == 0:
            bot.reply_to(message, "⚠️ No se pueden realizar cálculos porque uno de los precios no está disponible (es 0).")
            return
        amount = float(message.text)
        dolar = amount / dolar
        euro = amount / euro
        usdt = amount / usdt
        bot.reply_to(message, f"{amount} Bs son:\n\n💶 {euro:.2f} €\n💵 {dolar:.2f} $\n🪙 {usdt:.2f} USDT")
    except ValueError: 
        bot.reply_to(message, "Por favor, ingresa un número válido.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error interno: {e}")

def calculadora_eur_bs(message):
    from main import bot
    try:
        _, euro, _, _, _ = get_dolar_prices()
        amount = float(message.text)
        euro = amount * euro
        bot.reply_to(message, f"{amount} EUR son:\n{euro:.2f} Bs")
    except ValueError: 
        bot.reply_to(message, "Por favor, ingresa un número válido.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error interno: {e}")

def calculadora_usd_bs(message):
    from main import bot
    try:
        dolar, _, _, _, _ = get_dolar_prices()
        amount = float(message.text)
        dolar = amount * dolar
        bot.reply_to(message, f"{amount} USD son:\n{dolar:.2f} Bs")
    except ValueError: 
        bot.reply_to(message, "Por favor, ingresa un número válido.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error interno: {e}")

def calculadora_usdt_bs(message):
    from main import bot
    try:
        _, _, usdt, _, _ = get_dolar_prices()
        amount = float(message.text)
        usdt = amount * usdt
        bot.reply_to(message, f"{amount} USDT son:\n{usdt:.2f} Bs")
    except ValueError: 
        bot.reply_to(message, "Por favor, ingresa un número válido.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error interno: {e}")

# --- Calculadoras de Tasa Anterior ---

def calculadora_bs_eur_usd_usdt_ant(message):
    from main import bot
    try:
        val_dolar, val_euro, val_usdt, _, _ = get_last_price()
        if val_dolar == 0 or val_euro == 0 or val_usdt == 0:
            bot.reply_to(message, "⚠️ No se pueden realizar cálculos porque uno de los precios no está disponible (es 0).")
            return
        
        amount = float(message.text)
        dolar = amount / val_dolar
        euro = amount / val_euro
        usdt = amount / val_usdt
        bot.reply_to(message, f"{amount} Bs son:\n\n💶 {euro:.2f} €\n💵 {dolar:.2f} $\n🪙 {usdt:.2f} USDT")
    except ValueError: 
        bot.reply_to(message, "Por favor, ingresa un número válido.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error interno: {e}")

def calculadora_eur_bs_ant(message):
    from main import bot
    try:
        _, val_euro, _, _, _ = get_last_price()
        
        amount = float(message.text)
        euro = amount * val_euro
        bot.reply_to(message, f"{amount} EUR son:\n{euro:.2f} Bs")
    except ValueError: 
        bot.reply_to(message, "Por favor, ingresa un número válido.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error interno: {e}")

def calculadora_usd_bs_ant(message):
    from main import bot
    try:
        val_dolar, _, _, _, _ = get_last_price()

        amount = float(message.text)
        dolar = amount * val_dolar
        bot.reply_to(message, f"{amount} USD son:\n{dolar:.2f} Bs")
    except ValueError: 
        bot.reply_to(message, "Por favor, ingresa un número válido.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error interno: {e}")

def calculadora_usdt_bs_ant(message):
    from main import bot
    try:
        _, _, val_usdt, _, _ = get_last_price()

        amount = float(message.text)
        usdt = amount * val_usdt
        bot.reply_to(message, f"{amount} USDT son:\n{usdt:.2f} Bs")
    except ValueError: 
        bot.reply_to(message, "Por favor, ingresa un número válido.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error interno: {e}")