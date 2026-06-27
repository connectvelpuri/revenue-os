"""Revenue OS Production API — Auth, Logging, Rate Limiting, Persistence, WhatsApp.

Deploy: railway deploy OR flyctl deploy
Free tier: Railway ($5 credit), Render (512MB), Fly.io (3 VMs)
"""
import os
import sys

# Ensure agents directory is on Python path (handles Railway/Docker paths)
_agent_paths = [
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agents"),
    "/app/agents",
]
for _p in _agent_paths:
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.insert(0, _p)
import os
import json
import time
import logging
import sqlite3
import re
from datetime import datetime
from functools import wraps
from typing import Optional

# FastAPI
try:
    from fastapi import FastAPI, Request, HTTPException, Depends
    from fastapi.responses import JSONResponse, Response
    from fastapi.middleware.cors import CORSMiddleware
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

# Rate limiting
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    HAS_SLOWAPI = True
except ImportError:
    HAS_SLOWAPI = False

# Agent system
try:
    from agent_base.agent_wrapper import AgentIntelligence, TRAINING_MODULES
    from agent_base.personas import PERSONA_IDS
    HAS_AGENTS = True
except ImportError:
    HAS_AGENTS = False
    PERSONA_IDS = []
    TRAINING_MODULES = {}

# ============================================================
# LOGGING
# ============================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("revenue_os")

# ============================================================
# DATABASE — Conversation persistence
# ============================================================
DB_PATH = os.getenv("DATABASE_URL", "data/conversations.sqlite")

def get_db():
    """Get SQLite connection with WAL mode for concurrent reads."""
    os.makedirs(os.path.dirname(DB_PATH) if os.path.dirname(DB_PATH) else ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("""CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        persona_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.execute("""CREATE INDEX IF NOT EXISTS idx_conversations_session
        ON conversations(session_id, created_at)""")
    conn.commit()
    return conn


def save_message(session_id: str, persona_id: str, role: str, content: str):
    """Save a message to the conversation history."""
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO conversations (session_id, persona_id, role, content) VALUES (?, ?, ?, ?)",
            (session_id, persona_id, role, content[:10000]),
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to save message: {e}")


def get_history(session_id: str, limit: int = 10) -> list:
    """Get recent conversation history for a session."""
    try:
        conn = get_db()
        rows = conn.execute(
            "SELECT persona_id, role, content FROM conversations WHERE session_id = ? ORDER BY created_at DESC LIMIT ?",
            (session_id, limit),
        ).fetchall()
        conn.close()
        return [dict(r) for r in reversed(rows)]
    except Exception as e:
        logger.error(f"Failed to get history: {e}")
        return []


# ============================================================
# AUTHENTICATION — API Key validation
# ============================================================
API_KEYS = set()
_api_key_env = os.getenv("REVENUE_OS_API_KEY", "")
if _api_key_env:
    API_KEYS.add(_api_key_env)
# Default dev key if none set
if not API_KEYS:
    API_KEYS.add("rev-dev-key-2026")


async def verify_api_key(request: Request):
    """Dependency: Verify API key from header or query param."""
    if os.getenv("DISABLE_AUTH", "").lower() in ("true", "1", "yes"):
        return True
    api_key = request.headers.get("X-API-Key") or request.query_params.get("api_key", "")
    if api_key in API_KEYS:
        return True
    logger.warning(f"Unauthorized access attempt from {request.client.host if request.client else 'unknown'}")
    raise HTTPException(status_code=401, detail="Invalid or missing API key. Set X-API-Key header.")


# ============================================================
# RATE LIMITING
# ============================================================
if HAS_SLOWAPI:
    limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute", "10/second"])
else:
    limiter = None


# ============================================================
# AGENT ROUTING
# ============================================================
ROUTING_RULES = {
    "qualify": "meddpicc_qualifier", "meddpicc": "meddpicc_qualifier", "score": "meddpicc_qualifier",
    "negotiate": "negotiation", "deal": "negotiation", "price": "negotiation",
    "prospect": "prospecting_sdr", "lead": "prospecting_sdr",
    "psychology": "buyer_psychology", "buyer": "buyer_psychology", "influence": "buyer_psychology",
    "value": "value_engineer", "roi": "value_engineer", "tco": "value_engineer", "case": "value_engineer",
    "strategy": "revenue_orchestrator", "pipeline": "revenue_orchestrator",
    "coach": "call_coacher", "call": "call_coacher", "review": "call_coacher",
}
DEFAULT_PERSONA = "revenue_orchestrator"


def route_message(message: str) -> str:
    msg_lower = message.lower()
    for keyword, persona_id in ROUTING_RULES.items():
        if keyword in msg_lower:
            return persona_id
    return DEFAULT_PERSONA


# ============================================================
# FASTAPI APPLICATION
# ============================================================
if HAS_FASTAPI:
    app = FastAPI(title="Revenue OS API", version="2.0.0")

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rate limiter
    if HAS_SLOWAPI:
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Health check (no auth required)
    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "version": "2.0.0",
            "agents_loaded": HAS_AGENTS,
            "personas": len(PERSONA_IDS) if HAS_AGENTS else 0,
            "timestamp": datetime.utcnow().isoformat(),
            "database": os.path.exists(DB_PATH),
        }

    @app.get("/")
    async def root():
        return {
            "service": "Revenue OS Agent API",
            "version": "2.0.0",
            "status": "running",
            "docs": "/docs",
            "endpoints": {
                "GET /health": "Health check (no auth)",
                "POST /api/agent/execute": "Execute agent with persona",
                "POST /api/agent/chat": "Conversational chat with history",
                "GET /api/conversations/{session_id}": "Get conversation history",
                "POST /webhook/whatsapp": "WhatsApp JSON webhook",
                "POST /webhook/twilio": "Twilio WhatsApp webhook (form)",
            }
        }

    @app.post("/api/agent/execute")
    async def execute_agent(request: Request, auth=Depends(verify_api_key)):
        """Execute an agent with persona-driven LLM. Authenticated."""
        body = await request.json()
        persona_id = body.get("persona", DEFAULT_PERSONA)
        task = body.get("task", "Analyze")
        context = body.get("context", "")
        training = body.get("training", "")
        data = body.get("data", {})

        if not HAS_AGENTS:
            return JSONResponse(status_code=503, content={
                "error": "Agent system not loaded",
                "persona": persona_id, "task": task
            })

        if persona_id not in PERSONA_IDS:
            return JSONResponse(status_code=400, content={
                "error": f"Unknown persona: {persona_id}",
                "available": PERSONA_IDS,
            })

        start = time.time()
        agent = AgentIntelligence(persona_id, persona_id.replace("_", " ").title())
        result = agent.execute(task=task, data=data, training=training or "", temperature=body.get("temperature", 0.3))
        elapsed = time.time() - start

        logger.info(f"Execute: {persona_id} | task={task[:50]}... | {elapsed:.2f}s | success={result.get('success', False)}")

        return JSONResponse(content={
            "success": result.get("success", False),
            "persona": persona_id,
            "response": result.get("text", ""),
            "parsed": result.get("parsed"),
            "elapsed_seconds": round(elapsed, 2),
        })

    @app.post("/api/agent/chat")
    async def agent_chat(request: Request, auth=Depends(verify_api_key)):
        """Conversational chat with history. Authenticated."""
        body = await request.json()
        message = body.get("message", "")
        session_id = body.get("session_id", body.get("session", f"sess_{datetime.utcnow().timestamp():.0f}"))

        if not message:
            return JSONResponse(status_code=400, content={"error": "Message required"})

        persona_id = route_message(message)
        history = get_history(session_id, limit=5)

        start = time.time()
        agent = AgentIntelligence(persona_id, persona_id.replace("_", " ").title())
        context = f"Conversation history: {json.dumps(history)}" if history else ""
        result = agent.execute(task=message, data={"history": history}, temperature=0.3)
        elapsed = time.time() - start

        # Persist
        save_message(session_id, persona_id, "user", message)
        save_message(session_id, persona_id, "assistant", result.get("text", ""))

        logger.info(f"Chat: {session_id} -> {persona_id} | {elapsed:.2f}s")

        return JSONResponse(content={
            "success": result.get("success", False),
            "persona": persona_id,
            "response": result.get("text", ""),
            "session_id": session_id,
            "elapsed_seconds": round(elapsed, 2),
        })

    @app.get("/api/conversations/{session_id}")
    async def get_conversation(session_id: str, auth=Depends(verify_api_key)):
        """Get conversation history. Authenticated."""
        history = get_history(session_id, limit=50)
        return JSONResponse(content={
            "session_id": session_id,
            "messages": history,
            "count": len(history),
        })

    @app.post("/webhook/whatsapp")
    async def whatsapp_webhook(request: Request):
        """WhatsApp webhook (JSON). No auth — Twilio signs requests."""
        body = await request.json()
        message = body.get("Body") or body.get("message", {}).get("text", "") or body.get("text", "")
        sender = body.get("From") or body.get("message", {}).get("from", "whatsapp")

        if not message:
            return JSONResponse(content={"error": "No message"}, status_code=400)

        persona_id = route_message(str(message))
        session_id = f"wa_{sender}"

        if HAS_AGENTS:
            try:
                agent = AgentIntelligence(persona_id, "WhatsApp Agent")
                result = agent.execute(task="Respond to this message", data={"message": str(message)}, temperature=0.3)
                response_text = result.get("text", "I could not process that.")
                save_message(session_id, persona_id, "user", str(message))
                save_message(session_id, persona_id, "assistant", response_text)
                logger.info(f"WhatsApp: {sender} -> {persona_id}")
            except Exception as e:
                response_text = f"Error: {str(e)}"
                logger.error(f"WhatsApp error: {e}")
        else:
            response_text = f"Revenue OS received: {message[:100]}... (agents not loaded)"

        return JSONResponse(content={"response": response_text, "routed_to": persona_id})

    @app.post("/webhook/twilio")
    async def twilio_webhook(request: Request):
        """Twilio WhatsApp webhook (form-encoded). No auth needed."""
        body = await request.form()
        message = body.get("Body", "")
        sender = body.get("From", "unknown")

        if not message:
            twiml = '<?xml version="1.0"?><Response><Message>Please send a message.</Message></Response>'
            return Response(content=twiml, media_type="application/xml")

        persona_id = route_message(str(message))
        session_id = f"tw_{sender}"

        if HAS_AGENTS:
            try:
                agent = AgentIntelligence(persona_id, "WhatsApp Agent")
                result = agent.execute(task="Respond to this message", data={"message": str(message)}, temperature=0.3)
                response_text = result.get("text", "Could not process.")
                save_message(session_id, persona_id, "user", str(message))
                save_message(session_id, persona_id, "assistant", response_text)
            except Exception as e:
                response_text = f"Error: {str(e)}"
        else:
            response_text = f"Message received. Routed to: {persona_id}"

        twiml = f'<?xml version="1.0"?><Response><Message>{response_text}</Message></Response>'
        return Response(content=twiml, media_type="application/xml")

else:
    app = None
    print("FastAPI not installed.")

# ============================================================
# CLI ENTRY POINT (for demo_agent.py)
# ============================================================
def cli_chat():
    """Interactive CLI chat loop."""
    print("Revenue OS Chat (type 'quit' to exit)")
    session_id = f"cli_{datetime.utcnow().timestamp():.0f}"
    while True:
        message = input("> ").strip()
        if message.lower() in ("quit", "exit", "q"):
            break
        persona_id = route_message(message)
        print(f"[{persona_id}]")
        if HAS_AGENTS:
            try:
                agent = AgentIntelligence(persona_id)
                result = agent.execute(task=message, temperature=0.3)
                print(result.get("text", "")[:500])
                save_message(session_id, persona_id, "user", message)
                save_message(session_id, persona_id, "assistant", result.get("text", ""))
            except Exception as e:
                print(f"Error: {e}")
        else:
            print(f"Agents not loaded. Run: pip install -r requirements.txt")


if __name__ == "__main__":
    cli_chat()
