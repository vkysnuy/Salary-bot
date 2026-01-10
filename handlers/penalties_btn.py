from datetime import datetime
from services.storage import month_settings_storage, user_state
from telebot import types
from services.sheets_penalties import add_penalty, remove_penalty
from services.sheets import get_or_create_worksheet

penalties_sheet = get_or_create_worksheet(
    "penalties",
    ["user_id", "month", "date", "reason", "amount"]
    )  


def register_handlers(bot):

   
    @bot.message_handler(func=lambda m: m.text == "❌ Штраф")
    def handle_penalties(message):
        month_key = datetime.now().strftime("%Y-%m")
        user_id = message.from_user.id
        

        if user_id not in month_settings_storage:
            month_settings_storage[user_id] = {}
        if month_key not in month_settings_storage[user_id]:
            month_settings_storage[user_id][month_key] = {"penalties": []}

        
        bot.delete_message(message.chat.id, message.message_id)

        
        msg = bot.send_message(
            message.chat.id,
            "❓ За что был выдан штраф?",
            reply_markup=types.InlineKeyboardMarkup(
                [[types.InlineKeyboardButton("Ошибка", callback_data="penalty_error")]]
            )
        )

        
        user_state[user_id] = {
            "state": "entering_penalty_reason",
            "month_key": month_key,
            "question_msg_id": msg.message_id
        }
        

    
    
    @bot.callback_query_handler(func=lambda c: c.data == "penalty_error")
    def handle_penalty_error(call):
        user_id = call.from_user.id
        
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        if user_id in user_state:
            user_state.pop(user_id)
        bot.answer_callback_query(call.id, "❌ Штраф отменён")


    
    @bot.message_handler(func=lambda m: user_state.get(m.from_user.id, {}).get("state") == "entering_penalty_reason")
    def handle_penalties_quest(message):
        user_id = message.from_user.id

        
        bot.delete_message(message.chat.id, user_state[user_id]["question_msg_id"])
        bot.delete_message(message.chat.id, message.message_id)

        
        user_state[user_id]["reason"] = message.text
        user_state[user_id]["state"] = "entering_penalty_amount"

    
        msg = bot.send_message(message.chat.id, "❓ Какая сумма штрафа?")
        user_state[user_id]["question_msg_id"] = msg.message_id


   
    @bot.message_handler(func=lambda m: user_state.get(m.from_user.id, {}).get("state") == "entering_penalty_amount")
    def handle_penalties_amount(message):
        user_id = message.from_user.id
        month_key = user_state[user_id]["month_key"]
        reason = user_state[user_id]["reason"]

        try:
            amount = int(message.text.replace(",", ""))
        except ValueError:
            bot.send_message(message.chat.id, "❌ Введите число для суммы штрафа!")
            return

        
        if not isinstance(month_settings_storage[user_id][month_key].get("penalties"), list):
            month_settings_storage[user_id][month_key]["penalties"] = []

        add_penalty(
        user_id=user_id,
        month_key=month_key,
        reason=reason,
        amount=amount
        )   

    
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, user_state[user_id]["question_msg_id"])

        
        user_state.pop(user_id)

        bot.send_message(
            message.chat.id,
            f"Штраф добавлен ✅\nПричина: {reason}\nСумма: {amount} грн"
        )

    @bot.message_handler(commands=["remove_p"])
    def handle_remove_penalty(message):
        parts = message.text.split(maxsplit=2)

        if len(parts) < 3:
            bot.send_message(
                message.chat.id,
                "❌ Пример:\n/remove_p ГГГГ-ММ Причина\n/remove_p 2025-12 Опоздания"
            )
            return

        month_key = parts[1]
        reason = parts[2]

        success = remove_penalty(
            penalties_sheet,
            user_id=message.from_user.id,
            month_key=month_key,
            reason=reason
        )

        if success:
            bot.send_message(
                message.chat.id,
                f"🗑 Штраф удалён:\n{month_key} — {reason}"
            )
        else:
            bot.send_message(
                message.chat.id,
                f"⚠️ Штраф с причиной «{reason}» не найден" 
            )
