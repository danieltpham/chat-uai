from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from backend.api import dimensions, facts, analytics, sql
from backend.database import create_tables, populate_sample_data

app = FastAPI(title="DuckDB Analytics API", version="1.0.0")

# Include routers
app.include_router(dimensions.router, prefix="/api/v1/dimensions", tags=["dimensions"])
app.include_router(facts.router, prefix="/api/v1/facts", tags=["facts"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(sql.router, prefix="/api/v1", tags=["sql"])

@app.on_event("startup")
async def startup_event():
    """Initialize database and populate with sample data"""
    create_tables()
    populate_sample_data()

@app.get("/")
async def root():
    return {"message": "DuckDB Analytics API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

mcp = FastApiMCP(
    app,
    exclude_tags=["admin", "internal"]
)
mcp.mount_http()