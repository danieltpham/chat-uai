"""
Tools for extracting information from README.md and documentation files
"""

import base64
import re
import mermaid as md
from shiny import ui

def create_mermaid_image(mermaid_code: str):
    """
    Create a Shiny UI image element from mermaid code.

    Args:
        mermaid_code (str): The mermaid diagram code

    Returns:
        ui.img: A Shiny UI image element with the mermaid diagram
    """
    img_bytes = md.Mermaid(mermaid_code).img_response.content # type: ignore
    html_element = ui.img(
        src=f"data:image/jpeg;base64,{base64.b64encode(img_bytes).decode('utf-8')}",
        width="100%"
    )
    return html_element

def extract_mermaid_architecture_diagram():
    """
    Extract the architecture mermaid diagram of this project from README.md.

    Returns:
        A MermaidToolResult containing the diagram or error information
    """
    try:
        # Read the README.md file
        with open("README.md", "r", encoding="utf-8") as file:
            content = file.read()

        # Find the architecture mermaid diagram (first one after "Architecture Overview")
        # Look for the pattern: ```mermaid ... ```
        pattern = r"## 🏗️ Architecture Overview.*?```mermaid\n(.*?)\n```"
        match = re.search(pattern, content, re.DOTALL)

        if match:
            mermaid_code = match.group(1).strip()
            return {"mermaid_img": mermaid_code}
        else:
            return "No architecture diagram found in README.md"

    except Exception as e:
        print(e)
        return f"Error extracting architecture diagram: {str(e)}"

def extract_database_schema_diagram():
    """
    Extract the database schema mermaid diagram from README.md.

    Returns:
        A MermaidToolResult containing the schema diagram or error information
    """
    try:
        # Read the README.md file
        with open("README.md", "r", encoding="utf-8") as file:
            content = file.read()

        # Find the database schema mermaid diagram (after "Star Schema Design")
        # Look for the pattern: ```mermaid ... ```
        pattern = r"## 📊 Star Schema Design.*?```mermaid\n(.*?)\n```"
        match = re.search(pattern, content, re.DOTALL)

        if match:
            mermaid_code = match.group(1).strip()
            return {"mermaid_img": mermaid_code}
        else:
            return "No database schema diagram found in README.md"

    except Exception as e:
        print(f"Error extracting database schema diagram: {e}")
        return f"Error extracting database schema diagram: {str(e)}"