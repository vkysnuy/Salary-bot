from datetime import datetime
from services.sheets import get_or_create_worksheet

def add_penalty(user_id: int, month_key: str, reason: str, amount: int):
    sheet = get_or_create_worksheet(
        "penalties",
        headers=["user_id", "month", "date", "reason", "amount"]
    )

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    sheet.append_row([
        user_id,
        month_key,
        date_str,
        reason,
        amount
    ])

def get_penalties(user_id: int, month_key: str):
    sheet = get_or_create_worksheet(
        "penalties",
        headers=["user_id", "month", "date", "reason", "amount"]
    )

    rows = sheet.get_all_values()[1:]
    result = []

    for row in rows:
        if int(row[0]) == user_id and row[1] == month_key:
            result.append({
                "date": row[2],
                "reason": row[3],
                "amount": int(row[4]) if row[4] else 0
            })

    return result



def remove_penalty(sheet, user_id: int, month_key: str, reason: str):
    rows = sheet.get_all_values()
    
    for i in range(len(rows) - 1, 0, -1):  # с конца
        row = rows[i]
        if (
            int(row[0]) == user_id
            and row[1] == month_key
            and row[3] == reason
        ):
            sheet.delete_rows(i + 1)
            return True

    return False
