"""
Configuration settings for the DuckDB Analytics API
"""
import os
from typing import Optional

class Settings:
    """Application settings"""
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "duckdb:///analytics.db")
    TEST_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL", "duckdb:///:memory:")
    
    # API settings
    API_TITLE: str = "DuckDB Analytics API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Analytics API with DuckDB backend and star schema"
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Sample data settings
    SAMPLE_CUSTOMERS: int = int(os.getenv("SAMPLE_CUSTOMERS", "100"))
    SAMPLE_PRODUCTS: int = int(os.getenv("SAMPLE_PRODUCTS", "50"))
    SAMPLE_SALES: int = int(os.getenv("SAMPLE_SALES", "1000"))

# Global settings instance
settings = Settings()