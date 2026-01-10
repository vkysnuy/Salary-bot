from services.sheets import get_or_create_worksheet

month_settings_sheet = get_or_create_worksheet(
    "month_setting",
    ["user_id", "month", "plan", "category"]    
)

# План, категория
def get_month_setting(user_id: int, month_key: str):
    sheet = get_or_create_worksheet(
        "month_setting",
        headers=["user_id", "month", "plan", "category"]
    )
    rows = sheet.get_all_values()[1:]

    for row in rows:
        if int(row[0]) == user_id and row[1] == month_key:
            return{
                "plan": int(float(row[2].replace(",", "."))) if row[2] else None,
                "category": int(row[3]) if row[3] else 3
            }
        
    return {
        "plan": None,
        "category": 3
                }

def get_or_create_month_row(sheet, user_id, month_key):
    rows = sheet.get_all_values()[1:]

    for i, row in enumerate(rows, start=2):
        if row[0] == str(user_id) and row[1] == month_key:
            return i  # номер строки

    sheet.append_row([user_id, month_key, "", ""])
    return len(rows) + 2


def set_plan (sheet, user_id, month_key, plan):
    rows = get_or_create_month_row(sheet, user_id, month_key)
    sheet.update_cell(rows, 3, plan)

    

def set_category(sheet, user_id, month_key, category):
    rows = get_or_create_month_row(sheet, user_id, month_key)
    sheet.update_cell(rows, 4, category)

