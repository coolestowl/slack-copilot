# Quick Start Guide

Get your Slack Copilot bot up and running in 5 minutes!

## Prerequisites Checklist

Before starting, make sure you have:

- [ ] Python 3.12 or higher installed
- [ ] GitHub account with Copilot access
- [ ] Slack workspace admin access

## Step 1: Install System Dependencies (5 minutes)

### Install Python 3.12+

```bash
# Check your Python version
python3 --version

# If you need to install Python 3.12:
# Ubuntu/Debian:
sudo apt update
sudo apt install python3.12 python3.12-venv

# macOS (with Homebrew):
brew install python@3.12
```

### Install uv

```bash
pip install uv
```

### Install GitHub Copilot CLI

```bash
# Install GitHub Copilot CLI
# Visit: https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line

# Verify installation
copilot --version

# Authenticate on first use (follow the prompts)
copilot suggest "test command"
```

## Step 2: Create Slack App (5 minutes)

1. **Go to Slack API**: https://api.slack.com/apps

2. **Create New App**:
   - Click "Create New App"
   - Choose "From scratch"
   - Name: "Copilot Bot" (or your choice)
   - Select your workspace

3. **Enable Socket Mode**:
   - Go to "Socket Mode" in the left sidebar
   - Toggle "Enable Socket Mode" to ON
   - Create an app-level token with `connections:write` scope
   - Copy the **App Token** (starts with `xapp-`)

4. **Add Bot Scopes**:
   - Go to "OAuth & Permissions"
   - Under "Bot Token Scopes", add:
     - `app_mentions:read`
     - `chat:write`
     - `commands`

5. **Create Slash Command** (Optional):
   - Go to "Slash Commands"
   - Click "Create New Command"
   - Command: `/copilot`
   - Description: "Ask GitHub Copilot for help"
   - Usage hint: "your question here"

6. **Enable Events**:
   - Go to "Event Subscriptions"
   - Toggle "Enable Events" to ON
   - Under "Subscribe to bot events", add:
     - `app_mention`
     - `message.channels`

7. **Install App**:
   - Go to "Install App"
   - Click "Install to Workspace"
   - Copy the **Bot Token** (starts with `xoxb-`)

## Step 3: Set Up the Bot (2 minutes)

```bash
# Clone the repository
git clone https://github.com/coolestowl/slack-copilot.git
cd slack-copilot

# Run the setup script (automated)
./setup.sh

# OR manually:
# 1. Install dependencies
uv sync

# 2. Configure environment
cp .env.example .env
nano .env  # Add your tokens
```

Your `.env` should look like:
```env
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_APP_TOKEN=xapp-your-app-token-here
COPILOT_CLI_PATH=gh
PORT=3000
```

## Step 4: Run the Bot (1 minute)

```bash
# Run directly
uv run python main.py

# OR with make
make run
```

You should see:
```
INFO - 🚀 Slack Copilot Bot is starting...
INFO - Bot connected to Slack
```

## Step 5: Test in Slack (1 minute)

1. **Invite the bot to a channel**:
   ```
   /invite @copilot-bot
   ```

2. **Test with a mention**:
   ```
   @copilot-bot how do I list all files?
   ```

3. **Test the slash command**:
   ```
   /copilot how do I check disk space?
   ```

4. **Test command explanation**:
   ```
   @copilot-bot explain tar -xzvf file.tar.gz
   ```

## Production Deployment

### Option A: Docker (Recommended)

```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

### Option B: Systemd Service

```bash
# Copy service file
sudo cp slack-copilot.service /etc/systemd/system/

# Edit the service file with your paths
sudo nano /etc/systemd/system/slack-copilot.service

# Enable and start
sudo systemctl enable slack-copilot
sudo systemctl start slack-copilot
sudo systemctl status slack-copilot
```

## Troubleshooting

### Bot doesn't respond

**Check 1**: Is the bot running?
```bash
# If running directly:
# Check the terminal output

# If using Docker:
docker-compose ps

# If using systemd:
sudo systemctl status slack-copilot
```

**Check 2**: Are tokens correct?
```bash
# Verify .env file has correct tokens
cat .env | grep TOKEN
```

**Check 3**: Is Copilot CLI authenticated?
```bash
copilot --version
```

### "Copilot CLI not found" error

```bash
# Install GitHub Copilot CLI
# Visit: https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line

# Verify installation
copilot --version

# Authenticate on first use
copilot suggest "test command"
```

### Permission errors in Slack

1. Go to your Slack App settings
2. Check "OAuth & Permissions" > "Bot Token Scopes"
3. Ensure all required scopes are added
4. Reinstall the app to workspace

## Common Commands

```bash
# Development
make install      # Install dependencies
make run         # Run the bot
make clean       # Clean temporary files

# Docker
make build       # Build Docker image
make docker-run  # Run with Docker Compose
make docker-logs # View logs

# Systemd
sudo systemctl start slack-copilot    # Start
sudo systemctl stop slack-copilot     # Stop
sudo systemctl restart slack-copilot  # Restart
sudo systemctl status slack-copilot   # Check status
sudo journalctl -u slack-copilot -f   # View logs
```

## Next Steps

- Read [USAGE.md](USAGE.md) for detailed usage examples
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Getting Help

- 📖 Check the documentation
- 🐛 Open an issue: https://github.com/coolestowl/slack-copilot/issues
- 💬 Ask in discussions

---

**Congratulations! Your Slack Copilot bot is ready! 🎉**
