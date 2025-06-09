# Liquidity Pools MCP Server

An MCP server that tracks and analyzes DEX liquidity pools to power intelligent DeFi agents and automated strategies.

![GitHub License](https://img.shields.io/github/license/kukapay/liquidity-pools-mcp)
![Python Version](https://img.shields.io/badge/python-3.10+-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## Features

- **Liquidity Pool Data Retrieval**: Fetches liquidity pool details for a specified chain ID and token address using the DexScreener API.
- **Markdown Table Output**: Presents pool data in a clear markdown table with columns for Dex ID, Pair Address, Base/Quote Token Symbols, Price USD, 24h Buy/Sell Transactions, 24h Volume, Liquidity USD, and Market Cap.
- **Total Liquidity Calculation**: Computes and displays the total liquidity in USD across all pools.
- **Prompt Guidance**: Includes a prompt to guide users on analyzing liquidity pool data, including pool count, table output, total liquidity, and notable metrics.

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


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

