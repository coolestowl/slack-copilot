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

# Check if GitHub Copilot CLI is installed
if ! command -v copilot &> /dev/null; then
    echo "❌ GitHub Copilot CLI (copilot) is required but not found."
    echo "Please install it from: https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line"
    exit 1
fi

echo "✅ GitHub Copilot CLI found"

# Check if Copilot CLI is authenticated
if ! copilot --version &> /dev/null; then
    echo "⚠️  GitHub Copilot CLI may not be authenticated."
    echo "Please run 'copilot suggest \"test\"' to authenticate."
fi

echo "✅ GitHub Copilot CLI ready"

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
