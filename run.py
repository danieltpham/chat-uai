#!/usr/bin/env python3
"""
Start the combined ChatLas platform (FastAPI backend + Shiny frontend)
"""
import os
import uvicorn

if __name__ == "__main__":
    # Get port from environment variable or default to 8000
    port = int(os.getenv("PORT", 8000))

    print("Starting ChatLas Platform...")
    print(f"Analytics API: http://localhost:{port}/api/")
    print(f"MCP Endpoint: http://localhost:{port}/mcp")
    print(f"Web Interface: http://localhost:{port}/")
    print(f"API Docs: http://localhost:{port}/docs")
    print(f"Health Check: http://localhost:{port}/health")
    print()

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )