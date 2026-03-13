from flask import Flask
import os
import threading
import main

app = Flask(__name__)

@app.route('/')
def index():
    # Aquí puedes ejecutar tu lógica principal
    return "Bot de telegram en ejecución"

def run_bot():
    main.bot.infinity_polling()

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    app.run(host='0.0.0.0', port=os.getenv('PORT', 8080))