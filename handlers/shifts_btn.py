from datetime import datetime
from telebot import types
#from services.storage import get_user_shift
from services.sheets import get_or_create_worksheet
from services.sheets_shifts import get_shifts

shifts_sheet = get_or_create_worksheet(
    "shifts",
    ["user_id", "month", "shift_date", "revenue", "created_at"]
)



def send_shifts(bot, chat_id, user_id, month_key):
    shifts = get_shifts(user_id, month_key)
    
    text = f"📅 Смены за {month_key}\n\n"

    if not shifts:
        text += "❌ Смен нет"
    else:
        for date in sorted(shifts):
            text += f"✅ Смена: {date}\n"

   
    keyboard = types.InlineKeyboardMarkup()
    prev_btn = types.InlineKeyboardButton("⬅️", callback_data=f"shifts:{prev_month(month_key)}")
    next_btn = types.InlineKeyboardButton("➡️", callback_data=f"shifts:{next_month(month_key)}")
    keyboard.add(prev_btn, next_btn)

    bot.send_message(chat_id, text, reply_markup=keyboard)



def register_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "🗓 Смены")
    def handle_shifts(message):
        month_key = datetime.now().strftime("%Y-%m")
        send_shifts(bot, message.chat.id, message.from_user.id, month_key)

    # Нажатие ⬅️ ➡️
    @bot.callback_query_handler(func=lambda call: call.data.startswith("shifts:"))
    def handle_shift_callback(call):
        month_key = call.data.split(":")[1]
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        send_shifts(bot, call.message.chat.id, call.from_user.id, month_key)



def prev_month(month_key):
    dt = datetime.strptime(month_key, "%Y-%m")
    year = dt.year
    month = dt.month - 1

    if month == 0:
        month = 12
        year -= 1

    return f"{year}-{month:02d}"


def next_month(month_key):
    dt = datetime.strptime(month_key, "%Y-%m")
    year = dt.year
    month = dt.month + 1

    if month == 13:
        month = 1
        year += 1

    return f"{year}-{month:02d}"
