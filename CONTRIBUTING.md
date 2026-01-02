# Contributing to Slack Copilot

Thank you for your interest in contributing to Slack Copilot! This document provides guidelines and instructions for contributing.

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/slack-copilot.git
   cd slack-copilot
   ```

2. **Install dependencies**
   ```bash
   # Quick setup
   make setup
   
   # Or manually
   uv sync
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Slack tokens
   ```

4. **Run the bot**
   ```bash
   make run
   # Or: uv run python main.py
   ```

## Project Structure

```
slack-copilot/
├── src/
│   └── slack_copilot/
│       ├── __init__.py      # Package initialization
│       ├── bot.py           # Slack bot implementation
│       ├── config.py        # Configuration management
│       └── copilot.py       # GitHub Copilot CLI integration
├── main.py                  # Application entry point
├── pyproject.toml           # Project dependencies and metadata
└── uv.lock                  # Locked dependencies
```

## Making Changes

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add docstrings to functions and classes
   - Keep changes focused and atomic

3. **Test your changes**
   ```bash
   # Run the bot locally
   make run
   
   # Test in Slack
   # Mention the bot or use slash commands
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write clear, descriptive docstrings
- Keep functions focused and modular
- Use meaningful variable names

## Adding New Features

### Adding a new Slack command

1. Add handler in `src/slack_copilot/bot.py`:
   ```python
   @self.app.command("/your-command")
   async def handle_your_command(ack, command, say):
       await ack()
       # Your implementation
   ```

### Adding new Copilot CLI functionality

1. Add method in `src/slack_copilot/copilot.py`:
   ```python
   async def your_new_method(self, param: str) -> str:
       """Your method description."""
       # Your implementation
   ```

## Dependencies

We use `uv` for dependency management:

- **Add a dependency**: `uv add package-name`
- **Remove a dependency**: `uv remove package-name`
- **Update dependencies**: `uv sync`

## Documentation

- Update README.md if you add new features
- Update DEPLOYMENT.md if you change deployment procedures
- Add comments for complex logic

## Testing

Currently, the project focuses on manual testing:

1. Run the bot locally
2. Test Slack interactions
3. Verify Copilot CLI integration

We welcome contributions to add automated testing!

## Pull Request Guidelines

- **Title**: Clear and descriptive
- **Description**: Explain what changes were made and why
- **Testing**: Describe how you tested your changes
- **Screenshots**: Include screenshots for UI changes

## Common Development Tasks

```bash
# Install dependencies
make install

# Run the bot
make run

# Build Docker image
make build

# Run with Docker
make docker-run

# View Docker logs
make docker-logs

# Clean up
make clean
```

## Getting Help

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Be respectful and constructive in discussions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
