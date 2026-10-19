# ClaimSaathi 🛡️

**An AI agent that checks, fixes and fights health-insurance claims in India.**

Many health-insurance claims in India are rejected or only partly paid, and most people never appeal. The policy
wording is dense, the rules (moratorium, waiting periods, room-rent capping) are obscure, and writing a proper
appeal is hard. ClaimSaathi reads your documents, works out what you're actually owed, and drafts the letters.

It is an agent, not a chatbot. For each case it:

1. **Plans** the investigation and shows the plan as a live checklist.
2. **Reads** the policy, hospital bill, discharge summary and rejection letter (PDF, photo or text).
3. **Searches** the policy for the exact clauses and **looks up** IRDAI rules.
4. **Calculates** with tools, not guesswork: tenure, waiting periods, moratorium, proportionate deduction.
5. **Assesses every bill line** as payable, partly payable or not payable, with a clause for each.
6. **Builds the document checklist**, marking what's uploaded and what's still needed.
7. **Drafts ready-to-send documents**: a claim cover letter, a grievance letter, an Ombudsman complaint.
8. **Gives a verdict**: the amount it thinks you're owed, key findings, and next steps with deadlines.

You approve everything before it's sent. The agent never sends anything itself.

## Quick start

Needs Python 3.9+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then paste a free API key into .env (see below)
uvicorn app.main:app --reload
```

Open http://localhost:8000, click **Load a sample case**, then **Run the agent**.

### Choosing a free model

ClaimSaathi works with any provider that has an OpenAI-compatible API. Set `LLM_BASE_URL`, `LLM_API_KEY` and
`LLM_MODEL` in `.env`. Ready-made blocks are in `.env.example`.

| Provider | Cost | Notes |
|---|---|---|
| Google Gemini (AI Studio) | Free tier | Default. Good with long PDFs and photos of bills |
| Groq | Free tier | Very fast. Choose a model that supports tool calling |
| OpenRouter | Free models (`:free`) | Many models, rate-limited |
| Ollama | Free, runs locally | Offline. Needs a decent laptop and a tool-calling model |
| Claude / OpenAI | Paid | Most reliable for long multi-step runs |

Free tiers have per-minute limits. One full run makes about 10–20 model calls, and the client retries automatically
when it gets rate-limited.

## The sample case

`samples/` holds a fictional but realistic case. A claim of ₹1,88,300 for gall-bladder surgery was **fully
rejected** because hypertension wasn't disclosed when the policy was bought. The agent should find that:

- the policy has **88 months** of continuous cover, so the **60-month moratorium** (Policy §5.1) bars rejection for
  non-disclosure;
- hypertension has nothing to do with the surgery;
- the gall-bladder waiting period (24 months) was long over;
- some deductions *are* legitimate: the room was above the ₹5,000/day limit (proportionate deduction of ₹40,000, not
  applied to pharmacy, consumables or diagnostics), and ₹7,100 of non-payable items;
- so the insurer should pay about **₹1,41,200**, and the agent drafts the grievance letter and Ombudsman complaint.

## How it works

```
Browser (static/)  ──POST /run──▶  FastAPI (app/main.py)
      ▲                                  │
      │   server-sent events:            ▼
      │   plan, tool calls,        Agent loop (app/agent.py)
      └── results, messages  ◀──   model ⇄ tools, up to MAX_AGENT_STEPS
                                         │
                   ┌─────────────────────┼─────────────────────┐
                   ▼                     ▼                     ▼
          LLM (app/llm.py)      Tools (app/tools.py)   Documents (app/documents.py)
          any OpenAI-compatible  calculators, bill      PDF/text extraction, photo
          provider               assessment, drafts,    transcription, clause
                                 checklist, verdict     chunking, BM25 search
```

- **app/prompts.py**: the agent's instructions and claim-checking playbook.
- **app/regulations.py**: curated IRDAI rules the agent can cite. **Check these against the latest circulars.**
- **app/store.py**: in-memory cases. Restarting the server clears them.

## Tests

```bash
pytest
```

The tests cover the tools, document classification and search, the agent loop (with a scripted fake model) and
the API end to end. None of them needs an API key.

## Limitations

- Guidance, not legal advice. IRDAI rules change, so check `app/regulations.py` before relying on it.
- Cases live in memory only.
- Scanned PDFs without a text layer need to be uploaded as photos.
# zeero

> **Created on:** 19 October 2026 (IST)
