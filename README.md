# Game Calendar Bot

Telegram bot for tabletop game players — provides a shared session calendar and dice roller.

## Features

| Command  | Description                                                                 |
|----------|-----------------------------------------------------------------------------|
| `/date`  | Opens a game calendar. In private chat — opens as a Web App (inline). In groups — opens in browser. |
| `/dice`  | Rolls dice (e.g. d6, d20, d100) via inline keyboard buttons.                |

## How It Works

1. The bot runs as a long-polling Telegram bot using [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).
2. On startup it registers `/date` and `/dice` commands with Telegram.
3. The calendar is hosted externally on GitHub Pages and loaded inside Telegram via a [WebApp](https://core.telegram.org/bots/webapps) or a direct link.
4. Dice rolls are generated server-side with Python's `random.randint(1, N)` and logged to stdout.

## Quick Start

### Prerequisites

- Docker installed and running
- A Telegram Bot Token (get one from [@BotFather](https://t.me/BotFather))

### Setup

1. **Clone or download** this repository.

2. **Create `.env`** file from the example:
   ```bash
   cp .env.example .env
   ```

3. **Fill in your bot token** in `.env`:
   ```
   BOT_TOKEN=123456789:ABCdef...
   ```

### Run with Docker

```bash
# Build the image
docker build -t game-calendar-bot .

# Run the container
docker run --env-file .env game-calendar-bot
```

### Run locally (without Docker)

```bash
pip install -r requirements.txt
export BOT_TOKEN="your-token-here"
python bot.py
```

## Project Structure

```
game-calendar-bot/
├── bot.py             # Main bot logic
├── Dockerfile         # Container configuration
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variables template
└── QWEN.md            # Project context (for AI tooling)
```

## Obtaining a Bot Token

1. Open Telegram and search for **@BotFather**.
2. Send `/newbot` and follow the instructions.
3. Copy the token you receive and paste it into the `.env` file.
