# Siri All-Mighty

A personal DIY voice/chat assistant powered by **Groq** (reasoning) and **ElevenLabs** (voice).

The project includes:
- **Voice assistant** (`Siri2.py`) — the original, mic + keyboard input, spoken replies.
- **Telegram bot** (`telebot.py`) — a tool-calling agent you can text or voice-message from your phone.

## What it does
- Accepts typed and spoken input — `ctrl+shift` to speak, press `ctrl+alt(or option)` after hitting enter for the response.
- Sends prompts to Groq (`openai/gpt-oss-120b`), with tool/function calling.
- Voice notes are transcribed by Whisper (`whisper-large-v3-turbo`).
- Say **"delete"** to clear the memory file, **"bye"** to exit.

## Setup
```bash
git clone https://github.com/BTG9161/SIri-All-Mighty.git
cd SIri-All-Mighty
uv sync
```
If you don't have `uv`, copy the dependencies from `pyproject.toml` into a `requirements.txt`, and then- `pip install -r requirements.txt` instead.

Create a `.env`:
```
GROQ_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
TELEGRAM_API_KEY=your_telegram_bot_token
CHAT_IDS=comma,separated,allowed,chat,ids
DIR=path/to/save/incoming/voice/notes
```
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
Only chat IDs listed in `CHAT_IDS`, in .env(or enviornment vars), are allowed to talk to the bot.

**MCP server** (terminal/file/memory tools):
```bash
python functions/mcp_server.py
```

## Requirements
- macOS (uses `afplay` + `pyobjc` for the CLI version)
- Groq + ElevenLabs API keys (Telegram bot only needs Groq)
- Telegram bot token + your chat ID, for the Telegram bot

## Note(s)
- `Siri.py` is not the main file — kept because...why not!?, no real use.
- You may change Siri.py for your system, because i won't.
- `SETUP/` holds a helper script for finding your Telegram chat ID.
- Don't use it if you don't trust it, it has terminl access.

## For Hack Club reviewers
- AI was used as a coding assistant throughout: debugging the dual-input threading logic, writing boilerplate for the Groq/ElevenLabs/Telegram API calls, building the MCP terminal server, and helping draft this README (just ideas for what to write). The architecture and features(not bugs!) were made by me.
