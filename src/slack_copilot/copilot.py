"""GitHub Copilot CLI integration with REPL mode."""

import asyncio
import logging
import os
import pty
import re
import termios
from typing import Optional, Callable, Awaitable

logger = logging.getLogger(__name__)

# Regex to match ANSI escape sequences
ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')



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
        self.master_fd: Optional[int] = None
        self.reader: Optional[asyncio.StreamReader] = None
        
    async def start(self):
        """Start the Copilot CLI in REPL mode."""
        try:
            # Create PTY
            self.master_fd, slave_fd = pty.openpty()
            
            try:
                attrs = termios.tcgetattr(slave_fd)
                attrs[3] = attrs[3] & ~termios.ECHO
                termios.tcsetattr(slave_fd, termios.TCSANOW, attrs)
            except Exception as e:
                logger.warning(f"Could not disable echo on PTY: {e}")

            # Start copilot without subcommand to enter interactive REPL
            self.process = await asyncio.create_subprocess_exec(
                self.cli_path,
                stdin=slave_fd,
                stdout=slave_fd,
                stderr=slave_fd,
                preexec_fn=os.setsid,
            )
            
            # Close slave in parent
            os.close(slave_fd)
            
            # Create StreamReader for master_fd
            loop = asyncio.get_running_loop()
            self.reader = asyncio.StreamReader()
            protocol = asyncio.StreamReaderProtocol(self.reader)
            await loop.connect_read_pipe(lambda: protocol, os.fdopen(self.master_fd, 'rb', buffering=0))
            
            logger.info("Copilot CLI REPL started")
            
            # Start draining output
            self._output_task = asyncio.create_task(self._drain_output())
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
            
        if self.master_fd is not None:
            try:
                os.close(self.master_fd)
            except OSError:
                pass
            self.master_fd = None
    
    async def send_message(self, message: str, output_callback: Callable[[str], Awaitable[None]]):
        """Send a message to Copilot REPL and stream output.
        
        Args:
            message: The message to send to Copilot
            output_callback: Async function called with accumulated output chunks
        """
        if not self.process or self.master_fd is None:
            raise RuntimeError("Copilot CLI REPL not started")
        
        # Stop any existing output task (including drain task)
        if self._output_task and not self._output_task.done():
            self._output_task.cancel()
            try:
                await self._output_task
            except asyncio.CancelledError:
                pass

        # Write message to master_fd with newline
        os.write(self.master_fd, (message + "\n").encode())
        logger.info(f"Sent message to Copilot: {message[:50]}...")
        
        self._output_task = asyncio.create_task(
            self._stream_output(output_callback)
        )
    
    async def _drain_output(self):
        """Drain output from Copilot CLI."""
        if not self.reader:
            return
        try:
            while True:
                await self.reader.read(1024)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error draining output: {e}")

    async def _stream_output(self, output_callback: Callable[[str], Awaitable[None]]):
        """Stream output from Copilot CLI.
        
        Args:
            output_callback: Async function called with accumulated output
        """
        if not self.reader:
            return
        
        try:
            buffer = ""
            last_update = asyncio.get_event_loop().time()
            
            while True:
                # Read output with timeout
                try:
                    chunk = await asyncio.wait_for(
                        self.reader.read(1024),
                        timeout=1.0
                    )
                    
                    if not chunk:
                        # Process ended or no more output
                        if buffer:
                            await output_callback(buffer)
                        break
                    
                    text = chunk.decode('utf-8', errors='replace')
                    # Filter out ANSI escape codes
                    text = ANSI_ESCAPE.sub('', text)
                    buffer += text
                    
                    # Update Slack every second to avoid rate limiting
                    current_time = asyncio.get_event_loop().time()
                    if current_time - last_update >= 1.0:
                        if buffer:
                            await output_callback(buffer)
                            buffer = ""
                            last_update = current_time
                        
                except asyncio.TimeoutError:
                    # No data available within timeout
                    # Send any accumulated buffer if it's been a second since last update
                    current_time = asyncio.get_event_loop().time()
                    if buffer and (current_time - last_update >= 1.0):
                        await output_callback(buffer)
                        buffer = ""
                        last_update = current_time
                    continue
                    
        except asyncio.CancelledError:
            logger.info("Output streaming cancelled")
            raise
        except Exception as e:
            logger.error(f"Error streaming output: {e}")
