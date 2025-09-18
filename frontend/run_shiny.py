#!/usr/bin/env python3
"""
Run the ChatLas Shiny App via uvicorn
"""

import signal
import sys
import asyncio

if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting ChatLas Shiny App...")
    print("Make sure the FastAPI server is running on http://localhost:8000")
    print("App will be available at http://localhost:8080")
    print("Press Ctrl+C to stop")
    print()

    # Setup signal handlers for clean shutdown
    def signal_handler(signum, frame):
        print("\n🛑 Shutting down gracefully...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        config = uvicorn.Config(
            "shiny_app:app",
            host="0.0.0.0",
            port=8080,
            reload=False,
            log_level="info",
            # Add shutdown settings
            timeout_keep_alive=0,
            timeout_graceful_shutdown=5
        )
        server = uvicorn.Server(config)
        server.run()
    except KeyboardInterrupt:
        print("\nShiny app stopped.")
    except Exception as e:
        print(f"Error running Shiny app: {e}")
    finally:
        print("✅ Cleanup complete.")