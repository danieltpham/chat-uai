#!/usr/bin/env python3
"""
ChatLas - OpenAI Terminal Style Chatbot
A terminal-based chatbot that interfaces with the FastAPI analytics backend
"""

import os
from dotenv import load_dotenv
from chatlas import ChatOpenAI
import asyncio

# Import data analysis utilities (we'll keep these for data processing)
from tools import data_utils, chain_tools

# Load environment variables
load_dotenv()

async def main():
    """Main entry point"""

    # Create MCP provider for the FastAPI backend
    fastapi_mcp_url = "http://localhost:8000/mcp"

    # Create chat instance with MCP and system prompt
    chat = ChatOpenAI(
        model="gpt-4",
        system_prompt="""You are ChatLas, an AI assistant that helps users analyze data from a DuckDB analytics database.
        You have access to MCP tools that can query the FastAPI backend for:
        - Product information and categories (/api/v1/dimensions/products, /api/v1/dimensions/customers, /api/v1/dimensions/dates)
        - Sales data (/api/v1/facts/sales)
        - Pre-built analytics reports (/api/v1/analytics/*)
        - Custom SQL queries (/api/v1/sql)

        Always use the provided MCP tools to fetch data instead of making assumptions.
        Present data in a clear, readable format. When showing lists or tables, format them nicely.
        Be conversational and helpful.

        For product categories specifically, call the /api/v1/dimensions/products endpoint and extract unique categories from the results."""
    )
    
    try:
        print("Connecting to MCP server...")
        await asyncio.wait_for(
            chat.register_mcp_tools_http_stream_async(url=fastapi_mcp_url),
            timeout=10.0  # 10 second timeout
        )
        print("✓ MCP tools registered successfully")
    except asyncio.TimeoutError:
        print("⚠️  MCP connection timed out. Continuing without MCP tools.")
        print("   Make sure the FastAPI server is running on http://localhost:8000")
    except Exception as e:
        print(f"⚠️  Failed to connect to MCP: {e}")
        print("   Continuing without MCP tools.")

    # Register data analysis utilities (for processing the MCP results)
    chat.register_tool(data_utils.get_unique_values)
    chat.register_tool(data_utils.summarize_numeric_field)
    chat.register_tool(data_utils.count_by_field)
    chat.register_tool(data_utils.filter_data)
    chat.register_tool(data_utils.group_by_field)
    chat.register_tool(data_utils.sort_data)

    # Register chainable tools that combine MCP results with analysis
    chat.register_tool(chain_tools.extract_unique_categories)
    chat.register_tool(chain_tools.analyze_products_data)
    chat.register_tool(chain_tools.analyze_customer_data)
    chat.register_tool(chain_tools.analyze_sales_data)
    chat.register_tool(chain_tools.compare_categories)
    chat.register_tool(chain_tools.generate_insights)

    print("🚀 ChatLas - Analytics Chatbot")
    print("Connected to DuckDB Analytics API")
    print("Type 'quit' or 'exit' to stop\n")

    try:
        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye! 👋")
                    break

                if not user_input:
                    continue

                # Use chatlas async to handle the conversation
                await chat.chat_async(user_input)
                print()

            except KeyboardInterrupt:
                print("\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"Error: {e}")

    finally:
        # Cleanup MCP tools when exiting
        try:
            await chat.cleanup_mcp_tools()
        except:
            pass  # Ignore cleanup errors

asyncio.run(main())