import telebot
import os
from dotenv import load_dotenv 
from flask import Flask, request


load_dotenv()

BOT_TOKEN = os.getenv("TOKEN_BOT")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)


from handlers import start
from handlers import shifts
from handlers import shifts_btn
from handlers import salary_btn
from handlers import category_btn
from handlers import plan_btn
from handlers import penalties_btn


@app.route("/", methods=["GET"])
def index():
    return "Bot is runing", 200 

@app.route("/webhook", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(
        request.stream.read().decode("utf-8")
    )
    bot.process_new_updates([update])
    return "ok", 200

def setup_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")


shifts_btn.register_handlers(bot)
plan_btn.register_handlers(bot)
category_btn.register_handlers(bot)
penalties_btn.register_handlers(bot)
salary_btn.register_handlers(bot)
start.register_handlers(bot)
shifts.logic_shift(bot)



if __name__ == "__main__":
    setup_webhook()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))