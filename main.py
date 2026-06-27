"""
Revenue OS API Server — Entry point for deployment.
PORT is read from environment with fallback to 8080.
"""

import os
import uvicorn
from api.webhook import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)
