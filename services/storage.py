shift_storage = {} # хранилище
month_settings_storage = {}
user_state = {}




def add_shift(user_id, date_obj, revenue):
    month_key = date_obj.strftime("%Y-%m")
    data_key = date_obj.strftime("%d.%m.%Y")

    # если нет пользователя -> создать
    if user_id not in shift_storage:
        shift_storage[user_id] = {}
    # если ключ месяца нету у данного пользователя -> создать
    if month_key not in shift_storage[user_id]:
        shift_storage[user_id][month_key] = {}

    shift_storage[user_id][month_key][data_key] = revenue

def get_user_shift(user_id, month_key):
    return shift_storage.get(user_id, {}).get(month_key, {})

def remove_shift(user_id, date_obj):
    month_key = date_obj.strftime("%Y-%m")
    date_key = date_obj.strftime("%d.%m.%Y")

    if user_id not in shift_storage:
        return False
    
    if month_key not in shift_storage[user_id]:
        return False
    
    if date_key not in shift_storage[user_id][month_key]:
        return False
    
    del shift_storage[user_id][month_key][date_key]
    return True

def get_mouth_setting(user_id, month_key):
    if user_id not in month_settings_storage:
        month_settings_storage[user_id] = {}

    if month_key not in month_settings_storage[user_id]:
        month_settings_storage[user_id][month_key] = {
            "category": None,
            "plan_percent": None,
            "penalties": []
        }
    
    return month_settings_storage[user_id][month_key]
    