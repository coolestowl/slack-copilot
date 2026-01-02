"""GitHub Copilot CLI integration with REPL mode."""

import asyncio
import logging
from typing import Optional, Callable

logger = logging.getLogger(__name__)


class CopilotCLI:
    """GitHub Copilot CLI integration with persistent REPL session."""
    
    def __init__(self, cli_path: str = "copilot"):
        """Initialize the Copilot CLI integration.
        
        Args:
            cli_path: Path to the Copilot CLI executable (default: 'copilot')
        """
        self.cli_path = cli_path
        self.process: Optional[asyncio.subprocess.Process] = None
        self._output_task: Optional[asyncio.Task] = None
        
    async def start(self):
        """Start the Copilot CLI in REPL mode."""
        try:
            self.process = await asyncio.create_subprocess_exec(
                self.cli_path,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            logger.info("Copilot CLI REPL started")
        except FileNotFoundError:
            logger.error(f"Copilot CLI not found at path: {self.cli_path}")
            raise
        except Exception as e:
            logger.error(f"Error starting Copilot CLI: {e}")
            raise
    
    async def stop(self):
        """Stop the Copilot CLI REPL."""
        if self._output_task and not self._output_task.done():
            self._output_task.cancel()
            try:
                await self._output_task
            except asyncio.CancelledError:
                pass
        
        if self.process:
            try:
                self.process.terminate()
                await asyncio.wait_for(self.process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                self.process.kill()
                await self.process.wait()
            logger.info("Copilot CLI REPL stopped")
    
    async def send_message(self, message: str, output_callback: Callable[[str], None]):
        """Send a message to Copilot REPL and stream output.
        
        Args:
            message: The message to send to Copilot
            output_callback: Async function called with each chunk of output
        """
        if not self.process or not self.process.stdin:
            raise RuntimeError("Copilot CLI REPL not started")
        
        # Write message to stdin with newline
        self.process.stdin.write((message + "\n").encode())
        await self.process.stdin.drain()
        logger.info(f"Sent message to Copilot: {message[:50]}...")
        
        # Start streaming output
        if self._output_task and not self._output_task.done():
            self._output_task.cancel()
            try:
                await self._output_task
            except asyncio.CancelledError:
                pass
        
        self._output_task = asyncio.create_task(
            self._stream_output(output_callback)
        )
    
    async def _stream_output(self, output_callback: Callable[[str], None]):
        """Stream output from Copilot CLI.
        
        Args:
            output_callback: Async function called with each chunk of output
        """
        if not self.process or not self.process.stdout:
            return
        
        try:
            buffer = ""
            while True:
                # Read output every second
                try:
                    # Try to read available data
                    chunk = await asyncio.wait_for(
                        self.process.stdout.read(1024),
                        timeout=1.0
                    )
                    
                    if not chunk:
                        # Process ended
                        if buffer:
                            await output_callback(buffer)
                        break
                    
                    text = chunk.decode('utf-8', errors='replace')
                    buffer += text
                    
                    # Send accumulated buffer to callback
                    if buffer:
                        await output_callback(buffer)
                        buffer = ""
                        
                except asyncio.TimeoutError:
                    # No data available, send buffer if we have any
                    if buffer:
                        await output_callback(buffer)
                        buffer = ""
                    continue
                    
        except asyncio.CancelledError:
            logger.info("Output streaming cancelled")
            raise
        except Exception as e:
            logger.error(f"Error streaming output: {e}")
