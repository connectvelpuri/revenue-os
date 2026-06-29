# Revenue OS — AI-Powered Multi-Agent Revenue Operating System

![GitHub](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen)

> **147 AI agents across 27 divisions, each combining 10 world-class expert personas.  
> Think: MEDDPICC + SPIN + Challenger + Gap Selling, orchestrated by AI agents that think like Steve Jobs, Warren Buffett, Chris Voss, and Robert Cialdini — all in one CLI.**

---

## 🚀 One-Command Setup

```bash
# 1. Clone
git clone https://github.com/connectvelpuri/revenue-os.git
cd revenue-os

# 2. Install
pip install -r requirements.txt

# 3. Run — no API key needed for demo
python cli.py --logo
```

---

## 🎯 What Makes This Different

| Traditional Sales Tools | Revenue OS |
|------------------------|------------|
| One function (e.g., Gong = call analysis only) | **Full revenue lifecycle**: prospecting → qualification → negotiation → coaching |
| Generic AI prompts | **70 world-class experts** embedded as personas (Voss, Cialdini, Jobs, Buffett...) |
| Single-agent responses | **Multi-agent orchestration**: 3-4 agents analyze in parallel → combined report |
| Static playbooks | **Auto-improving**: learning loop tracks outcomes → optimizes prompts |
| Monthly SaaS fees | **Free + open source**: bring your own LLM key |

---

## 📋 How It Works

```
You type a question
       │
       ▼
┌──────────────────┐
│  Intent Detector  │  Classifies: deal? negotiate? buyer? pipeline?
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Clarifying       │  Asks 5 McKinsey-style questions
│  Questions        │  (like a consultant would)
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Multi-Agent      │  Routes to 3-4 specialized agents
│  Orchestrator     │  Each with 10 expert personas
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  McKinsey-Level   │  Combined report: Executive Summary
│  Report           │  → Perspectives → Recommendations
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Follow-ups       │  5 suggested next questions
└──────────────────┘
```

---

## 🧠 7 Core Agent Personas (70 Combined Experts)

| Persona | Experts Embedded | When to Use |
|---------|-----------------|-------------|
| **MEDDPICC Qualifier** | Dick Dunkel, Gong Labs, Neil Rackham, Matt Dixon, John McMahon + 5 more | Scoring deals, qualification gaps, champion validation |
| **Master Negotiator** | Chris Voss, Roger Fisher, William Ury, Herb Cohen, Jim Camp + 5 more | Contract negotiation, procurement defense, pricing |
| **Buyer Behavior** | Robert Cialdini, Daniel Kahneman, Dan Ariely, Dale Carnegie, Tony Robbins + 5 more | Stakeholder analysis, influence strategy, objection handling |
| **Value Architect** | Michael Porter, Clay Christensen, Simon Sinek, Peter Thiel, Brian Tracy + 5 more | ROI/TCO modeling, business cases, board presentations |
| **Elite Prospector** | Aaron Ross, Jill Konrath, Grant Cardone, John Barrows + 6 more | Lead generation, outreach sequences, pipeline building |
| **Revenue Conductor** | Steve Jobs, Jack Welch, Peter Drucker, Warren Buffett, Ray Dalio + 5 more | Pipeline strategy, forecasting, revenue operations |
| **Sales Call Coach** | Gong Labs, Zig Ziglar, Jeb Blount, Chris Orlob + 6 more | Call analysis, coaching, objection handling practice |

---

## 📖 Books Injected into Agent Prompts

The system doesn't just "know about" these books — their *frameworks* are embedded as executable reasoning patterns:

| Category | Books |
|----------|-------|
| **Sales Methodologies** | MEDDPICC, SPIN Selling, Challenger Sale, Gap Selling, Sandler Selling |
| **Psychology & Influence** | Influence (Cialdini), Thinking Fast and Slow (Kahneman), How to Win Friends (Carnegie), Unlimited Power (Robbins), Predictably Irrational (Ariely) |
| **Negotiation** | Never Split the Difference (Voss), Getting to Yes (Fisher), Bargaining for Advantage (Shell) |
| **Prospecting** | Predictable Revenue (Ross), Fanatical Prospecting (Blount), Sell or Be Sold (Cardone) |
| **Leadership & Strategy** | Think and Grow Rich (Hill), Good to Great (Collins), 7 Habits (Covey) |
| **Sales Management** | Sales EQ (Blount), Cracking the Sales Management Code (Jordan), The Qualified Sales Leader (McMahon) |

---

## 🖥️ CLI Commands

### Quick Start

```bash
# Show logo
python cli.py --logo

# Interactive mode (chat-like)
python cli.py

# With your own API key
python cli.py --api-key sk-or-...your-key
```

### Single Queries

```bash
# Route to correct agent automatically
python cli.py "qualify this $500K enterprise deal" --api-key your-key

# Force a specific persona
python cli.py --persona negotiation "negotiate with procurement"

# Multi-agent deep analysis (asks clarifying questions first)
python cli.py "I need to win a $2M deal against Oracle" --api-key your-key
```

### Interactive Mode Commands

Once in the CLI (`python cli.py`), type:

| Command | Description |
|---------|-------------|
| `qualify this deal` | Routes to MEDDPICC Qualifier with 10 experts |
| `negotiate with procurement` | Routes to Master Negotiator |
| `analyze buyer psychology` | Routes to Buyer Behavior Expert |
| `build an ROI case` | Routes to Value Architect |
| `/help` | Show all commands |
| `/personas` | List all agent personas |
| `/clear` | Clear screen |
| `/quit` | Exit |

### Example: Multi-Agent Deep Dive

```
> I need to win a $2M deal

? What is the deal value and current stage?  $2M, in legal review
? Who are the decision-makers?  CIO and Procurement Director  
? Which competitors are involved?  Oracle and IBM
? What is the prospect's biggest concern?  Implementation risk
? What evidence do you have that your champion is real?  They shared internal deck

Running multi-agent analysis...
  Consulting MEDDPICC Qualifier... done
  Consulting Buyer Psychology... done
  Consulting Negotiation... done

===== McKINSEY-LEVEL ANALYSIS REPORT =====

PERSPECTIVE 1: MEDDPICC Deal Qualification
[Analysis from 10 deal qualification experts...]

PERSPECTIVE 2: Buyer Psychology  
[Stakeholder influence mapping...]

PERSPECTIVE 3: Negotiation
[Procurement defense strategy...]

Follow-up questions:
1. Deep dive on Oracle competitive positioning
2. Negotiation scenario planning
3. Stakeholder influence map for CIO
```

---

## 🌐 API Server (Optional — for WhatsApp or custom integrations)

```bash
# Install server dependencies
pip install fastapi uvicorn python-multipart

# Start
uvicorn api.webhook:app --host 0.0.0.0 --port 8080

# Test
curl http://localhost:8080/health
```

### API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/health` | GET | No | Service health |
| `/api/agent/execute` | POST | X-API-Key | Execute single agent |
| `/api/agent/chat` | POST | X-API-Key | Conversational chat |
| `/webhook/whatsapp` | POST | No | WhatsApp webhook (JSON) |
| `/webhook/twilio` | POST | No | Twilio WhatsApp webhook |

### API Usage

```bash
curl -X POST https://your-server.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{"task":"qualify this $500K deal","persona":"meddpicc_qualifier"}'
```

---

## 🔧 Bring Your Own AI

The system supports multiple LLM providers. Set any of these environment variables:

```bash
# OpenRouter (recommended — free tier available)
export OPENROUTER_API_KEY=sk-or-...your-key

# Anthropic
export ANTHROPIC_API_KEY=sk-ant-...your-key

# NVIDIA NIM
export NVIDIA_NIM_API_KEY=nvapi-...your-key

# Then use the CLI
python cli.py --api-key $OPENROUTER_API_KEY
```

Free models are pre-configured:
- `openrouter/free` — auto-routes to best free model
- `nvidia/nemotron-3-ultra-550b-a55b:free` — 550B parameter reasoning
- `meta-llama/llama-3.3-70b-instruct:free` — 70B general purpose

---

## 📊 Learning Loop (Auto-Improvement)

The system includes a learning loop that tracks outcomes and optimizes agent prompts:

```python
from agents.learning_loop import LearningLoop

loop = LearningLoop()
loop.run_cycle(agent_id="meddpicc_qualifier", 
               task="Qualified a deal",
               score=4,
               feedback="Strong MEDDPICC analysis but missed champion validation")
```

---

## 📁 Project Structure

```
revenue-os/
├── cli.py                    # Main CLI (this is all you need)
├── agents/
│   ├── agent_base/
│   │   ├── llm_client.py     # LLM provider routing
│   │   ├── personas/         # 7 expert persona definitions
│   │   └── agent_wrapper.py  # Persona + training injection
│   ├── specialists/           # 36 specialist agent files
│   └── learning_loop.py      # Outcome-based improvement
├── api/
│   └── webhook.py            # FastAPI server + WhatsApp
├── docs/                     # Documentation
├── LICENSE
├── requirements.txt
└── README.md
```

---

## 📜 License

MIT — free to use, modify, and distribute. No strings attached.

---

## 🤝 Contributing

PRs welcome! Ideas for new personas, better prompts, additional book injections, or improved agent orchestration.

---

## ⚡ Quick Start (30 seconds)

```bash
git clone https://github.com/connectvelpuri/revenue-os.git
cd revenue-os
pip install -r requirements.txt
python cli.py
```

Type: `qualify this $500K deal` and see what happens.
