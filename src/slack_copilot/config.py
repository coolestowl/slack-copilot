"""Configuration management for Slack Copilot Bot."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Application configuration."""
    
    # Slack configuration
    slack_bot_token: str
    slack_app_token: str
    
    # GitHub Copilot CLI configuration
    copilot_cli_path: str = "gh"
    
    # Server configuration
    port: int = 3000
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
        slack_app_token = os.getenv("SLACK_APP_TOKEN")
        
        if not slack_bot_token:
            raise ValueError("SLACK_BOT_TOKEN environment variable is required")
        if not slack_app_token:
            raise ValueError("SLACK_APP_TOKEN environment variable is required")
        
        return cls(
            slack_bot_token=slack_bot_token,
            slack_app_token=slack_app_token,
            copilot_cli_path=os.getenv("COPILOT_CLI_PATH", "gh"),
            port=int(os.getenv("PORT", "3000")),
        )
