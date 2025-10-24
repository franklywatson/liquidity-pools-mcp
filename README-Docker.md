# Liquidity Pools MCP Server - Docker Deployment

A Dockerized MCP server that tracks and analyzes DEX liquidity pools with streamable-http transport support.

![GitHub License](https://img.shields.io/github/license/kukapay/liquidity-pools-mcp)
![Python Version](https://img.shields.io/badge/python-3.12+-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## Features

- **Streamable-HTTP Transport**: Native HTTP endpoint support for web integration
- **Liquidity Pool Data Retrieval**: Fetches liquidity pool details using DexScreener API
- **Docker Support**: Complete containerization with Docker and Docker Compose
- **Health Checks**: Built-in health monitoring
- **Production Ready**: Security hardening and best practices

## Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/kukapay/liquidity-pools-mcp.git
cd liquidity-pools-mcp

# Build and run with Docker Compose
docker-compose up -d

# Check the logs
docker-compose logs -f

# Test the server
python3 test_mcp.py
```

### Option 2: Using Docker Stack

```bash
# Build the image
docker build -t liquidity-pools-mcp:latest .

# Deploy using Docker Stack
docker stack deploy -c docker-stack.yml mcp-stack

# Check service status
docker service ls
docker service logs mcp-stack_liquidity-pools-mcp
```

### Option 3: Manual Docker Run

```bash
# Build the image
docker build -t liquidity-pools-mcp:latest .

# Run the container
docker run -d \
  --name liquidity-pools-mcp \
  -p 8000:8000 \
  -e FASTMCP_HOST=0.0.0.0 \
  -e FASTMCP_PORT=8000 \
  --restart unless-stopped \
  liquidity-pools-mcp:latest
```

## Configuration

The server can be configured using environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `FASTMCP_HOST` | `127.0.0.1` | Host to bind to |
| `FASTMCP_PORT` | `8000` | Port to listen on |
| `FASTMCP_DEBUG` | `false` | Enable debug mode |
| `FASTMCP_LOG_LEVEL` | `INFO` | Logging level |

## API Endpoints

### Main MCP Endpoint
- **URL**: `http://localhost:8000/mcp`
- **Method**: POST
- **Content-Type**: `application/json`

### Health Check
- **URL**: `http://localhost:8000/mcp`
- **Method**: GET

## Usage Examples

### Using the MCP Tool

The server provides the `get_liquidity_pools` tool with the following parameters:

- `chain_id` (str): Blockchain identifier (e.g., 'bsc', 'eth')
- `token_address` (str): Token contract address

Example Request:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_liquidity_pools",
    "arguments": {
      "chain_id": "bsc",
      "token_address": "0xe6DF05CE8C8301223373CF5B969AFCb1498c5528"
    }
  }
}
```

### Testing with Python

```python
import requests

# Test server health
response = requests.get("http://localhost:8000/mcp")
print(f"Status: {response.status_code}")

# Call the MCP tool
tool_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "get_liquidity_pools",
        "arguments": {
            "chain_id": "bsc",
            "token_address": "0xe6DF05CE8C8301223373CF5B969AFCb1498c5528"
        }
    }
}

response = requests.post(
    "http://localhost:8000/mcp",
    json=tool_request,
    headers={"Content-Type": "application/json"}
)
print(response.json())
```

## Docker Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client App    │───▶│  Docker Host    │───▶│ MCP Container   │
│                 │    │  Port 8000     │    │  StreamableHTTP │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │  DexScreener    │
                                              │     API         │
                                              └─────────────────┘
```

## Production Deployment

### Security Considerations

1. **Network Security**: Place behind reverse proxy (nginx/traefik)
2. **Authentication**: Configure OAuth/JWT authentication
3. **Rate Limiting**: Implement API rate limiting
4. **Monitoring**: Set up health monitoring and alerting

### Docker Compose Production Example

```yaml
version: '3.8'

services:
  liquidity-pools-mcp:
    image: liquidity-pools-mcp:latest
    container_name: liquidity-pools-mcp
    ports:
      - "127.0.0.1:8000:8000"  # Bind to localhost only
    environment:
      - FASTMCP_HOST=0.0.0.0
      - FASTMCP_PORT=8000
      - FASTMCP_DEBUG=false
      - FASTMCP_LOG_LEVEL=WARNING
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/mcp"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - mcp-network

networks:
  mcp-network:
    driver: bridge
```

### Docker Swarm Deployment

```bash
# Initialize Docker Swarm (if not already done)
docker swarm init

# Deploy the stack
docker stack deploy -c docker-stack.yml mcp-stack

# Scale the service
docker service scale mcp-stack_liquidity-pools-mcp=3

# Update the service
docker service update --image liquidity-pools-mcp:v2 mcp-stack_liquidity-pools-mcp

# Remove the stack
docker stack rm mcp-stack
```

## Monitoring and Logs

### View Logs
```bash
# Docker Compose
docker-compose logs -f

# Docker container
docker logs -f liquidity-pools-mcp

# Docker Stack
docker service logs mcp-stack_liquidity-pools-mcp
```

### Health Monitoring
```bash
# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}"

# Check service health (Swarm)
docker service ps mcp-stack_liquidity-pools-mcp
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using port 8000
   lsof -i :8000

   # Use a different port
   docker run -p 8001:8000 liquidity-pools-mcp:latest
   ```

2. **Connection Refused**
   ```bash
   # Check if container is running
   docker ps

   # Check container logs
   docker logs liquidity-pools-mcp
   ```

3. **Build Issues**
   ```bash
   # Clean build
   docker system prune -f
   docker build --no-cache -t liquidity-pools-mcp:latest .
   ```

### Debug Mode

Enable debug logging:
```bash
docker run -e FASTMCP_DEBUG=true -p 8000:8000 liquidity-pools-mcp:latest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.