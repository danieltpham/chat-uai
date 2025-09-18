"""
Configuration constants for the ChatLas Shiny application.
Contains all text strings, messages, and UI constants.
"""

import os

# UI Text Constants
APP_TITLE = "A simple SQL - FastAPI - MCP - Chatbot UI"
WINDOW_TITLE = "ChatUAI by Daniel Pham"
APP_DESCRIPTION = "Connected to DuckDB Analytics API with MCP tools for data analysis"

# Chat Welcome Messages
WELCOME_MESSAGE = '''

Hello! I'm ChatLas, your DuckDB analytics assistant. I can help you analyze sales data, customer information, and product details. Try asking me something like:

<span class="suggestion submit">What are all the product categories?</span>

<span class="suggestion submit">Show me sales by category</span>

<span class="suggestion submit">Who are the top 5 customers?</span>  
    
'''

# System Prompt for ChatOpenAI
SYSTEM_PROMPT = """You are an AI assistant that helps users analyze data from a DuckDB analytics database.
        You have access to MCP tools that can query the FastAPI backend for:
        - Product information and categories (get_products, get_customers, get_dates)
        - Sales data (get_sales, get_sales_by_customer, get_sales_by_product)
        - Pre-built analytics reports (get_sales_by_category, get_sales_by_month, get_top_customers, etc.)
        - Custom SQL queries (execute_sql, get_sql_tables, get_sql_examples)

        Always use the provided MCP tools to fetch data instead of making assumptions.
        Present data in a clear, readable format. When showing lists or tables, format them nicely.
        Be conversational and helpful.

        For product categories specifically, call the get_products tool and extract unique categories from the results."""

# Status Messages
MCP_CONNECTING_MESSAGE = "Connecting to MCP server..."
MCP_SUCCESS_MESSAGE = "✓ MCP tools registered successfully"
MCP_FAILURE_MESSAGE = "⚠️  Failed to connect to MCP: {error}"
MCP_CONTINUE_MESSAGE = "   Continuing without MCP tools."

# Configuration
MODEL_NAME = "gpt-4o"
MCP_URL = f"http://127.0.0.1:{os.getenv('PORT', '8000')}/mcp"
CHAT_ID = "my_chat"

# CSS Classes
CSS_CLASSES = {
    "title": "text-center mb-3",
    "description": "text-center text-muted mb-4",
    "container": "container-fluid",
    "chatui": "chatui"
}