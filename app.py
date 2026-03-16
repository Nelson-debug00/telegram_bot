from flask import Flask
import os
import threading
import main

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot de Telegram en ejecución (Servidor Flask Activo)"

def run_bot():
    try:
        print("Iniciando polling del bot...")
        main.bot.infinity_polling()
    except Exception as e:
        print(f"ERROR CRÍTICO EN EL BOT: {e}")

bot_thread = threading.Thread(target=run_bot)
bot_thread.daemon = True
bot_thread.start()

if __name__ == "__main__":
    app.run()