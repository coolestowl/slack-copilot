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
    
    async def _post_initial_message(self, client, channel: str, text: str) -> str:
        """Post initial 'Thinking...' message and return message timestamp.
        
        Args:
            client: Slack client
            channel: Channel ID to post message in
            text: Initial text to display
            
        Returns:
            Message timestamp of the posted message
        """
        result = await client.chat_postMessage(
            channel=channel,
            text=text
        )
        message_ts = result["ts"]
        self.active_messages[channel] = message_ts
        logger.debug(f"📤 Posted initial message to channel {channel}, message_ts: {message_ts}")
        return message_ts
    
    def _create_update_callback(self, client, channel: str, message_ts: str, user_prefix: str = ""):
        """Create a callback function to update Slack message with streaming response.
        
        Args:
            client: Slack client
            channel: Channel ID
            message_ts: Message timestamp to update
            user_prefix: Optional prefix for the message (e.g., "<@user> ")
            
        Returns:
            Async callback function that updates the message
        """
        # State to track message splitting
        state = {
            "current_ts": message_ts,
            "current_text": "",
            "is_first_message": True
        }
        
        # Slack message limit is ~4000 chars. Use a safe limit.
        MAX_LENGTH = 3500
        
        async def update_slack(chunk: str):
            prefix = user_prefix if state["is_first_message"] else ""
            current_length = len(prefix) + len(state["current_text"])
            
            # Check if adding chunk would exceed limit
            if current_length + len(chunk) > MAX_LENGTH:
                # Start a new message
                try:
                    # The new message starts with the chunk
                    new_text = chunk
                    result = await client.chat_postMessage(
                        channel=channel,
                        text=new_text
                    )
                    state["current_ts"] = result["ts"]
                    state["current_text"] = new_text
                    state["is_first_message"] = False
                    logger.debug(f"Started new message segment: {state['current_ts']}")
                except Exception as e:
                    logger.error(f"Error creating new message segment: {e}")
            else:
                # Append to current message
                state["current_text"] += chunk
                try:
                    await client.chat_update(
                        channel=channel,
                        ts=state["current_ts"],
                        text=f"{prefix}{state['current_text']}"
                    )
                except Exception as e:
                    logger.error(f"Error updating message: {e}")
        
        return update_slack
    
    async def _send_to_copilot(self, prompt: str, update_callback, client, channel: str, message_ts: str, error_prefix: str = ""):
        """Send message to Copilot and handle errors.
        
        Args:
            prompt: Message to send to Copilot
            update_callback: Callback function to update Slack message
            client: Slack client for error updates
            channel: Channel ID
            message_ts: Message timestamp to update on error
            error_prefix: Optional prefix for error messages (e.g., "<@user> ")
        """
        logger.debug(f"🤖 Sending message to Copilot - Prompt length: {len(prompt)} characters")
        try:
            await self.copilot.send_message(prompt, update_callback)
            logger.info(f"✅ Successfully processed Copilot response for channel {channel}")
        except Exception as e:
            logger.error(f"Error communicating with Copilot: {e}")
            await client.chat_update(
                channel=channel,
                ts=message_ts,
                text=f"{error_prefix}❌ Error: {str(e)}"
            )
    
    def _register_handlers(self):
        """Register Slack event handlers."""
        
        @self.app.event("app_mention")
        async def handle_app_mention(event, say, client):
            """Handle app mentions (@bot message)."""
            text = event.get("text", "")
            user = event.get("user")
            channel = event.get("channel")
            
            # Log incoming mention event for debugging
            logger.info(
                f"📨 Received app_mention event - User: {user}, Channel: {channel}, "
                f"Message length: {len(text) if text else 0} characters, "
                f"Event timestamp: {event.get('ts', 'N/A')}"
            )
            
            # Remove the bot mention from the text
            words = text.split(maxsplit=1)
            if len(words) > 1:
                prompt = words[1].strip()
            else:
                await say(f"Hi <@{user}>! Send me a message and I'll respond with Copilot.")
                return
            
            user_prefix = f"<@{user}> "
            message_ts = await self._post_initial_message(client, channel, f"{user_prefix}Thinking...")
            update_callback = self._create_update_callback(client, channel, message_ts, user_prefix)
            await self._send_to_copilot(prompt, update_callback, client, channel, message_ts, user_prefix)
        
        @self.app.command("/copilot")
        async def handle_copilot_command(ack, command, say, client):
            """Handle /copilot slash command."""
            await ack()
            
            text = command.get("text", "").strip()
            user = command.get("user_id")
            channel = command.get("channel_id")
            
            # Log incoming slash command for debugging
            logger.info(
                f"📨 Received /copilot command - User: {user}, Channel: {channel}, "
                f"Command length: {len(text) if text else 0} characters, "
                f"Command ID: {command.get('command_id', 'N/A')}"
            )
            
            if not text:
                await say("Please provide a question. Example: `/copilot how do I list files?`")
                return
            
            user_prefix = f"<@{user}> "
            message_ts = await self._post_initial_message(client, channel, f"{user_prefix}Thinking...")
            update_callback = self._create_update_callback(client, channel, message_ts, user_prefix)
            await self._send_to_copilot(text, update_callback, client, channel, message_ts, user_prefix)
        
        @self.app.event("message")
        async def handle_message_events(event, say, client):
            """Handle direct messages to the bot."""
            # Skip bot messages and thread replies
            if event.get("bot_id") or event.get("thread_ts"):
                logger.debug(
                    f"🔇 Skipping message event - Bot message: {bool(event.get('bot_id'))}, "
                    f"Thread reply: {bool(event.get('thread_ts'))}"
                )
                return
            
            channel = event.get("channel")
            user = event.get("user")
            text = event.get("text", "").strip()
            
            if not text:
                logger.debug(f"🔇 Skipping empty message event - Channel: {channel}, User: {user}")
                return
            
            # Check if this is a DM or the bot is in the channel
            channel_type = event.get("channel_type")
            if channel_type != "im":
                # Not a DM, ignore unless mentioned (handled by app_mention)
                logger.debug(
                    f"🔇 Skipping non-DM message event - Channel: {channel}, "
                    f"Channel type: {channel_type}, User: {user}"
                )
                return
            
            # Log incoming direct message event for debugging
            logger.info(
                f"📨 Received message event (DM) - User: {user}, Channel: {channel}, "
                f"Message length: {len(text)} characters, "
                f"Event timestamp: {event.get('ts', 'N/A')}"
            )
            
            message_ts = await self._post_initial_message(client, channel, "Thinking...")
            update_callback = self._create_update_callback(client, channel, message_ts)
            await self._send_to_copilot(text, update_callback, client, channel, message_ts)
    
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
