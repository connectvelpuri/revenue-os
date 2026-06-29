# DealForge

> **147 AI agents. 70 world-class experts. One CLI.**
> Forge smarter deals. Close faster.

---

## The Pain

**Sales teams use 8+ disconnected tools.** Gong records calls but can't prospect. Outreach sequences emails but can't analyze buyer psychology. Salesforce qualifies deals but can't run negotiation strategy. Every tool solves ONE piece. Nothing connects them. You pay $1,600+/month for fragmentation.

**Your best reps have 15+ years of instincts.** MEDDPICC. Challenger. SPIN. Gap Selling. Cialdini. Frameworks they've mastered over decades. When they leave, that knowledge walks out the door. New reps take 12+ months to ramp. You lose millions.

**Deals die silently.** Stalled at legal because nobody prepped procurement defense. Champions go unsupported. Competitive threats go unnoticed until the loss review. By then, it's too late.

---

## What DealForge Does

DealForge embeds **70 world-class sales experts** into one CLI. It covers the full revenue lifecycle:

```
PROSPECT --> QUALIFY --> NEGOTIATE --> CLOSE --> COACH
```

Each step is handled by specialized AI agents. Each agent is trained on 10 top experts in that domain. All in one command.

---

## How It Works

```
                         YOU
                          |
                    ------v------
                    |  Ask your  |
                    |  question  |
                    ------+------
                          |
              ------------+-----------
              |   Intent Detector    |
              |  (deal? negotiate?   |
              |   pipeline? buyer?)  |
              ------------+-----------
                          |
              ------------+-----------
              |  5 Clarifying        |
              |  Questions           |
              |  (consultant-style)  |
              ------------+-----------
                          |
         ----------------+----------------
         v               v                v
  +-----------+   +-----------+   +-----------+
  |  MEDDPICC |   |   Buyer   |   |  Master   |
  | Qualifier |   | Psychology|   | Negotiator|
  | 10 experts|   | 10 experts|   | 10 experts|
  +-----------+   +-----------+   +-----------+
         |               |                |
         +---------------+----------------+
                          |
              ------------+-----------
              |  McKinsey-Level      |
              |  Analysis Report     |
              |  + 5 Follow-up Qs    |
              ------------------------
```

**No server. No database. No cloud. Just Python.**

---

## 7 Expert Personas (70 Total Experts)

| Agent | What It Does | The 10 Experts Behind It |
|-------|-------------|--------------------------|
| **MEDDPICC Qualifier** | Scores deals, finds gaps, validates champions | Dunkel, Gong Labs, Rackham, Dixon, McMahon, Antonio, Whyte, Weisberg, Sandler, Blount |
| **Master Negotiator** | Procurement defense, BATNA, concessions | Voss, Fisher, Ury, Cohen, Camp, Karrass, Cialdini, Kupfer, Shell, Malhotra |
| **Buyer Behavior** | Stakeholder analysis, influence, objections | Cialdini, Kahneman, Ariely, Carnegie, Munger, Greene, Thaler, Ogilvy, Godin, Robbins |
| **Value Architect** | ROI/TCO, business cases, board presentations | Porter, Christensen, Moore, Sinek, Thiel, Ferriss, Rose, Tracy, Balfour, Peters |
| **Elite Prospector** | Lead gen, outreach, pipeline building | Ross, Konrath, Barrows, Bertuzzi, Efti, Tyler, Schultz, Coggins, Iannarino, Cardone |
| **Revenue Conductor** | Pipeline strategy, forecasting, ops | Jobs, Welch, Grove, Drucker, Bezos, Sandberg, Nadella, Powell, Buffett, Dalio |
| **Sales Call Coach** | Call analysis, coaching, objection practice | Gong Labs, McMahon, Chorus.ai, Weinberg, Priemer, Dixon, Orlob, Blount, Ziglar, Barrows |

---

## Quick Start (30 seconds)

```bash
git clone https://github.com/connectvelpuri/revenue-os.git
cd revenue-os
pip install -r requirements.txt
python cli.py --logo
```

### Interactive Mode

```bash
python cli.py
```

Type naturally:
- `qualify this $500K deal`
- `negotiate with procurement`
- `analyze buyer psychology for the CIO`
- `/help` for commands
- `/quit` to exit

### Single Query

```bash
python cli.py "qualify this $500K enterprise deal" --api-key your-key
```

### Multi-Agent Deep Dive (Best Feature)

Asks 5 clarifying questions, then runs 3-4 agents in parallel:

```bash
python cli.py "I need to win a $2M deal against Oracle" --api-key your-key
```

---

## Example: Multi-Agent Deep Dive

```
$ python cli.py --api-key sk-or-...

> I need to win a $2M enterprise deal

? Deal value and stage?  $2M, stuck at legal review
? Decision-makers?  CIO + Procurement Director
? Competitors?  Oracle
? Buyer's biggest concern?  Implementation risk
? Who is your champion?  VP of Engineering

Analyzing with 3 agents...

PERSPECTIVE 1: MEDDPICC QUALIFIER
Score: 32/40 - Gap: Economic buyer not engaged
Action: Schedule CIO briefing this week

PERSPECTIVE 2: BUYER PSYCHOLOGY
Procurement is risk-averse. Champion lacks budget authority.
Action: Equip VP Eng with TCO comparison.

PERSPECTIVE 3: MASTER NEGOTIATOR
Oracle will compete on price. Your advantage: implementation speed.
Action: Build switching cost narrative.

Follow-up questions:
1. Deep dive on Oracle's weaknesses
2. Procurement negotiation scenario
3. Stakeholder influence map for CIO
```

---

## Bring Your Own AI

```bash
export OPENROUTER_API_KEY=***
python cli.py --api-key $OPENROUTER_API_KEY
```

Free models: openrouter/free, nvidia/nemotron-3-ultra-550b-a55b:free, meta-llama/llama-3.3-70b-instruct:free

---

## Who Benefits

| Role | How |
|------|-----|
| **VP Sales / CRO** | Pipeline health, deal inspection, forecasts - in seconds |
| **Enterprise AE** | MEDDPICC scoring, negotiation strategy - like having 10 experts per call |
| **SDR / BDR** | Prospect research, outreach scripts, objection handling |
| **Solutions Architect** | ROI/TCO models, business cases, competitive diffs |
| **Sales Enablement** | Call coaching, training, ramp acceleration |
| **Revenue Operations** | Pipeline analytics, process optimization |
| **Founder / CEO** | Full deal visibility, McKinsey-level analysis, $0 cost |

---

## The Value Equation

```
Value = (Deal Velocity x Win Rate x Deal Size) - (Tool Sprawl x Ramp Time)
       ---------------------------------------------------------------
                                    $0
```

**Without:** 8 tools x $200/mo = $1,600/mo + 12-month ramp + 60% win rate
**With DealForge:** $0 + embedded expertise + multi-agent analysis

---

## License

MIT - free to use, modify, sell, deploy.
