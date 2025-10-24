# Liquidity Pools MCP Server

An MCP server that tracks and analyzes DEX liquidity pools to power intelligent DeFi agents and automated strategies.

![GitHub License](https://img.shields.io/github/license/kukapay/liquidity-pools-mcp)
![Python Version](https://img.shields.io/badge/python-3.10+-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## Features

- **Liquidity Pool Data Retrieval**: Fetches liquidity pool details for a specified chain ID and token address using the DexScreener API.
- **Multiple Transport Modes**: Supports both stdio (for Claude Desktop integration) and streamable-http (for web applications) transports.
- **Markdown Table Output**: Presents pool data in a clear markdown table with columns for Dex ID, Pair Address, Base/Quote Token Symbols, Price USD, 24h Buy/Sell Transactions, 24h Volume, Liquidity USD, and Market Cap.
- **Total Liquidity Calculation**: Computes and displays the total liquidity in USD across all pools.
- **Prompt Guidance**: Includes a prompt to guide users on analyzing liquidity pool data, including pool count, table output, total liquidity, and notable metrics.
- **Docker Support**: Ready-to-use Docker configuration for HTTP server deployment.

## Prerequisites

- Python 3.10 or higher.
- **uv**: Recommended for managing dependencies ([documentation](https://docs.astral.sh/uv/)).

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/kukapay/liquidity-pools-mcp.git
   cd liquidity-pools-mcp
   ```

2. **Install Dependencies**:

   Using `uv` (recommended for faster dependency management):

   ```bash
   uv sync
   ```

   Or using `pip`:

   ```bash
   pip install mcp[cli]
   ```
   
3. **Installing to Claude Desktop**:

    Install the server as a Claude Desktop application:
    ```bash
    uv run mcp install main.py --name "Liquidity Pools"
    ```

    Configuration file as a reference:

    ```json
    {
       "mcpServers": {
           "Liquidity Pools": {
               "command": "uv",
               "args": [ "--directory", "/path/to/liquidity-pools-mcp", "run", "main.py" ] 
           }
       }
    }
    ```
    Replace `/path/to/liquidity-pools-mcp` with your actual installation path.
   

## Usage


Use the MCP Inspector or integrate with a client (e.g., Claude Desktop) to call the `get_liquidity_pools` tool. 

**Example Prompt**:
```
Fetch the liquidity pools for token 0xe6DF05CE8C8301223373CF5B969AFCb1498c5528 on chain bsc.
```

**Example Output**:

```markdown
| Dex ID      | Pair Address                              | Base/Quote | Price USD | 24h Buys/Sells | 24h Volume | Liquidity USD | Market Cap |
|-------------|-------------------------------------------|------------|-----------|----------------|------------|---------------|------------|
| pancakeswap | 0x123...abc                              | CAKE/BUSD  | 2.45      | 150/100        | 500000     | 1000000       | 2000000    |
| apeswap     | 0x456...def                              | CAKE/BNB   | 2.43      | 80/50          | 300000     | 800000        | 1900000    |

**Total Liquidity USD**: 1800000
```

## HTTP Server Mode

The server supports running in HTTP mode for web application integration. This is useful when you want to expose the MCP functionality as an HTTP API.

### Running the HTTP Server

#### Option 1: Direct Python Execution

```bash
# Run with streamable-http transport (default port 8000)
python main.py --transport streamable-http

# Run with custom host and port
export FASTMCP_HOST=0.0.0.0
export FASTMCP_PORT=8080
python main.py --transport streamable-http
```

#### Option 2: Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/kukapay/liquidity-pools-mcp.git
cd liquidity-pools-mcp

# Build and run with Docker Compose
docker-compose up -d

# The server will be available at http://localhost:9889
```

#### Option 3: Manual Docker Run

```bash
# Build the image
docker build -t liquidity-pools-mcp:latest .

# Run the container
docker run -d \
  --name liquidity-pools-mcp \
  -p 8000:8000 \
  -e FASTMCP_HOST=0.0.0.0 \
  -e FASTMCP_PORT=8000 \
  liquidity-pools-mcp:latest
```

### HTTP API Usage

#### Server Endpoints

- **Main MCP Endpoint**: `http://localhost:8000/mcp` (POST)
- **Health Check**: `http://localhost:8000/mcp` (GET)

#### Making API Requests

The server accepts JSON-RPC 2.0 requests. Here's how to call the `get_liquidity_pools` tool:

```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
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
  }'
```

#### Python Client Example

```python
import requests

# Call the MCP tool via HTTP
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

result = response.json()
print(result)
```

### Configuration

The HTTP server can be configured using environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `FASTMCP_HOST` | `127.0.0.1` | Host to bind the server to |
| `FASTMCP_PORT` | `8000` | Port to listen on |
| `FASTMCP_DEBUG` | `false` | Enable debug mode |
| `FASTMCP_LOG_LEVEL` | `INFO` | Logging level |

### Testing the HTTP Server

```bash
# Test server health
curl http://localhost:8000/mcp

# Run the provided test script
python3 test_mcp.py
```

For more detailed Docker deployment instructions and production configuration examples, see [README-Docker.md](README-Docker.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

