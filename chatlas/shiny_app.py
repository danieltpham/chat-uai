#!/usr/bin/env python3
"""
ChatLas Shiny App - Web interface for the DuckDB Analytics Chatbot
"""

import os
from dotenv import load_dotenv
from chatlas import ChatOpenAI
from shiny import ui, App

# Import data analysis utilities
from tools import data_utils, chain_tools

# Load environment variables
load_dotenv()

# UI setup
app_ui = ui.page_fixed(
    ui.div(
        ui.h1("🚀 ChatLas - Analytics Chatbot", class_="text-center mb-3"),
        ui.p(
            "Connected to DuckDB Analytics API with MCP tools for data analysis",
            class_="text-center text-muted mb-4"
        ),
        ui.chat_ui(id="my_chat"),
        class_="container-fluid"
    ),
    # ui.include_css("""
    # .container-fluid {
    #     max-width: 1200px;
    #     margin: 0 auto;
    #     padding: 20px;
    # }

    # h1 {
    #     color: #2c3e50;
    #     font-weight: 600;
    # }

    # .text-muted {
    #     font-size: 1.1rem;
    # }
    # """)
)

def server(input):
    chat = ui.Chat(
        id="my_chat",
        messages=[
            "Hello! I'm ChatLas, your DuckDB analytics assistant. I can help you analyze sales data, customer information, and product details. Try asking me something like:",
            "• 'What are all the product categories?'",
            "• 'Show me sales by category'",
            "• 'Who are the top 5 customers?'",
            "• 'Analyze weekend vs weekday sales'"
        ],
    )

    # Create MCP provider for the FastAPI backend
    fastapi_mcp_url = "http://localhost:8000/mcp"

    chat_client = ChatOpenAI(
        model="gpt-4o",
        system_prompt="""You are ChatLas, an AI assistant that helps users analyze data from a DuckDB analytics database.
        You have access to MCP tools that can query the FastAPI backend for:
        - Product information and categories (get_products, get_customers, get_dates)
        - Sales data (get_sales, get_sales_by_customer, get_sales_by_product)
        - Pre-built analytics reports (get_sales_by_category, get_sales_by_month, get_top_customers, etc.)
        - Custom SQL queries (execute_sql, get_sql_tables, get_sql_examples)

        Always use the provided MCP tools to fetch data instead of making assumptions.
        Present data in a clear, readable format. When showing lists or tables, format them nicely.
        Be conversational and helpful.

        For product categories specifically, call the get_products tool and extract unique categories from the results."""
    )

    # Initialize MCP tools and local tools on startup
    async def initialize_tools():
        try:
            print("Connecting to MCP server...")
            await chat_client.register_mcp_tools_http_stream_async(url=fastapi_mcp_url)
            print("✓ MCP tools registered successfully")
        except Exception as e:
            print(f"⚠️  Failed to connect to MCP: {e}")
            print("   Continuing without MCP tools.")

        # Register data analysis utilities (for processing the MCP results)
        chat_client.register_tool(data_utils.get_unique_values)
        chat_client.register_tool(data_utils.summarize_numeric_field)
        chat_client.register_tool(data_utils.count_by_field)
        chat_client.register_tool(data_utils.filter_data)
        chat_client.register_tool(data_utils.group_by_field)
        chat_client.register_tool(data_utils.sort_data)

        # Register chainable tools that combine MCP results with analysis
        chat_client.register_tool(chain_tools.extract_unique_categories)
        chat_client.register_tool(chain_tools.analyze_products_data)
        chat_client.register_tool(chain_tools.analyze_customer_data)
        chat_client.register_tool(chain_tools.analyze_sales_data)
        chat_client.register_tool(chain_tools.compare_categories)
        chat_client.register_tool(chain_tools.generate_insights)

    # Initialize tools when the server starts
    import asyncio
    asyncio.create_task(initialize_tools())

    @chat.on_user_submit
    async def handle_user_input(user_input: str):
        try:
            # Stream the response using ChatOpenAI
            response = await chat_client.stream_async(user_input)
            await chat.append_message_stream(response)
        except Exception as e:
            await chat.append_message(f"Error: {str(e)}")

app = App(app_ui, server)