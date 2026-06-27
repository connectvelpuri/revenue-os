#!/usr/bin/env python3
"""Start script for Railway deployment.
Reads PORT from environment and passes to uvicorn.
Railway sets PORT automatically.
"""
import os
import sys
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"Starting Revenue OS on {host}:{port}")
    sys.stdout.flush()
    uvicorn.run(
        "api.webhook:app",
        host=host,
        port=port,
        log_level=os.environ.get("LOG_LEVEL", "info").lower(),
    )
