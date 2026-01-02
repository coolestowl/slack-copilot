"""GitHub Copilot CLI integration with REPL mode."""

import asyncio
import logging
from typing import Optional, Callable, Awaitable

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
            # Start copilot without subcommand to enter interactive REPL
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
    
    async def send_message(self, message: str, output_callback: Callable[[str], Awaitable[None]]):
        """Send a message to Copilot REPL and stream output.
        
        Args:
            message: The message to send to Copilot
            output_callback: Async function called with accumulated output chunks
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
    
    async def _stream_output(self, output_callback: Callable[[str], Awaitable[None]]):
        """Stream output from Copilot CLI.
        
        Args:
            output_callback: Async function called with accumulated output
        """
        if not self.process or not self.process.stdout:
            return
        
        try:
            buffer = ""
            last_update = asyncio.get_event_loop().time()
            
            while True:
                # Read output with timeout
                try:
                    chunk = await asyncio.wait_for(
                        self.process.stdout.read(1024),
                        timeout=1.0
                    )
                    
                    if not chunk:
                        # Process ended or no more output
                        if buffer:
                            await output_callback(buffer)
                        break
                    
                    text = chunk.decode('utf-8', errors='replace')
                    buffer += text
                    
                    # Update Slack every second to avoid rate limiting
                    current_time = asyncio.get_event_loop().time()
                    if current_time - last_update >= 1.0:
                        if buffer:
                            await output_callback(buffer)
                            last_update = current_time
                        
                except asyncio.TimeoutError:
                    # No data available within timeout
                    # Send any accumulated buffer if it's been a second since last update
                    current_time = asyncio.get_event_loop().time()
                    if buffer and (current_time - last_update >= 1.0):
                        await output_callback(buffer)
                        last_update = current_time
                    continue
                    
        except asyncio.CancelledError:
            logger.info("Output streaming cancelled")
            raise
        except Exception as e:
            logger.error(f"Error streaming output: {e}")
