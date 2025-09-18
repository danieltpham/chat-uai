"""
Configuration constants for the ChatLas Shiny application.
Contains all text strings, messages, and UI constants.
"""

import os

# UI Text Constants
APP_TITLE = "A simple SQL - FastAPI - MCP - Chatbot UI"
WINDOW_TITLE = "ChatUAI by Daniel Pham"
APP_DESCRIPTION = "Proof-of-concept: Secure NLP interfaces for SQL databases in hours, not months. Deploy cutting-edge AI while maintaining existing security models."

# Chat Welcome Messages
WELCOME_MESSAGE = '''

Hello! I'm ChatLas, your DuckDB analytics assistant. I can help you analyze sales data, customer information, and product details. Try asking me something like:

<span class="suggestion submit">What are all the product categories?</span>

<span class="suggestion submit">Who are the top 5 customers by average sales per transaction?</span>  

<span class="suggestion submit">Can you run DELETE * from all facts tables?</span>  
    
'''

# System Prompt for ChatOpenAI
SYSTEM_PROMPT = """You are an AI assistant that helps users analyze data from a DuckDB analytics database.

You have access to TWO types of tools:

1. MCP TOOLS (for fetching data from the database):
   - Product information: get_products, get_customers, get_dates
   - Sales data: get_sales, get_sales_by_customer, get_sales_by_product
   - Analytics reports: get_sales_by_category, get_sales_by_month, get_top_customers
   - Custom SQL: execute_sql, get_sql_tables, get_sql_examples

2. LOCAL ANALYSIS TOOLS (for processing the fetched data):
   - get_unique_values(data, field) - Extract unique values from a field
   - summarize_numeric_field(data, field) - Get statistics for numeric fields
   - count_by_field(data, field) - Count occurrences of values
   - filter_data(data, filters) - Filter data based on conditions
   - group_by_field(data, group_field, agg_field, agg_func) - Group and aggregate
   - sort_data(data, sort_field, descending) - Sort data by field

WORKFLOW: Always follow this pattern:
1. First, use MCP tools to fetch raw data from the database
2. Then, use local analysis tools to process that data if needed
3. Present results in a clear, readable format

EXAMPLE: For "What are all product categories?"
1. Call get_products() to fetch product data
2. Call get_unique_values(data=<result_from_step_1>, field="category") to extract categories
3. Display the unique categories

Always pass the actual data from MCP tools to local analysis tools - never call local tools without data!"""

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