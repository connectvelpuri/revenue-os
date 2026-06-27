# Revenue OS — AI-Powered Revenue Operating System

**Event-driven multi-agent platform for enterprise sales.** 147 agents across 27 divisions, each combining 10 world-class expert personas.

## Quick Start

### 1. Test Without API Key

```bash
python demo_agent.py
```

Type any sales query:
- `"qualify this $500K enterprise deal with MEDDPICC"`
- `"negotiate a 3-year contract with procurement"`
- `"analyze buyer psychology for the CIO"`
- `"build an ROI case for cloud migration"`
- `"coach me on my last sales call"`

### 2. Test With Real AI

```bash
set OPENROUTER_API_KEY=***
python demo_agent.py "qualify this deal with MEDDPICC scoring"
```

### 3. Deploy API (WhatsApp-ready)

```bash
# Install deps
pip install fastapi uvicorn python-multipart

# Set your key
set REVENUE_OS_API_KEY=***
set OPENROUTER_API_KEY=***

# Start server
uvicorn api.webhook:app --host 0.0.0.0 --port 8080
```

Then configure Twilio WhatsApp Sandbox → POST to `http://your-url:8080/webhook/twilio`

## Deploy to Railway ($0)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/XYZ?referralCode=revenue-os)

Or manually:

```bash
railway login
railway up
```

## API Reference

All authenticated endpoints require `X-API-Key` header.

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/` | GET | No | Service status |
| `/health` | GET | No | Health check |
| `/api/agent/execute` | POST | Yes | Execute agent with persona |
| `/api/agent/chat` | POST | Yes | Conversational chat with history |
| `/api/agent/conversation/{id}` | GET | Yes | Get conversation history |
| `/webhook/whatsapp` | POST | No* | WhatsApp webhook (JSON) |
| `/webhook/twilio` | POST | No* | WhatsApp webhook (form) |

*WhatsApp webhooks use platform-level signature verification.

### Execute Agent

```json
POST /api/agent/execute
X-API-Key: your-key
{
  "task": "qualify this enterprise deal",
  "persona": "meddpicc_qualifier",
  "context": "Fortune 500, $2M deal, 3 competitors",
  "data": {"deal_size": "2M", "company": "Acme Corp"},
  "training": "MEDDPICC: M=0.25, E=0.15...",
  "conversation_id": "optional-session-id"
}
```

## Personas Available

| Persona | Experts | Use For |
|---------|---------|---------|
| `revenue_orchestrator` | Jobs, Welch, Grove, Drucker, Bezos... | Pipeline strategy, forecasting |
| `buyer_psychology` | Cialdini, Kahneman, Ariely, Carnegie... | Stakeholder analysis, influence |
| `value_engineer` | Porter, Christensen, Moore, Sinek... | ROI, TCO, business cases |
| `negotiation` | Voss, Fisher, Ury, Cohen, Camp... | Contract, pricing, procurement |
| `prospecting_sdr` | Ross, Konrath, Barrows, Bertuzzi... | Lead gen, outreach sequences |
| `meddpicc_qualifier` | Dunkel, Antonio, Gong, Rackham... | Deal scoring, qualification |
| `call_coacher` | Gong Labs, McMahon, Orlob, Barrows... | Call analysis, coaching |

## Architecture

```
WhatsApp/Twilio → API Gateway → Agent Router → Persona Engine → LLM (OpenRouter)
                                              → Training Injection
                                              → Conversation Memory
                                              → Rule-based Fallback
```

## Repository

- **Code:** https://github.com/connectvelpuri/revenue-os
- **Docs:** `docs/` directory in repo
- **License:** AGPL v3
