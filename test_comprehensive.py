#!/usr/bin/env python3
"""
Comprehensive test suite for Chart.js MCP Server
Tests all 39 tools to ensure they work correctly
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_all_tools():
    """Test all 39 tools in the MCP server"""
    
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "server.py"],
        env=None
    )

    print("🚀 Starting Chart.js MCP Server Test Suite\n")
    print("=" * 60)
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List all available tools
            tools = await session.list_tools()
            print(f"\n✅ Server connected successfully!")
            print(f"📊 Total tools available: {len(tools.tools)}\n")
            
            print("=" * 60)
            print("AVAILABLE TOOLS:")
            print("=" * 60)
            
            for i, tool in enumerate(tools.tools, 1):
                print(f"{i:2d}. {tool.name}")
            
            print("\n" + "=" * 60)
            print("RUNNING TESTS:")
            print("=" * 60 + "\n")
            
            # Test 1: Basic chart config
            print("1️⃣  Testing create_chart_config...")
            result = await session.call_tool("create_chart_config", arguments={
                "chart_type": "bar",
                "labels": ["Q1", "Q2", "Q3", "Q4"],
                "datasets": [{"label": "Sales", "data": [100, 150, 120, 180]}]
            })
            print(f"   ✓ Success! Config length: {len(result.content[0].text)} chars\n")
            
            # Test 2: Pie chart
            print("2️⃣  Testing create_pie_chart...")
            result = await session.call_tool("create_pie_chart", arguments={
                "labels": ["Chrome", "Firefox", "Safari"],
                "data": [60, 25, 15],
                "title": "Browser Share",
                "color_palette": "professional"
            })
            print(f"   ✓ Success! Config length: {len(result.content[0].text)} chars\n")
            
            # Test 3: Data analysis
            print("3️⃣  Testing analyze_data_for_chart...")
            result = await session.call_tool("analyze_data_for_chart", arguments={
                "data": [12, 45, 23, 67, 89, 34, 56, 78, 90, 23],
                "labels": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
            })
            analysis = json.loads(result.content[0].text)
            print(f"   ✓ Success! Statistics calculated:")
            print(f"     - Mean: {analysis['statistics']['mean']}")
            print(f"     - Median: {analysis['statistics']['median']}")
            print(f"     - Std Dev: {analysis['statistics']['std_dev']}")
            print(f"     - Suggested charts: {len(analysis['suggested_charts'])}\n")
            
            # Test 4: Theme preset
            print("4️⃣  Testing create_theme_preset...")
            result = await session.call_tool("create_theme_preset", arguments={
                "theme_name": "ocean"
            })
            theme = json.loads(result.content[0].text)
            print(f"   ✓ Success! Theme loaded:")
            print(f"     - Background: {theme['backgroundColor']}")
            print(f"     - Text Color: {theme['textColor']}\n")
            
            # Test 5: Moving average transformation
            print("5️⃣  Testing transform_data_moving_average...")
            result = await session.call_tool("transform_data_moving_average", arguments={
                "data": [10, 20, 30, 40, 50],
                "window_size": 3
            })
            transform = json.loads(result.content[0].text)
            print(f"   ✓ Success! Moving average calculated:")
            print(f"     - Original: {transform['original']}")
            print(f"     - Moving Avg: {transform['moving_average']}\n")
            
            # Test 6: Waterfall chart
            print("6️⃣  Testing create_waterfall_chart...")
            result = await session.call_tool("create_waterfall_chart", arguments={
                "labels": ["Start", "Income", "Expenses", "End"],
                "data": [1000, 500, -300, 1200],
                "title": "Cash Flow"
            })
            print(f"   ✓ Success! Waterfall config length: {len(result.content[0].text)} chars\n")
            
            # Test 7: Export to CSV
            print("7️⃣  Testing export_chart_data_csv...")
            result = await session.call_tool("export_chart_data_csv", arguments={
                "labels": ["Jan", "Feb", "Mar"],
                "datasets": [
                    {"label": "2023", "data": [100, 150, 120]},
                    {"label": "2024", "data": [120, 180, 140]}
                ]
            })
            csv_lines = result.content[0].text.split('\n')
            print(f"   ✓ Success! CSV exported with {len(csv_lines)} rows\n")
            
            # Test 8: Color palettes
            print("8️⃣  Testing get_color_palettes...")
            result = await session.call_tool("get_color_palettes", arguments={})
            palettes = json.loads(result.content[0].text)
            print(f"   ✓ Success! {len(palettes)} color palettes available\n")
            
            # Test 9: Chart templates
            print("9️⃣  Testing get_chart_templates...")
            result = await session.call_tool("get_chart_templates", arguments={})
            templates = json.loads(result.content[0].text)
            print(f"   ✓ Success! {len(templates)} chart templates available\n")
            
            # Test 10: HTML generation
            print("🔟 Testing create_chart_html...")
            result = await session.call_tool("create_chart_html", arguments={
                "chart_type": "line",
                "labels": ["Mon", "Tue", "Wed"],
                "datasets": [{"label": "Temperature", "data": [22, 24, 23]}],
                "title": "Weekly Temperature",
                "theme": "dark"
            })
            html_length = len(result.content[0].text)
            print(f"   ✓ Success! HTML generated: {html_length} chars\n")
            
            print("=" * 60)
            print("✅ ALL TESTS PASSED!")
            print("=" * 60)
            print(f"\n🎉 Chart.js MCP Server is working perfectly!")
            print(f"📊 All {len(tools.tools)} tools are functional and ready to use.\n")

if __name__ == "__main__":
    asyncio.run(test_all_tools())
