# Siri All-Mighty

A personal DIY voice/chat assistant powered by **Groq** (reasoning) and **ElevenLabs** (voice).

## The project has two parts:

### With TUI:
siriApp.py:
- **Voice command** — This doesn't fully support voice input, and you may encounter errors.
- **Normal input** — This includes multiline pormpts.

Telegram bot (`telebot.py`):
- A tool-calling agent you can text or voice-message from your phone using Telegram.

### Without TUI:
- This is the older version of Siri All-Mighty which doesn't include any UI, just simple terminal.
- The version of the build is 0.1.1, you can find the source code, or the zip file in releases.
- **Voice assistant** (`Siri2.py`) — the original, mic + keyboard input, spoken replies, also includes multiline prompts.  

## Requirements
- yt-dlp for playing songs.
- macOS (uses `afplay` + `pyobjc` for the CLI version) for the older build.
- Groq + ElevenLabs API keys (Telegram bot only needs Groq).
- Telegram bot token + your chat ID, for the Telegram bot, use BotFather.

## What can it do
- It can use the terminal to do almost anything, so you should use it wisely.
- Siri can also play songs if you have the correct setup for yt-dlp.
- Siri can also do websearch
- It can return responses in **Markdown**.
- Siri can accept written input, but you should remember to press `ctrl+alt(or option)` after writing, for older build.
- It can also accept spoken input through `ctrl+shift`, for older build.
- You can also use it through Telegram(it also takes spoken input).
- There is also a command for adding chat IDs in Telegram through /approve pass ID.
- It can also store memories, but it is a work-in-progress.

## How it works
- It uses Groq’s LLMs to generate output through APIs, and uses ElevenLabs to convert Groq’s output to speech (speech is in the older build).
- The memory is stored on your device, in JSON format, along with the tool calls.
- All the environment variables are stored in .env, but you can also store them temporarily for a single session using export.

## Setup
```bash
git clone https://github.com/BTG9161/SIri-All-Mighty.git
cd SIri-All-Mighty
uv sync
./install.sh
```
`./install` makes you a global script for restoring sessions, for older build.
If you don't have `uv`, copy the dependencies from `pyproject.toml` into a `requirements.txt`, and then- `pip install -r requirements.txt` instead.

Create a `.env`:
```
GROQ_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
TELEGRAM_API_KEY=your_telegram_bot_token
PASS=secret_password
CHAT_IDS=comma,separated,allowed,chat,ids
DIR=path/to/your/sandbox
```
- It is recommended that you set up your DIR as a sandbox, you could choose not to.
Or set these as environment variables directly in your shell instead of using `.env`.
- PASS is the password for telegram approving IDs authentication

## Usage

**TUI:**
```bash
uv siriApp.py
```

**Telegram bot:**
```bash
uv telebot.py
```
- Only chat IDs listed in `CHAT_IDS`, in .env(or enviornment vars), are allowed to talk to the bot.
- Or you can download the binaries(Siri2-macOS.zip and telebot-macOS.zip), and unzip them before executing.
- Don’t forget to make it executable ```chmod +x Siri2-macOS```.

**MCP server** (terminal/file/memory tools):
```bash
uv functions/mcp_server.py
```

## Note(s)
- `Siri.py` is not the main file — kept because...why not!?, no real use.
- You may change Siri.py for your system, because i won't.
- `SETUP/` holds a helper script for finding your Telegram chat ID.
- Don't use it if you don't trust it, it has terminl access. Or you can remove it by running 
```rm functions/terminal_access.py```
along with editing mcp_tools_creation.py and execute_tool_call.py.

## Agent in action
<img width="1422" height="802" alt="screenshot-2026-10-04_23-21-48" src="https://github.com/user-attachments/assets/5a50b414-a260-4b99-bcac-139f07da886e" />
<img width="1142" height="884" alt="Screenshot 2026-08-10 at 11 18 35 PM" src="https://github.com/user-attachments/assets/4695f355-185e-4073-96f8-2732b0473754" />
<img width="1440" height="900" alt="Screenshot 2026-07-24 at 10 03 13 PM" src="https://github.com/user-attachments/assets/90dcdfae-8b42-4625-a51c-46d2587e9cac" />
### For older build:
<img width="661" height="692" alt="Screenshot 2026-08-03 at 10 36 03 PM" src="https://github.com/user-attachments/assets/c31d4d90-103c-448b-aa6d-e540ef5727d9" />

