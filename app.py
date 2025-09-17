#!/usr/bin/env python3
"""
Combined FastAPI backend with Shiny Python frontend in a single uvicorn app
Served by `uvicorn.run("app:app", host='127.0.0.1', port=8000, reload=True)`

Routes:
- /api/*     - FastAPI backend with analytics API
- /mcp       - Model Context Protocol endpoint
- /*         - Shiny web application (ChatLas frontend)
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

# Import FastAPI backend components
from backend.api import dimensions, facts, analytics, sql
from backend.database import create_tables, populate_sample_data

# Import Shiny frontend app
from frontend.shiny_app import app as shiny_app

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and populate with sample data on startup"""
    import os
    if not os.path.exists("analytics.db"):
        create_tables()
        populate_sample_data()
    yield

# Create the main FastAPI app
app = FastAPI(
    title="ChatLas - From UI to U-AI Platform",
    version="1.0.0",
    description="AI-powered analytics platform with secure NLP data access",
    lifespan=lifespan
)

# Include API routers directly in main app so MCP can see them
app.include_router(dimensions.router, prefix="/api/v1/dimensions", tags=["dimensions"])
app.include_router(facts.router, prefix="/api/v1/facts", tags=["facts"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(sql.router, prefix="/api/v1", tags=["sql"])

# Setup MCP integration - must be before mounting Shiny
mcp = FastApiMCP(
    app,
    exclude_tags=["admin", "internal"]
)
mcp.mount_http()  # This creates /mcp endpoint

# Add main app health check
@app.get("/health")
async def main_health_check():
    return {"status": "healthy", "service": "chatlas-platform"}

# Add platform info endpoint
@app.get("/info")
async def platform_info():
    return {
        "platform": "ChatLas - From UI to U-AI",
        "version": "1.0.0",
        "endpoints": {
            "analytics_api": "/api/v1/",
            "api_docs": "/docs",
            "mcp_endpoint": "/mcp",
            "web_app": "/app/",
            "health": "/health"
        },
        "description": "AI-powered analytics platform with secure NLP data access"
    }

# Add root redirect to Shiny app
from fastapi.responses import RedirectResponse

@app.get("/")
async def root():
    return RedirectResponse(url="/app/")

# Mount the Shiny app at /app path
app.mount("/app", shiny_app)