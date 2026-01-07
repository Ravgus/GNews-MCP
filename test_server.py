#!/usr/bin/env python3
"""
Test script for GNews MCP Server
Run this to verify the server is working correctly
"""

import os
import sys
import asyncio
import json
from pathlib import Path

# Add the current directory to the path to import main
sys.path.insert(0, str(Path(__file__).parent))

from main import mcp, get_api_key


async def test_server():
    """Test the GNews MCP server functionality"""
    print("🧪 Testing GNews MCP Server")
    print("=" * 50)

    # Test 1: Test tools are registered (this doesn't require API key)
    print("\n1. Testing tool registration...")
    tools = await mcp.list_tools()
    tool_names = [tool.name for tool in tools]
    expected_tools = ["search_news", "get_top_headlines"]

    for tool_name in expected_tools:
        if tool_name in tool_names:
            print(f"✅ Tool '{tool_name}' registered")
        else:
            print(f"❌ Tool '{tool_name}' not found")
            return False

    # Test 2: Check API key (optional for basic functionality)
    print("\n2. Testing API key configuration...")
    try:
        api_key = get_api_key()
        print(f"✅ API key found: {api_key[:8]}...")
        api_key_available = True
    except ValueError as e:
        print(f"⚠️  API key not configured: {e}")
        print("💡 Set GNEWS_API_KEY environment variable for full functionality")
        api_key_available = False

    print("\n" + "=" * 50)
    if api_key_available:
        print("✅ All tests passed! Server is ready to use.")
    else:
        print("⚠️  Server structure OK, but API key needed for full functionality")
    print("\n💡 Next steps:")
    print("1. Add this server to your Claude Desktop config")
    print("2. Set the GNEWS_API_KEY environment variable")
    print("3. Start using the news search capabilities!")

    return True


def test_environment():
    """Test environment setup"""
    print("🔧 Testing Environment Setup")
    print("=" * 50)

    # Check Python version
    print(f"Python version: {sys.version}")

    # Check required modules
    required_modules = ["mcp", "httpx", "pydantic"]
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} imported successfully")
        except ImportError:
            print(f"❌ {module} not found - run: pip install {module}")
            return False

    # Check if we can import the main module
    try:
        import main
        print("✅ Main module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import main module: {e}")
        return False

    return True


if __name__ == "__main__":
    print("🚀 GNews MCP Server Test Suite")
    print("=" * 50)

    # Test environment first
    if not test_environment():
        print("\n❌ Environment test failed")
        sys.exit(1)

    # Test server functionality
    try:
        result = asyncio.run(test_server())
        if result:
            print("\n🎉 All tests completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test suite error: {e}")
        sys.exit(1)