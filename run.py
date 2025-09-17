#!/usr/bin/env python3
"""
Start the combined ChatLas platform (FastAPI backend + Shiny frontend)
"""
import uvicorn

if __name__ == "__main__":
    print("Starting ChatLas Platform...")
    print("Analytics API: http://localhost:8000/api/")
    print("MCP Endpoint: http://localhost:8000/mcp")
    print("Web Interface: http://localhost:8000/")
    print("API Docs: http://localhost:8000/docs")
    print()

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )