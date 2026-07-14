import os
import json
from groq import Groq
import logging
import asyncio
from functions.agent_call import agent_call, final_call
from functions.execute_tool_call import execute_tool_call
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import(
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

load_dotenv()
logging.basicConfig(level=logging.INFO)

VOICE_PATH = os.getenv("DIR")
BOT_TOKEN = os.getenv("TELEGRAM_API_KEY")
USER_MEMORY_FILE = "siri_memory.json"
ALLOWED_CHAT_IDS = [int(x) for x in os.getenv("CHAT_IDS").split(",")]
API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is up. Send me a message.")


async def handle_prompt(update: Update, prompt: str) -> str:
    loop = asyncio.get_running_loop()

    if prompt.lower() == "delete" and os.path.exists(USER_MEMORY_FILE):
        os.remove(USER_MEMORY_FILE)
        print("Memory file deleted!")
        await update.message.reply_text("Memory file deleted!")
        return
    elif prompt.lower() == "delete" and not os.path.exists(USER_MEMORY_FILE):
        await update.message.reply_text("You haven't even started...")
        return

    if os.path.exists(USER_MEMORY_FILE):
        with open(USER_MEMORY_FILE, "r") as f:
            user_messages = json.load(f)
    else:
        # First run: define system prompts
        with open("system_prompt.txt") as f:
            user_system_prompt = f.read()
        
        # Initialize conversation with system prompt
        user_messages = [
        {"role": "system", "content": user_system_prompt},
        ]
    
    user_messages.append({"role": "user", "content": prompt})
    with open(USER_MEMORY_FILE, "w") as f:
            json.dump(user_messages, f, indent=2)

    response = await loop.run_in_executor(None, agent_call, user_messages)

    Response = response.choices[0].message.content

    if response.choices[0].message.tool_calls:
        # Execute each tool call (using the helper function from step 2)
        for tool_call in response.choices[0].message.tool_calls:
            function_response = await loop.run_in_executor(None, execute_tool_call, tool_call)
            
            # Add tool result to messages
            user_messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.function.name,
                "content": str(function_response)
            })
    
        # Send results back and get final response
        final_response = await loop.run_in_executor(None, final_call, user_messages)
        final_Response = final_response.choices[0].message.content

        user_messages.append({"role": "assistant", "content": final_Response})

        reply = final_Response
        
        with open(USER_MEMORY_FILE, "w") as f:
            json.dump(user_messages, f, indent=2)
    
    else:
        reply = Response
        # Save model response into memory as assistant message (planning stage)

        user_messages.append({"role": "assistant", "content": Response})
        with open(USER_MEMORY_FILE, "w") as f:
            json.dump(user_messages, f, indent=2)

    await update.message.reply_text(reply)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id not in ALLOWED_CHAT_IDS:
        return

    prompt = update.message.text
    print(f"Got: {prompt}")
    
    await handle_prompt(update, prompt)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id not in ALLOWED_CHAT_IDS:
        return
    voice_file = await update.message.voice.get_file()
    
    await voice_file.download_to_drive(VOICE_PATH)

    with open(VOICE_PATH, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=("audio.ogg", file.read()),
            model="whisper-large-v3-turbo",
        )
    prompt = transcription.text

    print(f"Got: {prompt}")

    await handle_prompt(update, prompt)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handlers([CommandHandler("start", start),
                      MessageHandler(filters.TEXT & ~ filters.COMMAND, handle_text),
                      MessageHandler(filters.VOICE, handle_voice)])

    print("Bot running... Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()

