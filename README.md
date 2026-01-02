# slack-copilot

A Slack bot that integrates with GitHub Copilot CLI to provide AI-powered command suggestions and explanations directly in your Slack workspace.

## Features

- 🤖 **AI Command Suggestions**: Get command-line suggestions using GitHub Copilot
- 📚 **Command Explanations**: Understand what any command does
- 💬 **Slack Integration**: Interact via mentions or slash commands
- 🚀 **Easy Deployment**: Docker support for quick server deployment
- 🔧 **Configurable**: Environment-based configuration

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12+**
- **uv** (Python package manager): [Installation Guide](https://github.com/astral-sh/uv)
- **GitHub CLI** with Copilot extension: [Installation Guide](https://cli.github.com/)
  ```bash
  # Install GitHub CLI
  # See: https://github.com/cli/cli#installation
  
  # Install Copilot extension
  gh extension install github/gh-copilot
  ```

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/coolestowl/slack-copilot.git
cd slack-copilot
```

### 2. Set Up Slack App

1. Go to [Slack API](https://api.slack.com/apps) and create a new app
2. Enable Socket Mode in your app settings
3. Add the following Bot Token Scopes:
   - `app_mentions:read`
   - `chat:write`
   - `commands`
4. Install the app to your workspace
5. Copy the **Bot User OAuth Token** (starts with `xoxb-`)
6. Copy the **App-Level Token** (starts with `xapp-`)

### 3. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env and add your tokens
```

Update the `.env` file with your Slack tokens:
```env
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_APP_TOKEN=xapp-your-app-token-here
```

### 4. Install Dependencies

```bash
uv sync
```

### 5. Run the Bot

```bash
uv run python main.py
```

## Usage

### Mention the Bot

```
@slack-copilot how do I find large files?
@slack-copilot explain tar -xzvf file.tar.gz
```

### Use Slash Command

```
/copilot how do I list all processes?
/copilot explain docker-compose up -d
```

## Deployment

### Using Docker

1. Build the Docker image:
```bash
docker build -t slack-copilot .
```

2. Run the container:
```bash
docker run -d --name slack-copilot \
  -e SLACK_BOT_TOKEN=xoxb-your-token \
  -e SLACK_APP_TOKEN=xapp-your-token \
  slack-copilot
```

### Using Docker Compose

```bash
docker-compose up -d
```

## Project Structure

```
slack-copilot/
├── src/
│   └── slack_copilot/
│       ├── __init__.py
│       ├── bot.py          # Slack bot implementation
│       ├── config.py       # Configuration management
│       └── copilot.py      # GitHub Copilot CLI integration
├── main.py                 # Application entry point
├── pyproject.toml          # Project dependencies
├── uv.lock                 # Lock file for dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── .env.example            # Example environment variables
└── README.md               # This file
```

## Configuration

All configuration is done via environment variables:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SLACK_BOT_TOKEN` | Slack Bot User OAuth Token | - | Yes |
| `SLACK_APP_TOKEN` | Slack App-Level Token | - | Yes |
| `COPILOT_CLI_PATH` | Path to GitHub CLI executable | `gh` | No |
| `PORT` | Server port (for future use) | `3000` | No |

## Development

### Install Development Dependencies

```bash
uv sync
```

### Run in Development Mode

```bash
uv run python main.py
```

## Troubleshooting

### Bot doesn't respond
- Ensure Socket Mode is enabled in your Slack app
- Verify your tokens are correct in `.env`
- Check that the bot is invited to the channel

### "GitHub CLI not found" error
- Install GitHub CLI: https://cli.github.com/
- Install Copilot extension: `gh extension install github/gh-copilot`
- Authenticate: `gh auth login`

### Permission errors
- Ensure your Slack app has the required scopes
- Reinstall the app to your workspace if you added new scopes

## License

See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
