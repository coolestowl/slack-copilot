# slack-copilot

A Slack bot that integrates with GitHub Copilot CLI in REPL mode for interactive AI-powered assistance.

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Configure environment variables in `.env`:
```env
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
COPILOT_CLI_PATH=copilot
```

3. Run the bot:
```bash
uv run python main.py
```

## Usage

Mention the bot in Slack or use the `/copilot` command. The bot will start a Copilot REPL session and stream responses back to Slack in real-time.
