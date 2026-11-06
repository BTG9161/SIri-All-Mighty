import os
from pathlib import Path
from telegram import Update
from dotenv import load_dotenv
from telegram.ext import ContextTypes
from telefunc.telebot_wrapper import command

load_dotenv()

env = Path(".env")
env_text = env.read_text()
ALLOWED_CHAT_IDS = [int(x) for x in os.getenv("CHAT_IDS").split(",")]
PASS = os.getenv("PASS")

@command("approve")
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global env_text, env
    
    if context.args[0] == PASS:
        env_text = env_text.replace("CHAT_IDS=",
                         f"CHAT_IDS= {int(context.args[1])}, ", 1)

        env.write_text(env_text)
        ALLOWED_CHAT_IDS.append(int(context.args[1]))
        await update.message.reply_text("You've got it!")
