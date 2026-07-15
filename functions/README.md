# Siri All-Mighty

A personal DIY voice/chat assistant powered by **Groq** (reasoning) and **ElevenLabs** (voice). Since it uses cloud APIs instead of a local model, it runs well on **older or less powerful computers** — like the one this was built on.

The project has two faces now:
- **CLI voice assistant** (`Siri2.py`) — the original, mic + keyboard input, spoken replies.
- **Telegram bot** (`telebot.py`) — a tool-calling agent you can text or voice-message from your phone.

## What it does
- Accepts typed and spoken input — `ctrl+shift` to speak, `ctrl+alt`/`option` to type (both **after** pressing enter) in the CLI version.
- Sends prompts to Groq (`openai/gpt-oss-120b`), with tool/function calling and automatic retry on rate limits.
- Speaks replies via ElevenLabs (CLI version).
- Telegram bot transcribes voice notes with Whisper (`whisper-large-v3-turbo`) and replies as text.
- Persists conversation memory to `siri_memory.json` (say **"delete"** to clear it, **"bye"** to exit the CLI).
- Ships a standalone MCP server (`functions/mcp_server.py`) exposing terminal access, file read/write/delete, and a simple markdown-based memory store (`MEMORY.md`) — usable by any MCP-compatible client, including Claude.
- `-v` / `--verbose` flag for token usage logging (CLI).

## Setup
```bash
git clone https://github.com/BTG9161/SIri-All-Mighty.git
cd SIri-All-Mighty
uv sync
```
If you don't have `uv`, copy the dependencies from `pyproject.toml` into a `requirements.txt` and `pip install -r requirements.txt` instead.

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

**CLI voice assistant:**
```bash
python Siri2.py
```

**Telegram bot:**
```bash
python telebot.py
```
Only chat IDs listed in `CHAT_IDS` are allowed to talk to the bot.

**MCP server** (terminal/file/memory tools, standalone):
```bash
python functions/mcp_server.py
```

## Requirements
- macOS (uses `afplay` + `pyobjc` for the CLI version)
- Groq + ElevenLabs API keys (Telegram bot only needs Groq)
- A Telegram bot token + your chat ID, for the Telegram bot
- Microphone for speech input (CLI)
- No GPU/local model needed — designed for modest hardware

## Status
Active personal project, still evolving — expect rough edges. Currently working on persistent long-term memory via mem0 (hit some dependency snags on Intel macOS — torch/fastembed version mismatches — with OpenAI embeddings as the likely fallback).

## Note(s)
- `Siri.py` is not the main file — kept around for sentimental reasons, no real use.
- Feel free to adapt `Siri2.py` for other platforms; not a priority here.
- `SETUP/` holds a helper script for finding your Telegram chat ID.

## For Hack Club reviewers
- AI (Claude) was used as a coding assistant throughout: debugging the dual-input threading logic, writing boilerplate for the Groq/ElevenLabs/Telegram API calls, building the MCP terminal server, and helping draft this README. The core architecture, feature decisions, and all the debugging of actual hardware/API issues were mine.
