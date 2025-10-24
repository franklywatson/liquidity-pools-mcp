# Use Python 3.12 slim image for smaller size
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    FASTMCP_HOST=0.0.0.0 \
    FASTMCP_PORT=9889 \
    FASTMCP_DEBUG=false

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir mcp[cli]>=1.9.3

# Copy application code
COPY main.py ./

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash mcp && \
    chown -R mcp:mcp /app
USER mcp

# Expose the port
EXPOSE 9889

# Health check - check if server process is responding (any response other than 000 means server is up)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -s -o /dev/null -w "%{http_code}" http://localhost:9889/ | grep -qv "000" || exit 1

# Run the MCP server with streamable-http transport
CMD ["python3", "main.py", "--transport", "streamable-http"]