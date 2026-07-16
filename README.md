# wiki-llm

A personal knowledge base maintained by an LLM agent: markdown pages in `wiki/` are the source of truth. See [AGENTS.md](AGENTS.md) for the schema and conventions the agent follows.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
wikillm init
```

## Usage

```bash
wikillm new entity "Ada Lovelace" --tags mathematician computing-history
wikillm search "computing history"
wikillm lint                          # orphans, duplicate titles, unresolved links, hubs
wikillm log "ingest | Note G"
wikillm stats
```

## How it fits together

- **raw/** — immutable source documents. Never edited by the agent.
- **wiki/** — markdown pages (`entities/`, `concepts/`, `sources/`, plus `index.md` and `log.md`). This is what you read and what the agent writes.
- **wikillm/** — the Python package: parses frontmatter + `[[wikilinks]]` and builds an in-memory link graph from `wiki/*.md` on every command. `lint` uses it to find orphans, hub pages, and unresolved links; `search` does a simple scored full-text lookup over titles, tags, and body text; `stats` reports page/link counts. Nothing is persisted outside the markdown files — the graph is recomputed each run.

Point your LLM agent (Claude Code, etc.) at this repo with `AGENTS.md` as its schema, and it does the reading, summarizing, and cross-referencing — this tooling just keeps the bookkeeping (index, log, link integrity) honest.

At larger scale, if `wikillm search`'s naive term matching stops being good enough, consider swapping in a proper local search engine like [qmd](https://github.com/tobi/qmd) (hybrid BM25/vector search over markdown, with a CLI and MCP server) rather than reintroducing external infrastructure.
