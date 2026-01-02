"""Slack bot implementation."""

import logging
import asyncio
from typing import Optional

from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

from .config import Config
from .copilot import CopilotCLI

logger = logging.getLogger(__name__)


class SlackCopilotBot:
    """Slack bot that integrates with GitHub Copilot CLI."""
    
    def __init__(self, config: Config):
        """Initialize the Slack bot.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.app = AsyncApp(token=config.slack_bot_token)
        self.copilot = CopilotCLI(config.copilot_cli_path)
        
        # Register event handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Register Slack event handlers."""
        
        @self.app.message("hello")
        async def message_hello(message, say):
            """Respond to hello messages."""
            await say(f"Hey there <@{message['user']}>! 👋")
        
        @self.app.event("app_mention")
        async def handle_app_mention(event, say):
            """Handle app mentions (@bot message)."""
            text = event.get("text", "")
            user = event.get("user")
            
            # Remove the bot mention from the text
            # The text typically starts with <@BOTID>
            words = text.split(maxsplit=1)
            if len(words) > 1:
                prompt = words[1].strip()
            else:
                await say(f"Hi <@{user}>! Ask me anything about commands. For example: '@bot how do I list files?'")
                return
            
            # Check if it's an explain request
            if prompt.lower().startswith("explain "):
                command = prompt[8:].strip()
                response = await self.copilot.explain_command(command)
            else:
                response = await self.copilot.execute_command(prompt)
            
            await say(f"<@{user}> {response}")
        
        @self.app.command("/copilot")
        async def handle_copilot_command(ack, command, say):
            """Handle /copilot slash command."""
            await ack()
            
            text = command.get("text", "").strip()
            user = command.get("user_id")
            
            if not text:
                await say("Please provide a question or command. Example: `/copilot how do I find large files?`")
                return
            
            # Check if it's an explain request
            if text.lower().startswith("explain "):
                cmd = text[8:].strip()
                response = await self.copilot.explain_command(cmd)
            else:
                response = await self.copilot.execute_command(text)
            
            await say(f"<@{user}> {response}")
        
        @self.app.event("message")
        async def handle_message_events(body, logger):
            """Log message events."""
            logger.info(body)
    
    async def start(self):
        """Start the Slack bot."""
        logger.info("Starting Slack Copilot Bot...")
        handler = AsyncSocketModeHandler(self.app, self.config.slack_app_token)
        await handler.start_async()
