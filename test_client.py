import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_server():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List tools
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")
            
            # Test create_chart_config
            print("\nTesting create_chart_config...")
            result = await session.call_tool("create_chart_config", arguments={
                "chart_type": "bar",
                "labels": ["Red", "Blue"],
                "datasets": [{"label": "Votes", "data": [12, 19]}]
            })
            print(f"Result length: {len(result.content[0].text)}")
            print("Sample output:")
            print(result.content[0].text[:200] + "...")

            # Test get_chart_templates
            print("\nTesting get_chart_templates...")
            result = await session.call_tool("get_chart_templates", arguments={})
            print(f"Result length: {len(result.content[0].text)}")

if __name__ == "__main__":
    asyncio.run(test_server())
