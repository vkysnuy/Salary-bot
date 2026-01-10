import telebot
import os
from dotenv import load_dotenv 
from handlers import start
from handlers import shifts
from handlers import shifts_btn
from handlers import salary_btn
from handlers import category_btn
from handlers import plan_btn
from handlers import penalties_btn

load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"))


shifts_btn.register_handlers(bot)
plan_btn.register_handlers(bot)
category_btn.register_handlers(bot)
penalties_btn.register_handlers(bot)
salary_btn.register_handlers(bot)
start.register_handlers(bot)
shifts.logic_shift(bot)


bot.infinity_polling()
