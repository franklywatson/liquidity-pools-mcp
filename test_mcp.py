#!/usr/bin/env python3
"""
Simple test script to verify the MCP server is running correctly.
"""

import requests
import json

def test_mcp_server():
    """Test the MCP server health endpoint."""
    base_url = "http://localhost:8000"

    try:
        # Test basic connectivity
        response = requests.get(f"{base_url}/mcp", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")

        if response.status_code == 200:
            print("✅ MCP Server is running successfully!")
            print(f"Response: {response.text[:200]}...")
        else:
            print(f"❌ Server returned status code: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to MCP server. Make sure it's running on http://localhost:8000")
    except requests.exceptions.Timeout:
        print("❌ Connection timeout. Server may be starting up...")
    except Exception as e:
        print(f"❌ Error testing server: {e}")

if __name__ == "__main__":
    test_mcp_server()