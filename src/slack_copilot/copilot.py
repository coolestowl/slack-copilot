"""GitHub Copilot CLI integration."""

import asyncio
import logging
from typing import Optional

logger = logging.getLogger(__name__)


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
        try:
            # Run GitHub Copilot CLI
            # Using 'gh copilot suggest' for command suggestions
            process = await asyncio.create_subprocess_exec(
                self.cli_path,
                "copilot",
                "suggest",
                prompt,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode().strip()
                logger.error(f"Copilot CLI error: {error_msg}")
                return f"❌ Error executing Copilot CLI: {error_msg}"
            
            result = stdout.decode().strip()
            return result if result else "No response from Copilot CLI"
            
        except FileNotFoundError:
            logger.error(f"GitHub CLI not found at path: {self.cli_path}")
            return f"❌ GitHub CLI not found. Please install it: https://cli.github.com/"
        except Exception as e:
            logger.error(f"Error executing Copilot CLI: {e}")
            return f"❌ Error: {str(e)}"
    
    async def explain_command(self, command: str) -> str:
        """Explain a command using GitHub Copilot CLI.
        
        Args:
            command: The command to explain
            
        Returns:
            The explanation from Copilot CLI
        """
        try:
            process = await asyncio.create_subprocess_exec(
                self.cli_path,
                "copilot",
                "explain",
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode().strip()
                logger.error(f"Copilot CLI error: {error_msg}")
                return f"❌ Error executing Copilot CLI: {error_msg}"
            
            result = stdout.decode().strip()
            return result if result else "No response from Copilot CLI"
            
        except FileNotFoundError:
            logger.error(f"GitHub CLI not found at path: {self.cli_path}")
            return f"❌ GitHub CLI not found. Please install it: https://cli.github.com/"
        except Exception as e:
            logger.error(f"Error executing Copilot CLI: {e}")
            return f"❌ Error: {str(e)}"
