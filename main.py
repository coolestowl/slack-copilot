"""Main entry point for Slack Copilot Bot."""

import asyncio
import logging
import sys

from dotenv import load_dotenv

from src.slack_copilot.bot import SlackCopilotBot
from src.slack_copilot.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


async def main():
    """Main function to run the Slack bot."""
    # Load environment variables from .env file
    load_dotenv()
    
    try:
        # Load configuration
        config = Config.from_env()
        
        # Create and start the bot
        bot = SlackCopilotBot(config)
        logger.info("🚀 Slack Copilot Bot is starting...")
        await bot.start()
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please check your .env file and ensure all required variables are set.")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
