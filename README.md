# Siri All-Mighty 🎙️

A personal DIY voice assistant powered by **Groq** (reasoning) and **ElevenLabs** (voice). Since it uses cloud APIs instead of a local model, it runs well on **older or less powerful computers**.
Actually it is for **older or less powerful computers** because my mac is an **older and less powerful computer**

## What it does
- Accepts typed and spoken input (The merger is Work In Progress but, they work(in a way))
- Sends prompts to Groq, supports tool/function calling
- Speaks replies via ElevenLabs
- Persists conversation memory to `siri_memory.json`
- Say **"delete"** to clear memory, **"bye"** to exit
- `-v` / `--verbose` flag for token usage logging

## Setup
```bash
git clone https://github.com/BTG9161/SIri-All-Mighty.git
cd SIri-All-Mighty
uv sync
```
If you don't have uv, you could copy the project.toml libs to a .txt file and download from there (pip install -r requirements.txt)

Create a `.env`:
```
GROQ_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
```

Or you could make enviornment vars in terminal

## Usage
```bash
python Siri2.py
```

## Requirements
- macOS (uses `afplay` + `pyobjc`)
- Groq + ElevenLabs API keys
- Microphone for speech input
- No GPU/local model needed — designed for modest hardware

## Status
Active personal project, still evolving — expect rough edges.

## Note(s)
- The Siri.py is not the main file, actually it is just there because i want it and has no real use.
- You could change the Siri2.py for other platforms, because i don't want to do it.

## For Hack Club reviewers
- AI (Claude) was used as a coding assistant throughout: debugging the dual-input threading logic, writing boilerplate for the Groq/ElevenLabs API calls, and helping draft this README. The core architecture, feature decisions, and all the debugging of actual hardware/API issues were mine.

