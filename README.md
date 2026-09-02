# Siri All-Mighty

A personal DIY voice/chat assistant powered by **Groq** (reasoning) and **ElevenLabs** (voice).

The project includes:
- **Voice assistant** (`Siri2.py`) — the original, mic + keyboard input, spoken replies.
- **Telegram bot** (`telebot.py`) — a tool-calling agent you can text or voice-message from your phone.

## Requirements
- macOS (uses `afplay` + `pyobjc` for the CLI version)
- Groq + ElevenLabs API keys (Telegram bot only needs Groq)
- Telegram bot token + your chat ID, for the Telegram bot, use BotFather

## What can it do
- Siri can accept written input, but you should remember to press `ctrl+alt(or option)` after writing.
- It can also accept spoken input through `ctrl+shift`.
- You can also use it through telegram(it also takes spoken input).
- It can also store memories, but it is a work-in-progress.

## How it works
- It uses Groq’s LLMs to generate output through APIs, and uses ElevenLabs to convert Groq’s output to speech.
- The memory is stored on your device, in JSON format, along with the tool calls.
- All the environment variables are stored in .env, but you can also store them temporarily for a single session using export).

## Setup
```bash
git clone https://github.com/BTG9161/SIri-All-Mighty.git
cd SIri-All-Mighty
uv sync
./install.sh
```
`./install` makes you a global script for restoring sessions.
If you don't have `uv`, copy the dependencies from `pyproject.toml` into a `requirements.txt`, and then- `pip install -r requirements.txt` instead.

Create a `.env`:
```
GROQ_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
TELEGRAM_API_KEY=your_telegram_bot_token
CHAT_IDS=comma,separated,allowed,chat,ids
DIR=path/to/your/sandbox
```
- It is recommended that you set up your DIR. Howevet, */Siri is hardcoded.
Or set these as environment variables directly in your shell instead of using `.env`.

## Usage

**Voice assistant:**
```bash
python Siri2.py
```

**Telegram bot:**
```bash
python telebot.py
```
- Only chat IDs listed in `CHAT_IDS`, in .env(or enviornment vars), are allowed to talk to the bot.
- Or you can download the binaries(Siri2-macOS.zip and telebot-macOS.zip), and unzip them before executing.
- Don’t forget to make it executable ```chmod +x Siri2-macOS```.

**MCP server** (terminal/file/memory tools):
```bash
python functions/mcp_server.py
```

## Note(s)
- `Siri.py` is not the main file — kept because...why not!?, no real use.
- You may change Siri.py for your system, because i won't.
- `SETUP/` holds a helper script for finding your Telegram chat ID.
- Don't use it if you don't trust it, it has terminl access. Or you can remove it by running 
```rm functions/terminal_access.py```

## For Hack Club reviewers
- AI was used as a coding assistant throughout: debugging the dual-input threading logic, writing boilerplate for the Groq/ElevenLabs/Telegram API calls, building the MCP terminal server, and helping draft this README (just ideas for what to write). The architecture and features(not bugs!) were made by me.
- There are some features that aren't covered in the READEME, like siriApp.py, please ignore, for the review the siri2.py will not be edited as required by siriApp.py, i commited the new features by mistake, so it might not work on terminal. 
- PLEASE review my project, i used Claude for making the binaries as there were problems and i was clueless, sorry.

## Agent in action
<img width="661" height="692" alt="Screenshot 2026-08-03 at 10 36 03 PM" src="https://github.com/user-attachments/assets/c31d4d90-103c-448b-aa6d-e540ef5727d9" />
<img width="1142" height="884" alt="Screenshot 2026-08-10 at 11 18 35 PM" src="https://github.com/user-attachments/assets/4695f355-185e-4073-96f8-2732b0473754" />
<img width="1440" height="900" alt="Screenshot 2026-07-24 at 10 03 13 PM" src="https://github.com/user-attachments/assets/90dcdfae-8b42-4625-a51c-46d2587e9cac" />

