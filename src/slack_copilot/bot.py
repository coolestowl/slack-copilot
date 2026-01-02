"""Slack bot implementation with streaming Copilot responses."""

import logging
import asyncio
from typing import Optional, Dict

from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

from .config import Config
from .copilot import CopilotCLI

logger = logging.getLogger(__name__)


class SlackCopilotBot:
    """Slack bot that integrates with GitHub Copilot CLI in REPL mode."""
    
    def __init__(self, config: Config):
        """Initialize the Slack bot.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.app = AsyncApp(token=config.slack_bot_token)
        self.copilot = CopilotCLI(config.copilot_cli_path)
        
        # Track active conversations: channel_id -> message_ts
        self.active_messages: Dict[str, str] = {}
        
        # Register event handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Register Slack event handlers."""
        
        @self.app.event("app_mention")
        async def handle_app_mention(event, say, client):
            """Handle app mentions (@bot message)."""
            text = event.get("text", "")
            user = event.get("user")
            channel = event.get("channel")
            
            # Remove the bot mention from the text
            words = text.split(maxsplit=1)
            if len(words) > 1:
                prompt = words[1].strip()
            else:
                await say(f"Hi <@{user}>! Send me a message and I'll respond with Copilot.")
                return
            
            # Post initial message
            result = await client.chat_postMessage(
                channel=channel,
                text=f"<@{user}> Thinking..."
            )
            message_ts = result["ts"]
            self.active_messages[channel] = message_ts
            
            # Create callback to update message
            full_response = [""]
            
            async def update_slack(chunk: str):
                full_response[0] += chunk
                try:
                    await client.chat_update(
                        channel=channel,
                        ts=message_ts,
                        text=f"<@{user}> {full_response[0]}"
                    )
                except Exception as e:
                    logger.error(f"Error updating message: {e}")
            
            # Send message to Copilot
            try:
                await self.copilot.send_message(prompt, update_slack)
            except Exception as e:
                logger.error(f"Error communicating with Copilot: {e}")
                await client.chat_update(
                    channel=channel,
                    ts=message_ts,
                    text=f"<@{user}> ❌ Error: {str(e)}"
                )
        
        @self.app.command("/copilot")
        async def handle_copilot_command(ack, command, say, client):
            """Handle /copilot slash command."""
            await ack()
            
            text = command.get("text", "").strip()
            user = command.get("user_id")
            channel = command.get("channel_id")
            
            if not text:
                await say("Please provide a question. Example: `/copilot how do I list files?`")
                return
            
            # Post initial message
            result = await client.chat_postMessage(
                channel=channel,
                text=f"<@{user}> Thinking..."
            )
            message_ts = result["ts"]
            self.active_messages[channel] = message_ts
            
            # Create callback to update message
            full_response = [""]
            
            async def update_slack(chunk: str):
                full_response[0] += chunk
                try:
                    await client.chat_update(
                        channel=channel,
                        ts=message_ts,
                        text=f"<@{user}> {full_response[0]}"
                    )
                except Exception as e:
                    logger.error(f"Error updating message: {e}")
            
            # Send message to Copilot
            try:
                await self.copilot.send_message(text, update_slack)
            except Exception as e:
                logger.error(f"Error communicating with Copilot: {e}")
                await client.chat_update(
                    channel=channel,
                    ts=message_ts,
                    text=f"<@{user}> ❌ Error: {str(e)}"
                )
        
        @self.app.event("message")
        async def handle_message_events(event, say, client):
            """Handle direct messages to the bot."""
            # Skip bot messages and thread replies
            if event.get("bot_id") or event.get("thread_ts"):
                return
            
            channel = event.get("channel")
            user = event.get("user")
            text = event.get("text", "").strip()
            
            if not text:
                return
            
            # Check if this is a DM or the bot is in the channel
            channel_type = event.get("channel_type")
            if channel_type != "im":
                # Not a DM, ignore unless mentioned (handled by app_mention)
                return
            
            # Post initial message
            result = await client.chat_postMessage(
                channel=channel,
                text="Thinking..."
            )
            message_ts = result["ts"]
            self.active_messages[channel] = message_ts
            
            # Create callback to update message
            full_response = [""]
            
            async def update_slack(chunk: str):
                full_response[0] += chunk
                try:
                    await client.chat_update(
                        channel=channel,
                        ts=message_ts,
                        text=full_response[0]
                    )
                except Exception as e:
                    logger.error(f"Error updating message: {e}")
            
            # Send message to Copilot
            try:
                await self.copilot.send_message(text, update_slack)
            except Exception as e:
                logger.error(f"Error communicating with Copilot: {e}")
                await client.chat_update(
                    channel=channel,
                    ts=message_ts,
                    text=f"❌ Error: {str(e)}"
                )
    
    async def start(self):
        """Start the Slack bot and Copilot REPL."""
        logger.info("Starting Slack Copilot Bot...")
        
        # Start Copilot REPL
        try:
            await self.copilot.start()
        except Exception as e:
            logger.error(f"Failed to start Copilot CLI: {e}")
            raise
        
        # Start Slack bot
        handler = AsyncSocketModeHandler(self.app, self.config.slack_app_token)
        await handler.start_async()
    
    async def stop(self):
        """Stop the bot and cleanup."""
        logger.info("Stopping Slack Copilot Bot...")
        await self.copilot.stop()
