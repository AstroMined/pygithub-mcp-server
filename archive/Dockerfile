# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install UV package manager
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY github/ github/

# Create virtual environment and install dependencies
RUN uv venv
RUN uv pip install .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Run the server
CMD ["python", "-m", "github.server"]
