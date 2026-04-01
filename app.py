from flask import Flask, render_template, jsonify
import threading
import logica_bot
from get_prices import get_dolar_prices, get_last_price

app = Flask(__name__)

@app.route('/')
def index():
    dolar, euro, usdt, fecha_bcv, fecha_usdt = get_dolar_prices()
    dolar_ant, euro_ant, usdt_ant, fecha_bcv_ant, fecha_usdt_ant = get_last_price()
    return render_template("index.html", dolar=dolar, euro=euro, usdt=usdt, fecha_bcv=fecha_bcv, fecha_usdt=fecha_usdt, dolar_ant=dolar_ant, euro_ant=euro_ant, usdt_ant=usdt_ant, fecha_bcv_ant=fecha_bcv_ant, fecha_usdt_ant=fecha_usdt_ant)

@app.route('/contacto')
def contacto():
    return render_template("contacto.html")

@app.route('/api/rates')
def api_rates():
    dolar, euro, usdt, fecha_bcv, fecha_usdt = get_dolar_prices()
    return jsonify({
        'dolar': dolar,
        'euro': euro,
        'usdt': usdt,
        'fecha_bcv': fecha_bcv,
        'fecha_usdt': fecha_usdt
    })

@app.route('/graficos')
def graficos():
    history = get_history_prices(7)
    return render_template("graficos.html", history=history)

def run_bot():
    try:
        print("Iniciando polling del bot...")
        logica_bot.bot.infinity_polling()
    except Exception as e:
        print(f"ERROR CRÍTICO EN EL BOT: {e}")

bot_thread = threading.Thread(target=run_bot)
bot_thread.daemon = True
bot_thread.start()

if __name__ == "__main__":
    app.run()