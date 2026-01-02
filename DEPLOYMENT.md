# Deployment Guide

This guide provides instructions for deploying the Slack Copilot bot to a production server.

## Prerequisites

- A Linux server (Ubuntu 20.04+ recommended)
- Docker and Docker Compose installed
- GitHub CLI installed and authenticated
- Slack Bot tokens

## Deployment Options

### Option 1: Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/coolestowl/slack-copilot.git
cd slack-copilot
```

2. Copy and configure environment variables:
```bash
cp .env.example .env
# Edit .env with your tokens
nano .env
```

3. Authenticate GitHub CLI (for Copilot access):
```bash
gh auth login
gh extension install github/gh-copilot
```

4. Build and run:
```bash
docker-compose up -d
```

5. Check logs:
```bash
docker-compose logs -f
```

### Option 2: Systemd Service (Direct Installation)

1. Install dependencies:
```bash
# Install Python 3.12
sudo apt update
sudo apt install python3.12 python3.12-venv

# Install uv
pip install uv

# Install GitHub CLI
sudo apt install gh
gh auth login
gh extension install github/gh-copilot
```

2. Clone and setup:
```bash
cd /opt
sudo git clone https://github.com/coolestowl/slack-copilot.git
cd slack-copilot
sudo uv sync
```

3. Configure environment:
```bash
sudo cp .env.example .env
sudo nano .env  # Add your tokens
```

4. Create systemd service:
```bash
sudo nano /etc/systemd/system/slack-copilot.service
```

Add the following content:
```ini
[Unit]
Description=Slack Copilot Bot
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/opt/slack-copilot
Environment="PATH=/opt/slack-copilot/.venv/bin:/usr/local/bin:/usr/bin:/bin"
EnvironmentFile=/opt/slack-copilot/.env
ExecStart=/usr/local/bin/uv run python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

5. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable slack-copilot
sudo systemctl start slack-copilot
sudo systemctl status slack-copilot
```

6. View logs:
```bash
sudo journalctl -u slack-copilot -f
```

## Monitoring

### Docker
```bash
# View logs
docker-compose logs -f slack-copilot

# Restart service
docker-compose restart slack-copilot

# Stop service
docker-compose stop slack-copilot
```

### Systemd
```bash
# View logs
sudo journalctl -u slack-copilot -f

# Restart service
sudo systemctl restart slack-copilot

# Stop service
sudo systemctl stop slack-copilot

# Check status
sudo systemctl status slack-copilot
```

## Troubleshooting

### Bot doesn't respond
1. Check if the service is running:
   - Docker: `docker-compose ps`
   - Systemd: `sudo systemctl status slack-copilot`

2. Check logs for errors:
   - Docker: `docker-compose logs slack-copilot`
   - Systemd: `sudo journalctl -u slack-copilot -n 50`

3. Verify environment variables are set correctly

4. Ensure GitHub CLI is authenticated:
   ```bash
   gh auth status
   ```

### GitHub Copilot not working
1. Ensure GitHub CLI is installed and authenticated
2. Check if Copilot extension is installed:
   ```bash
   gh extension list
   ```
3. Install if missing:
   ```bash
   gh extension install github/gh-copilot
   ```

## Updating

### Docker
```bash
cd /path/to/slack-copilot
git pull
docker-compose down
docker-compose build
docker-compose up -d
```

### Systemd
```bash
cd /opt/slack-copilot
sudo git pull
sudo uv sync
sudo systemctl restart slack-copilot
```

## Security Best Practices

1. **Use environment variables**: Never commit tokens to git
2. **Restrict file permissions**: 
   ```bash
   chmod 600 .env
   ```
3. **Run as non-root user**: Update the systemd service to use a dedicated user
4. **Keep dependencies updated**: Regularly update dependencies
5. **Monitor logs**: Set up log rotation and monitoring

## Support

For issues and questions, please open an issue on GitHub:
https://github.com/coolestowl/slack-copilot/issues
