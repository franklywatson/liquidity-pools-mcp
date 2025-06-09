import asyncio
import httpx
from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP, Context

# Initialize MCP server
mcp = FastMCP("Liquidity Pools Server")

# Tool to fetch liquidity pools
@mcp.tool()
async def get_liquidity_pools(chain_id: str, token_address: str, ctx: Context) -> str:
    """
    Fetch all liquidity pools for a given chain ID and token address from DexScreener API.
    
    Args:
        chain_id (str): The blockchain identifier (e.g., 'bsc' for Binance Smart Chain, 'eth' for Ethereum)
        token_address (str): The contract address of the token (e.g., '0xe6DF05CE8C8301223373CF5B969AFCb1498c5528')
        ctx (Context): MCP context for logging and request handling
    
    Returns:
        str: A markdown table containing liquidity pool details including dexId, pairAddress, 
             base/quote token symbols, price USD, 24h buy/sell transactions, 24h volume, 
             liquidity USD, and market cap, followed by total liquidity USD
    """
    try:
        async with httpx.AsyncClient() as client:
            url = f"https://api.dexscreener.com/token-pairs/v1/{chain_id}/{token_address}"
            ctx.info(f"Fetching liquidity pools from {url}")
            
            response = await client.get(url)
            response.raise_for_status()
            
            pools = response.json()
            ctx.info(f"Retrieved {len(pools)} liquidity pools")
            
            # Calculate total liquidity
            total_liquidity = 0
            for pool in pools:
                liquidity_usd = pool.get("liquidity", {}).get("usd", 0)
                if isinstance(liquidity_usd, (int, float)):
                    total_liquidity += liquidity_usd
            
            # Build markdown table
            table = "| Dex ID | Pair Address | Base/Quote | Price USD | 24h Buys/Sells | 24h Volume | Liquidity USD | Market Cap |\n"
            table += "|--------|--------------|------------|-----------|----------------|------------|---------------|------------|\n"
            
            for pool in pools:
                base_symbol = pool.get("baseToken", {}).get("symbol", "N/A")
                quote_symbol = pool.get("quoteToken", {}).get("symbol", "N/A")
                base_quote = f"{base_symbol}/{quote_symbol}"
                price_usd = pool.get("priceUsd", "N/A")
                txns_h24 = pool.get("txns", {}).get("h24", {})
                buys_sells = f"{txns_h24.get('buys', 0)}/{txns_h24.get('sells', 0)}"
                volume_h24 = pool.get("volume", {}).get("h24", "N/A")
                liquidity_usd = pool.get("liquidity", {}).get("usd", "N/A")
                market_cap = pool.get("marketCap", "N/A")
                
                table += f"| {pool.get('dexId', 'N/A')} | {pool.get('pairAddress', 'N/A')} | {base_quote} | {price_usd} | {buys_sells} | {volume_h24} | {liquidity_usd} | {market_cap} |\n"
            
            # Add total liquidity
            table += f"\n**Total Liquidity USD**: {total_liquidity}"
            
            return table
            
    except httpx.HTTPStatusError as e:
        ctx.error(f"HTTP error fetching liquidity pools: {str(e)}")
        return f"**Error**: HTTP error: {str(e)}"
    except Exception as e:
        ctx.error(f"Error fetching liquidity pools: {str(e)}")
        return f"**Error**: {str(e)}"

# Prompt to guide liquidity pool queries
@mcp.prompt()
def liquidity_pool_query(chain_id: str, token_address: str) -> str:
    """Generate a prompt for querying liquidity pools"""
    return f"""
Please analyze the liquidity pools for token {token_address} on chain {chain_id}.
Use the get_liquidity_pools tool to fetch the data and provide:
1. Number of pools found
2. A markdown table with: dexId, pairAddress, base/quote token symbols, 
   price USD, 24h buy/sell transactions, 24h volume, liquidity USD, market cap
3. Total liquidity USD across all pools
4. Any significant price changes or notable pool metrics
"""

# Main execution
if __name__ == "__main__":
    mcp.run()
