from datetime import datetime
from telebot import types
from services.salary_service import calculate_salary
from services.sheets_penalties import get_penalties

MONTHS_RU = {
    1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель",
    5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
    9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
}

CATEGORY_VIEW = {
    1: "🥇 Золото",
    2: "🥈 Серебро",
    3: "🥉 Бронза"
}



def format_month(month_key: str) -> str:
    dt = datetime.strptime(month_key, "%Y-%m")
    month_name = MONTHS_RU[dt.month]
    return f"{month_name} | {dt.strftime('%m.%Y')}"


def build_salary_text(month_key, salary_data):
    category_text = CATEGORY_VIEW.get(
        salary_data["category"], "🥉 Бронза"
    )
    
    penalties = salary_data["penalties"]
    if penalties:
        penalties_text = "\n".join(
            f"➖ {p['reason']} | {p['amount']} грн" for p in penalties
        )
        penalties_line = (
            f"⁉ Штрафы: {salary_data['penalties_total']} грн\n"
            f"{penalties_text}\n"
        )
    else:
        penalties_line = "⁉ Штрафы: 0 грн\n"


    plan_percent = salary_data.get("plan_percent")
    
    if plan_percent is None:
        plan_line = "📈 План | Отсутствует\n➕ Бонус: 0 грн\n\n"
    else:
        plan_line = (
            f"📈 План | {plan_percent:.2f}%\n"
            f"➕ Бонус: {salary_data['plan_bonus_total']:.2f} грн\n\n"
        )
    


    text = (
        f"💰 Зарплата за {format_month(month_key)}\n\n"

        f"✅ Смен: {salary_data['shifts_count']}\n"
        f"💵 За смены: {salary_data['shift_pay']} грн\n\n"

        f"{category_text}\n"
        f"➕ Бонус категории: {salary_data['category_bonus']} грн\n\n"

        f"💎 Выручка\n"
        f"➕ Бонус: {salary_data['revenue_bonus']:.2f} грн\n\n"

        f"{plan_line}"
        
        
        f"{penalties_line}"
        f"━━━━━━━━━━━━━━━━\n"
        f"💰 ИТОГО: {salary_data['total']:.2f} грн"
    )

        
    return text



def send_salary(bot, chat_id, user_id, month_key):
    salary_data = calculate_salary(user_id, month_key)

    text = build_salary_text(month_key, salary_data)
    
    keyboard = types.InlineKeyboardMarkup()
    prev_btn = types.InlineKeyboardButton("⬅️", callback_data=f"salary:{prev_month(month_key)}")
    next_btn = types.InlineKeyboardButton("➡️", callback_data=f"salary:{next_month(month_key)}")
    keyboard.add(prev_btn, next_btn)
    
    bot.send_message(chat_id, text, reply_markup=keyboard)



def register_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == "💰 Зарплата")
    def handle_salary(message):
        month_key = datetime.now().strftime("%Y-%m")
        send_salary(bot, message.chat.id, message.from_user.id, month_key)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("salary:"))
    def handle_salary_callback(call):
        month_key = call.data.split(":")[1]
        # Удаляем старое сообщение
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        send_salary(bot, call.message.chat.id, call.from_user.id, month_key)


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
