from flask import Flask, render_template, jsonify
import threading
import logica_bot
from get_prices import get_dolar_prices

app = Flask(__name__)

@app.route('/')
def index():
    dolar, euro, usdt, fecha_bcv, fecha_usdt = get_dolar_prices()
    return render_template("index.html", dolar=dolar, euro=euro, usdt=usdt, fecha_bcv=fecha_bcv, fecha_usdt=fecha_usdt)

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