from datetime import datetime
from services.sheets import get_or_create_worksheet 
# Гугл таблицы, Дубликат, добавления, получения, и удаления смен! 

def shift_exists(sheet, user_id: int, month_key: str, shift_date: str):
    rows = sheet.get_all_values()

    for row in rows:
        if (
            str(row[0]) == str(user_id)
            and row[1] == month_key
            and row[2] == shift_date
        ):
            return True
        
    return False
        

def add_shift(sheet, user_id: int, month_key: str, shift_date: str, revenue: float):
    created_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sheet.append_row([
        user_id,
        month_key,
        shift_date,
        revenue,
        created_dt
    ])

def get_shifts(user_id: int, month_key: str):
    sheet = get_or_create_worksheet(
        "shifts",
        headers=["user_id", "month", "date", "revenue"]
    )

    rows = sheet.get_all_values()[1:]
    shifts = []

    for row in rows:
        if int(row[0]) != user_id:
            continue
        if row[1] != month_key:
            continue

        shifts.append(row[2])

    return sorted(shifts)

def get_revenue(user_id: int, month_key: str):
    sheet = get_or_create_worksheet(
        "shifts",
        headers=["user_id", "month", "date", "revenue"]
    )
    
    rows = sheet.get_all_values()[1:]
    revenues = []

    for row in rows:
        if int(row[0]) != user_id:
            continue
        if (row[1]) != month_key:
            continue
        if not row[3]:
            continue
        
        revenues.append(float(row[3].replace(",", ".")))
    return revenues

def remove_shift(sheet, user_id: int, month_key: str, shift_date: str):
    rows = sheet.get_all_values()

    for i, row in enumerate(rows[1:], start=2):
        if (
            str(row[0]) == str(user_id)
            and row[1] == month_key
            and row[2] == shift_date
        ):
            sheet.delete_rows(i)
            return True
        
    return False