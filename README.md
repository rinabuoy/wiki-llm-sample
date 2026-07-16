# wiki-llm

A personal knowledge base maintained by an LLM agent: markdown pages in `wiki/` as the source of truth, synced into a Neo4j Aura knowledge graph for structural queries (search, orphans, hubs, cross-references). See [AGENTS.md](AGENTS.md) for the schema and conventions the agent follows.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env   # fill in your Neo4j Aura URI/username/password
wikillm init
```

Create a free Neo4j Aura instance at [console.neo4j.io](https://console.neo4j.io) if you don't have one — it gives you a connection URI and one-time password on creation.

## Usage

```bash
wikillm new entity "Ada Lovelace" --tags mathematician computing-history
wikillm sync                          # push wiki/*.md -> Neo4j Aura
wikillm search "computing history"
wikillm lint                          # orphans, duplicate titles, hubs
wikillm log "ingest | Note G"
wikillm stats
```

## How it fits together

- **raw/** — immutable source documents. Never edited by the agent.
- **wiki/** — markdown pages (`entities/`, `concepts/`, `sources/`, plus `index.md` and `log.md`). This is what you read and what the agent writes.
- **wikillm/** — the Python package: parses frontmatter + `[[wikilinks]]`, syncs pages into Neo4j as nodes (`Page` + `Entity`/`Concept`/`Source`/`Topic`) and relationships (`LINKS_TO`, `HAS_TAG`, `DERIVED_FROM`), and exposes full-text search and lint queries over the graph.
- **Neo4j Aura** is a derived view, not a second source of truth — `wikillm sync` is idempotent and safe to re-run; it prunes nodes for pages that were deleted from `wiki/`.

Point your LLM agent (Claude Code, etc.) at this repo with `AGENTS.md` as its schema, and it does the reading, summarizing, and cross-referencing — this tooling just keeps the graph in sync with what it writes.
