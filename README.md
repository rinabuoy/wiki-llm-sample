# wiki-llm

A personal knowledge base maintained by an LLM agent: markdown pages in `wiki/` are the source of truth. See [AGENTS.md](AGENTS.md) for the schema and conventions the agent follows.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
wikillm init
```

Everything above works with zero external services. Two optional extras add capability:

```bash
pip install -e ".[vector]"   # local sentence embeddings for semantic search (fastembed, on-device)
pip install -e ".[graph]"    # Neo4j Aura sync (neo4j driver + python-dotenv)
```

For `.[graph]`, also `cp .env.example .env` and fill in your Neo4j Aura URI/username/password (create a free instance at [console.neo4j.io](https://console.neo4j.io) if you don't have one).

## Usage

```bash
wikillm new entity "Ada Lovelace" --tags mathematician computing-history
wikillm search "computing history"    # hybrid keyword + semantic search
wikillm lint                          # orphans, duplicate titles, unresolved links, hubs
wikillm log "ingest | Note G"
wikillm stats
wikillm sync                          # push wiki/*.md into Neo4j Aura (requires .[graph])
```

## How it fits together

- **raw/** — immutable source documents. Never edited by the agent.
- **wiki/** — markdown pages (`entities/`, `concepts/`, `sources/`, plus `index.md` and `log.md`). This is what you read and what the agent writes. Always the source of truth.
- **wikillm/** — the Python package:
  - `markdown.py` parses frontmatter + `[[wikilinks]]` and builds an in-memory link graph from `wiki/*.md` on every command.
  - `lint.py` uses that graph to find orphans, hub pages, duplicate titles, and unresolved links.
  - `embeddings.py` computes sentence embeddings for pages (local model via `fastembed`, no API calls), cached in `.wikillm_cache/` keyed by content hash so only changed pages get re-embedded.
  - `search.py` blends keyword scoring with cosine similarity over those embeddings for hybrid search; falls back to keyword-only if `fastembed` isn't installed.
  - `graph.py` (`wikillm sync`) pushes the current markdown state into Neo4j Aura: nodes (`Page` + `Entity`/`Concept`/`Source`/`Topic`), relationships (`LINKS_TO`, `HAS_TAG`, `DERIVED_FROM`), a full-text index, and a native vector index over the same embeddings.

**Neo4j Aura is a separate, rebuildable production copy** — not a second source of truth. You never hand-edit it; `wikillm sync` regenerates it entirely from the markdown each run (upserts current pages, deletes stale ones, rebuilds relationships and the vector index). The point is that a production app can query Aura directly over Bolt/Cypher — for graph traversal, full-text, or vector search — without depending on this Python tool, the local embedding cache, or the markdown files at all. Everything else (`init`/`new`/`search`/`lint`/`log`/`stats`) only ever touches `wiki/*.md` and needs no credentials.

Point your LLM agent (Claude Code, etc.) at this repo with `AGENTS.md` as its schema, and it does the reading, summarizing, and cross-referencing — this tooling just keeps the bookkeeping (index, log, link integrity, and optionally the Aura mirror) honest.
