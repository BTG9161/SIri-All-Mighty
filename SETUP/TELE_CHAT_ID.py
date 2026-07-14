import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_API_KEY")

resp = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates").json()

for u in resp['result']:
    msg = u.get('message',{})
    print(msg.get('from').get('id')) # Add the result to .env (CHAT_ID=result)

