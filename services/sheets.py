import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv
import json

load_dotenv()

creds_raw = os.getenv("GOOGLE_CREDENTIALS_PATH")

if not creds_raw:
    raise RuntimeError("❌ GOOGLE_CREDENTIALS_PATH не задан в .env")


try:
    if creds_raw.endswith('.json'):
        creds_dict = json.load(open(creds_raw))
    else:
        creds_dict = json.loads(creds_raw)
except Exception as e:
    raise RuntimeError(f"❌ Ошибка загрузки Google ключей: {e}")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    creds_dict,
    scopes=SCOPES
)

client = gspread.authorize(creds)

spreadsheet = client.open("bot_tg")

def get_or_create_worksheet(title, headers):
    try:
        ws = spreadsheet.worksheet(title)
    except gspread.exceptions.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(
            title=title,
            rows=1000,
            cols=len(headers)
        )
        ws.append_row(headers)
    return ws