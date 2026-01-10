from telebot import types
from datetime import datetime
from services.sheets import get_or_create_worksheet
from services.sheet_month_setting import set_plan
from services.sheet_month_setting import month_settings_sheet

# Кнопка план, выставления плана, за прошлый или этот месяц, и обработчик кнопки ПЛАН

def get_month_choice_keyboard():
    now = datetime.now()
    current_month = now.strftime("%Y-%m")
    prev = now.replace(day=1)

    if prev.month == 1:
        prev_month = f"{prev.year - 1}-12"
    else:#
        prev_month = f"{prev.year}-{prev.month - 1:02d}"

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("⬅️ Прошлый месяц", callback_data=f"plan_month:{prev_month}"),
        types.InlineKeyboardButton("📅 Текущий месяц", callback_data=f"plan_month:{current_month}")   
    )
    
    return keyboard

def register_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == "📊 План")
    def handle_plan_button(message):
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(
            message.chat.id,
            "📅 За какой месяц план?",
            reply_markup=get_month_choice_keyboard()
        )
        
    
    @bot.callback_query_handler(func=lambda c: c.data.startswith("plan_month:"))
    def handle_plan_month(call):
        user_id = call.from_user.id
        _, month_key = call.data.split(":")

        bot.delete_message(call.message.chat.id, call.message.message_id)

        msg = bot.send_message(
            call.message.chat.id,
            f"📊 Введите процент выполнения плана за {month_key}:"
        )

        bot.register_next_step_handler(
            msg,
            handle_plan_input,
            month_key,
            msg.message_id
        )


    def handle_plan_input(message, month_key, question_msg_id):
        raw = message.text.strip().replace("%", "").replace(",", ".")
        user_id = message.from_user.id

        try:
            plan_percent = float(raw)
        except ValueError:
            bot.send_message(
                message.chat.id,
                "❌Введите число для плана!\nПример: 96 / 107.23"
            )
            return

        plan_percent = round(plan_percent, 2)

        set_plan(
            month_settings_sheet,
            user_id,
            month_key,
            plan_percent
        )
        
        bot.delete_message(message.chat.id, question_msg_id)
        bot.delete_message(message.chat.id, message.message_id)

        bot.send_message(
            message.chat.id,
            f"Процент выполнения плана за {month_key}\n{plan_percent}% сохранён ✅"
        )
