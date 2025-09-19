#!/usr/bin/env python3
"""
ChatLas Shiny App - Web interface for the DuckDB Analytics Chatbot
"""

import base64
from dotenv import load_dotenv
from chatlas import ChatOpenAI, ContentToolRequest, ContentToolResult
from faicons import icon_svg
from shiny import ui, App

# Import data analysis utilities
from .tools import data_utils, chain_tools, readme_tools
from .config import (
    APP_TITLE, APP_DESCRIPTION, WELCOME_MESSAGE,
    SYSTEM_PROMPT, MCP_CONNECTING_MESSAGE, MCP_SUCCESS_MESSAGE,
    MCP_FAILURE_MESSAGE, MCP_CONTINUE_MESSAGE, MODEL_NAME, MCP_URL,
    CHAT_ID, CSS_CLASSES, WINDOW_TITLE
)
from .theme import UAI_THEME

# Load environment variables
load_dotenv()

# UI setup
app_ui = ui.page_fixed(
    ui.div(
        ui.h1(APP_TITLE, class_=CSS_CLASSES["title"]),
        ui.p(
            APP_DESCRIPTION,
            class_=CSS_CLASSES["description"]
        ),
        ui.chat_ui(id=CHAT_ID,
                    messages=[WELCOME_MESSAGE],
                   icon_assistant=icon_svg("twitch"),),
    ),
    theme=UAI_THEME,
    # full_width=True,
    window_title=WINDOW_TITLE
)

def server(input):
    chat = ui.Chat(id=CHAT_ID)

    # Create MCP provider for the FastAPI backend
    fastapi_mcp_url = MCP_URL

    chat_client = ChatOpenAI(
        model=MODEL_NAME,
        system_prompt=SYSTEM_PROMPT
    )

    # Store connections for cleanup
    connections = []

    # Initialize MCP tools and local tools on startup
    async def initialize_tools():
        try:
            print(MCP_CONNECTING_MESSAGE)
            connection = await chat_client.register_mcp_tools_http_stream_async(url=fastapi_mcp_url)
            if connection:
                connections.append(connection)
            print(MCP_SUCCESS_MESSAGE)
        except Exception as e:
            print(MCP_FAILURE_MESSAGE.format(error=e))
            print(MCP_CONTINUE_MESSAGE)

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

        # Register README tools for documentation extraction
        chat_client.register_tool(readme_tools.extract_mermaid_architecture_diagram)
        chat_client.register_tool(readme_tools.extract_database_schema_diagram)

    # Initialize tools when the server starts
    import asyncio
    asyncio.create_task(initialize_tools())

    @chat.on_user_submit
    async def handle_user_input(user_input: str):
        try:
            # Stream the response using ChatOpenAI
            response = await chat_client.stream_async(user_input, content="all")
            
            import htmltools, mermaid as md
            async def filtered_stream():
                skip_rest = False
                async for chunk in response:
                    # Skip displaying of the request
                    if isinstance(chunk, ContentToolRequest):
                        continue
                    # Display custom HTML for custom json-like ContentToolResult
                    # HACK: Render custom contenttoolresult as html/img, then skip the rest
                    if isinstance(chunk, ContentToolResult):
                        if isinstance(chunk.value, dict):
                            # skip_rest = True
                            if 'mermaid_img' in chunk.value: # mermaid code as string
                                mermaid_code = chunk.value.get('mermaid_img', "")
                                html_element = readme_tools.create_mermaid_image(mermaid_code)
                            yield htmltools.HTML(html_element)
                    elif not skip_rest:
                        yield chunk
                    else:
                        continue
            
            await chat.append_message_stream(filtered_stream())
            
        except Exception as e:
            await chat.append_message(f"Error: {str(e)}")

app = App(app_ui, server)