import os
from pathlib import Path
from telegram import Update
from dotenv import load_dotenv
from telegram.ext import ContextTypes
from functions.sessions import store_session
from telefunc.telebot_wrapper import command

load_dotenv()

DIR = os.getenv("DIR")
USER_MEMORY_FILE = Path(DIR, "current_session.json").resolve()

@command("store_session")
async def store_tele_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    store_session(USER_MEMORY_FILE)
    await update.message.reply_text("Session stored.")

