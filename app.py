from flask import Flask
import os
import threading
import main # Importa main.py donde está la definición del bot

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot de Telegram en ejecución (Servidor Flask Activo)"

def run_bot():
    try:
        # Iniciamos el bot desde aquí usando el objeto definido en main.py
        print("Iniciando polling del bot...")
        main.bot.infinity_polling()
    except Exception as e:
        print(f"ERROR CRÍTICO EN EL BOT: {e}")

# Iniciamos el bot en un hilo al cargar el módulo (necesario para Gunicorn en Render)
bot_thread = threading.Thread(target=run_bot)
bot_thread.daemon = True # Usamos .daemon para compatibilidad
bot_thread.start()

if __name__ == "__main__":
    # Esto solo se ejecuta al correr localmente: python app.py
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
