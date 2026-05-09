# Local LLM Tools


A tiny local-first news summarizer that fetches headlines from free RSS feeds and summarizes them using Ollama.

## Setup

1. Install Python 3.11+
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install Ollama and a local model:

```bash
ollama pull qwen2.5:3b
```

Optional: use `llama3:8b` by setting:

```bash
export OLLAMA_MODEL=llama3:8b
```

## Run

```bash
python main.py
```

## What it does

- Fetches recent news from RSS feeds (BBC, Reuters, Hacker News, TechCrunch)
- Prints top headlines
- Sends the articles to a local Ollama model
- Prints a concise briefing with themes and bullet points

## Notes

- No external APIs, databases, or agents frameworks
- Uses only `requests`, `feedparser`, and the local Ollama CLI
