# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install GitHub Copilot CLI
# Note: You need to install copilot CLI in the container
# Visit: https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line
# For now, we expect it to be available in the PATH or mounted

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src ./src
COPY main.py ./

# Install Python dependencies
RUN uv sync --frozen --no-dev

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["uv", "run", "python", "main.py"]
