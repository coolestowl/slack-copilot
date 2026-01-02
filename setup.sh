#!/bin/bash
# Setup script for Slack Copilot Bot

set -e

echo "🚀 Setting up Slack Copilot Bot..."

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "⚠️  This script is designed for Linux. You may need to adjust for your OS."
fi

# Check if Python 3.12+ is installed
if ! command -v python3.12 &> /dev/null; then
    echo "❌ Python 3.12 is required but not found."
    echo "Please install Python 3.12 first."
    exit 1
fi

echo "✅ Python 3.12 found"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    pip install uv
fi

echo "✅ uv found"

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is required but not found."
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

echo "✅ GitHub CLI found"

# Check if GitHub CLI is authenticated
if ! gh auth status &> /dev/null; then
    echo "⚠️  GitHub CLI is not authenticated."
    echo "Running 'gh auth login'..."
    gh auth login
fi

echo "✅ GitHub CLI authenticated"

# Check if Copilot extension is installed
if ! gh extension list | grep -q "github/gh-copilot"; then
    echo "📦 Installing GitHub Copilot extension..."
    gh extension install github/gh-copilot
fi

echo "✅ GitHub Copilot extension installed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit .env file and add your Slack tokens:"
    echo "   - SLACK_BOT_TOKEN"
    echo "   - SLACK_APP_TOKEN"
    echo ""
    read -p "Press enter to open .env in your default editor..."
    ${EDITOR:-nano} .env
fi

echo "✅ .env file configured"

# Install dependencies
echo "📦 Installing Python dependencies..."
uv sync

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the bot, run:"
echo "  uv run python main.py"
echo ""
echo "Or with Docker:"
echo "  docker-compose up -d"
echo ""
