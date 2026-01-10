import re 
from datetime import datetime


def parse_person(text):
    match = re.search(r"👤\s*([А-Яа-яІіЇїЄєҐґ'’\-]+\s+[А-Яа-яІіЇїЄєҐґ'’\-]+)", text)
    if not match:
        return None, "Имя и фамилия не найдены"

    full_name = match.group(1).strip()
    return full_name, None


def valid_date(data_str):
    try:
        datetime.strptime(data_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False

#Парсер даты
def parse_date(text):
    match = re.search(r"(\d{1,2}\.\d{1,2}\.\d{4})", text)
    if not match:
        return None, None
    
    date_str = match.group(1)

    #даты ли существует?
    try:
        date_obj = datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        return None, f"Неверная дата: {date_str}"
    
    return date_obj, None

#Парсер виручки
def parse_revenue(text):
    match = re.search(r"Виручка:\s*([\d\.]+)", text)
    if not match:
        return None, "Виручка не найдена"

    try:
        revenue = float(match.group(1))
        return revenue, None
    except ValueError:
        return None, "Неверный формат выручки"
    
    