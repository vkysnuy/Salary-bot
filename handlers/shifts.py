from services.parser import parse_date, parse_revenue, parse_person
from services.storage import  shift_storage
from services.sheets_shifts import add_shift, remove_shift, shift_exists
from services.sheets import get_or_create_worksheet

shifts_sheet = get_or_create_worksheet(
    "shifts",
    ["user_id", "month", "shift_date", "revenue", "created_at"]
)

def logic_shift(bot):
    @bot.message_handler(commands=['remove'])
    def handle_remove_shift(message):
        date_obj, date_error = parse_date(message.text)

        if date_obj is None:
            bot.send_message(message.chat.id, "❌ Пример: /remove ДД.ММ.ГГГГ")
            return

        shift_date = date_obj.strftime("%d.%m.%Y")
        month_key = date_obj.strftime("%Y-%m")

        success = remove_shift(
            shifts_sheet,
            user_id=message.from_user.id,
            month_key=month_key,
            shift_date=shift_date
        )

        if success:
            bot.send_message(message.chat.id, f"🗑 Смена за {shift_date} удалена")
        else:
            bot.send_message(message.chat.id, "❌ Такой смены нет")


    @bot.message_handler(content_types=['text'])
    def handle_shift(message):
        full_name, error = parse_person(message.text)
        date_obj, date_error = parse_date(message.text)
        revenue, revenue_error = parse_revenue(message.text)


        if date_obj is None and date_error is None:
            return
        
        if date_error:
            bot.send_message(message.chat.id, f"❌ {date_error}")
            return

        if revenue_error:   
            return
        
        
        month_key = date_obj.strftime("%Y-%m")
        shift_date = date_obj.strftime("%d.%m.%Y")
        
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        
        if shift_exists(
            shifts_sheet,
            user_id=message.from_user.id,
            month_key=month_key,
            shift_date=shift_date
        ):
            bot.send_message(
                message.chat.id,
                f"⚠️ Смена за {shift_date} уже существует"
            )
            return

        add_shift(
            shifts_sheet,
            user_id=message.from_user.id,
            month_key=month_key,
            shift_date=shift_date,
            revenue=revenue
        )


        date_for_text = date_obj.strftime("%d.%m.%Y")
        bot.send_message(
            message.chat.id, 
            f"✅ 👤 {full_name} \n"
            f"✅ Смена за {date_for_text} добавлена.\n"
            f"✅ Выручка: {revenue} за день."
        )