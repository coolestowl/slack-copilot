"""GitHub Copilot CLI integration."""

import asyncio
import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)


def sanitize_error_message(error: str) -> str:
    """Sanitize error messages to prevent information leakage.
    
    Args:
        error: Raw error message
        
    Returns:
        Sanitized error message safe for display
    """
    # Remove potential file paths
    error = re.sub(r'/[^\s]*', '[path]', error)
    # Remove potential user names
    error = re.sub(r'/home/[^\s/]*', '/home/[user]', error)
    # Limit length
    if len(error) > 500:
        error = error[:500] + "..."
    return error


class CopilotCLI:
    """GitHub Copilot CLI integration."""
    
    def __init__(self, cli_path: str = "gh"):
        """Initialize the Copilot CLI integration.
        
        Args:
            cli_path: Path to the GitHub CLI executable (default: 'gh')
        """
        self.cli_path = cli_path
    
    async def execute_command(self, prompt: str) -> str:
        """Execute a GitHub Copilot CLI command and return the result.
        
        Args:
            prompt: The prompt/question to send to Copilot
            
        Returns:
            The response from Copilot CLI
        """
        # Basic input validation
        if not prompt or not prompt.strip():
            return "❌ Please provide a valid question or prompt."
        
        # Limit prompt length to prevent abuse
        if len(prompt) > 1000:
            return "❌ Prompt is too long. Please keep it under 1000 characters."
        
        try:
            # Run GitHub Copilot CLI
            # Using 'gh copilot suggest' for command suggestions
            # Note: The prompt is passed as a separate argument, not concatenated,
            # which prevents command injection
            process = await asyncio.create_subprocess_exec(
                self.cli_path,
                "copilot",
                "suggest",
                prompt,  # Passed as separate argument, not shell-interpreted
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode().strip()
                sanitized_error = sanitize_error_message(error_msg)
                logger.error(f"Copilot CLI error: {error_msg}")
                return f"❌ Error executing Copilot CLI: {sanitized_error}"
            
            result = stdout.decode().strip()
            return result if result else "No response from Copilot CLI"
            
        except FileNotFoundError:
            logger.error(f"GitHub CLI not found at path: {self.cli_path}")
            return f"❌ GitHub CLI not found. Please install it: https://cli.github.com/"
        except Exception as e:
            logger.error(f"Error executing Copilot CLI: {e}")
            return f"❌ An unexpected error occurred. Please try again later."
    
    async def explain_command(self, command: str) -> str:
        """Explain a command using GitHub Copilot CLI.
        
        Args:
            command: The command to explain
            
        Returns:
            The explanation from Copilot CLI
        """
        # Basic input validation
        if not command or not command.strip():
            return "❌ Please provide a valid command to explain."
        
        # Limit command length to prevent abuse
        if len(command) > 1000:
            return "❌ Command is too long. Please keep it under 1000 characters."
        
        try:
            process = await asyncio.create_subprocess_exec(
                self.cli_path,
                "copilot",
                "explain",
                command,  # Passed as separate argument, not shell-interpreted
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode().strip()
                sanitized_error = sanitize_error_message(error_msg)
                logger.error(f"Copilot CLI error: {error_msg}")
                return f"❌ Error executing Copilot CLI: {sanitized_error}"
            
            result = stdout.decode().strip()
            return result if result else "No response from Copilot CLI"
            
        except FileNotFoundError:
            logger.error(f"GitHub CLI not found at path: {self.cli_path}")
            return f"❌ GitHub CLI not found. Please install it: https://cli.github.com/"
        except Exception as e:
            logger.error(f"Error executing Copilot CLI: {e}")
            return f"❌ An unexpected error occurred. Please try again later."
