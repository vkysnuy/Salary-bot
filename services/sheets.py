import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv

load_dotenv()


SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_CREDENTIALS_PATH")

if not SERVICE_ACCOUNT_FILE:
    raise RuntimeError("❌ GOOGLE_CREDENTIALS_PATH не задан в .env")
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

client = gspread.authorize(creds)


spreadsheet = client.open("bot_tg")


def get_or_create_worksheet(title, headers):
    try:
        ws = spreadsheet.worksheet(title)
    except:
        ws = spreadsheet.add_worksheet(
            title=title,
            rows=1000,
            cols=len(headers)
        )
        ws.append_row(headers)
    return ws
