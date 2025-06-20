# Loud Hawk News API

This project provides a minimal FastAPI service that rewrites news articles in a casual, Gen&nbsp;Z WhatsApp style using OpenAI's ChatGPT.

## Requirements

- Python 3.11+
- An OpenAI API key available as the `OPENAI_API_KEY` environment variable.

## Setup

Install dependencies and run the server locally:

```bash
pip install -r requirements.txt
uvicorn app.main:app
```

The server will start on `http://127.0.0.1:8000`.

## Testing `/edit`

Send a `POST` request to `/edit` with a JSON payload like the one below:

```json
{
  "title": "Loud Hawk Launches New App",
  "date": "2025-06-20",
  "body": "The team behind Loud Hawk just released a new app to help you stay in the loop with the latest hawk-related news.",
  "link": "https://example.com/loud-hawk-launch"
}
```

The endpoint will return the rewritten news text wrapped in a formatted message.
