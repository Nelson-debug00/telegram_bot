from flask import Flask
import os
import threading
import main # Importa main.py donde está la definición del bot

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot de Telegram en ejecución (Servidor Flask Activo)"

def run_bot():
    # Iniciamos el bot desde aquí usando el objeto definido en main.py
    print("Iniciando polling del bot...")
    main.bot.infinity_polling()

if __name__ == "__main__":
    # Iniciamos el bot en un hilo para que no bloquee a Flask
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.setDaemon(True) # Se asegura que el hilo muera si Flask se detiene
    bot_thread.start()
    
    # Iniciamos el servidor Flask
    # Ajustamos el puerto a 8080 o el que Render asigne
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)