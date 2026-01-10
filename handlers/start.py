from telebot import types

def register_handlers(bot):
    @bot.message_handler(commands=['beerland'])
    def start_handler(message):
        user_name = message.from_user.first_name
        # Создаем кнопки 
        keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        btn_shifts = types.KeyboardButton("🗓 Смены")
        btn_plan = types.KeyboardButton("📊 План")
        btn_fine = types.KeyboardButton("❌ Штраф")
        btn_category = types.KeyboardButton("🏷 Категория")
        btn_salary = types.KeyboardButton("💰 Зарплата")
        keyboard.add(btn_shifts, btn_plan, btn_fine, btn_category, btn_salary)
        
        bot.send_message(
            message.chat.id,
            f"Привет! {user_name}!",
            reply_markup=keyboard)

    

    @bot.message_handler(commands=['helps'])
    def helps_text(message):
        bot.send_message(
            message.chat.id,
        """
        Для удаления лишней смены:\n
        /remove ДД.ММ.ГГГГ\n
        /remove 07.04.2026\n
Для удаления штрафа:\n
        /remove_p ГГГГ.ММ Причина\n
        /remove_p 2026-03 Опоздания\n
Причину надо писать одинаково как она и написана в зарплате!
        """
        )