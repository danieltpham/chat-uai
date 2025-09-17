#!/usr/bin/env python3
"""
Run the ChatLas Shiny App via uvicorn
"""

if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting ChatLas Shiny App...")
    print("Make sure the FastAPI server is running on http://localhost:8000")
    print("App will be available at http://localhost:8080")
    print()

    try:
        uvicorn.run(
            "shiny_app:app",
            host="0.0.0.0",
            port=8080,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nShiny app stopped.")
    except Exception as e:
        print(f"Error running Shiny app: {e}")