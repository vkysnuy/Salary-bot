from telebot import types
from datetime import datetime
from services.storage import month_settings_storage # < удаляем
from services.sheet_month_setting import set_category
from services.sheet_month_setting import month_settings_sheet

CATEGORY_VIEW = {
    1: "🥇 Золото",
    2: "🥈 Серебро",
    3: "🥉 Бронза"
}

def get_category_keyboard(month_key):
    """Создаёт inline-кнопки выбора категории"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("🥇 Золото", callback_data=f"category:{month_key}:1"),
        types.InlineKeyboardButton("🥈 Серебро", callback_data=f"category:{month_key}:2"),
        types.InlineKeyboardButton("🥉 Бронза", callback_data=f"category:{month_key}:3")
    )
    return keyboard

def get_month_choice_keyboard():
    now = datetime.now()
    current_month = now.strftime("%Y-%m")

    prev = now.replace(day=1)
    if prev.month == 1:
        prev_month = f"{prev.year - 1}-12"
    else:
        prev_month = f"{prev.year}-{prev.month - 1:02d}"

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("⬅️ Прошлый месяц", callback_data=f"category_month:{prev_month}"),
        types.InlineKeyboardButton("📅 Текущий месяц", callback_data=f"category_month:{current_month}")
    )
    return keyboard


def register_handlers(bot):
    """Обработчик кнопки 🏷 Категория и выбор категории"""
    
    # Нажатие кнопки 🏷 Категория
    @bot.message_handler(func=lambda m: m.text == "🏷 Категория")
    def handle_category_button(message):
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(
        message.chat.id,
        "📅 За какой месяц выбрать категорию?",
        reply_markup=get_month_choice_keyboard()
        )

    # Нажатие одной из inline-кнопок категории
    @bot.callback_query_handler(func=lambda c: c.data.startswith("category:"))
    def handle_category_choice(call):
        _, month_key, category = call.data.split(":")
        category = int(category)
        user_id = call.from_user.id
        
        set_category(
            month_settings_sheet,
            user_id,
            month_key,
            category
        )
        
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"{CATEGORY_VIEW[category]} за {month_key} сохранено ✅")


    @bot.callback_query_handler(func=lambda c: c.data.startswith("category_month:"))
    def handle_category_month(call):
        month_key = call.data.split(":")[1]

        bot.edit_message_text(
        "🏷 Выберите категорию:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=get_category_keyboard(month_key)
    )
