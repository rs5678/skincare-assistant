# Skinsight

An AI-powered skincare assistant that reasons over a user's logged skin history and a retrieval-augmented knowledge base of ingredient science to generate grounded, personalized recommendations. This is built from scratch using the Claude API's tool-use capabilities, with no agent framework in between.

## What it does

A user logs their skin conditions over time (symptoms, severity, products used, notes). Skinsight can then answer questions like *"why has my skin been getting worse this month?"* by:

1. Retrieving the user's recent skin log history
2. Semantically searching a knowledge base of skincare ingredient facts (effects, warnings, interactions)
3. Reasoning over both to explain likely correlations (e.g., connecting a newly introduced retinol to a spike in reported dryness) and offering grounded recommendations

## Architecture

```
User question
     │
     ▼
Agent loop (Claude + tool use)
     │
     ├──► get_user_history ──► Postgres (skin log entries)
     │
     └──► search_ingredients ──► pgvector semantic search ──► Voyage embeddings
     │                                    │
     │                          Postgres (ingredient facts + embeddings)
     ▼
Grounded, personalized response
```

## Tech stack

| Layer | Tool |
|---|---|
| LLM & tool-use orchestration | Claude API (Anthropic), hand-rolled agent loop |
| Retrieval / RAG | pgvector (Postgres extension), Voyage AI embeddings (`voyage-3.5-lite`) |
| Data validation | Pydantic |
| Database | PostgreSQL (containerized via Docker) |
| Evaluation | Custom eval harness — checks tool-call correctness per test case |
| Infrastructure (in progress) | Terraform |

## Why no agent framework?

Frameworks like LangChain abstract away exactly the mechanics I wanted to understand: how a tool-use loop actually works, how tool results get threaded back into a conversation, and how retrieval actually integrates with an LLM's reasoning. Every piece of the agent loop, RAG pipeline, and eval harness here is written directly against the Claude API and psycopg2/pgvector, so the whole system is transparent from top to bottom.

## Project structure

```
models.py       # Pydantic data models (SkinLogEntry, IngredientFact)
fake_data.py    # In-memory fixtures used in early development and testing
tools.py        # Agent-facing tool functions + schemas (get_user_history, search_ingredients)
rag.py          # Embedding generation + pgvector retrieval pipeline
agent.py        # The core agent loop: Claude tool-use orchestration
evals.py        # Automated eval harness — validates tool-calling behavior
```

## Evals

Rather than eyeballing whether the agent "seems to work," `evals.py` runs a set of test cases against the live agent and checks that it calls the expected tools for each class of question — e.g., a question requiring both history and ingredient context should trigger both `get_user_history` and `search_ingredients`.

```
python3 evals.py
```

## Running it locally

**Prerequisites:** Python 3.10+, Docker, an Anthropic API key, a Voyage AI API key.

```bash
# 1. Clone and install dependencies
git clone https://github.com/<your-username>/skinsight.git
cd skinsight
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Set up environment variables
cp .env.example .env
# add your ANTHROPIC_API_KEY and VOYAGE_API_KEY to .env

# 3. Start Postgres with pgvector
docker run --name skinsight-db \
  -e POSTGRES_PASSWORD=devpassword \
  -e POSTGRES_DB=skincare \
  -p 5433:5432 \
  -d pgvector/pgvector:pg16

# 4. Set up the schema (see /schema.sql)
docker exec -it skinsight-db psql -U postgres -d skincare -f /schema.sql

# 5. Embed and load the ingredient knowledge base
python3 rag.py

# 6. Run the agent
python3 agent.py
```

## Current status & what's next

This project is under active development. Currently working end-to-end:

- ✅ Tool-use agent loop (Claude API, no framework)
- ✅ RAG-based ingredient retrieval (pgvector + Voyage embeddings)
- ✅ Automated eval harness

In progress:

- 🚧 Migrating user skin-log history from an in-memory fixture to persistent Postgres storage
- 🚧 Terraform-based deployment (containerized app, managed Postgres, secrets management)

## What I learned building this

- How tool-use agent loops actually work under the hood — message roles, tool_use/tool_result blocks, and multi-turn orchestration
- The mechanics of RAG: embeddings, vector similarity search, and the query/document embedding asymmetry
- Writing evals as a first-class part of an AI system, not an afterthought
- Debugging real infrastructure issues (Docker networking, port conflicts, Postgres role/auth issues) that don't show up in tutorials