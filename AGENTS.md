# Wiki schema and conventions

This repo is a personal knowledge base built by an LLM agent, following the "LLM wiki" pattern: `raw/` holds immutable sources, `wiki/` holds the markdown knowledge base you (the agent) write and maintain, and this file is the schema. A Python tool, `wikillm`, mirrors `wiki/*.md` into a Neo4j Aura graph so structure (links, tags, orphans, hubs) can be queried directly instead of eyeballed.

## Layout

```
raw/                 immutable source documents — never edit these
  assets/            downloaded images referenced by raw sources
wiki/
  index.md           catalog of every page, grouped by type — update on every ingest
  log.md             append-only activity log
  entities/          people, organizations, places, things
  concepts/          ideas, definitions, recurring themes
  sources/           one page per ingested source (summary + takeaways)
wikillm/             the Python CLI/library — you shouldn't need to edit this often
```

## Page format

Every page under `wiki/` (except `index.md` and `log.md`) has YAML frontmatter:

```yaml
---
title: Ada Lovelace
type: entity          # entity | concept | source | topic | page
tags: [mathematician, computing-history]
aliases: [Countess of Lovelace]
sources: [sources/note-g.md]   # pages this one derives from
created: 2026-07-16
updated: 2026-07-16
---
```

Cross-reference other pages with `[[Page Title]]` (matches by title, filename, or alias — case-insensitive). Body content is freeform markdown; use the template headings `wikillm new` generates as a starting point, not a strict schema.

## Workflows

**Ingest a source**
1. Read the new file in `raw/`.
2. Discuss key takeaways with the user.
3. `wikillm new source "<title>"` to create the source page; fill in the summary and takeaways.
4. Update or create entity/concept pages touched by this source (`wikillm new entity ...` / `wikillm new concept ...` as needed), linking back to the source with `[[...]]` and listing it under `sources:` in frontmatter.
5. Update `wiki/index.md` with any new/changed pages.
6. `wikillm log "ingest | <source title>"`.
7. `wikillm sync` to push the updated graph to Neo4j.

**Answer a query**
1. Read `wiki/index.md` first; use `wikillm search "<query>"` for full-text hits across the graph if the index isn't enough.
2. Read the relevant pages, synthesize an answer with citations to page paths.
3. If the answer is worth keeping (a comparison, an analysis, a new connection), file it back as a new wiki page rather than letting it live only in chat — then log and sync.

**Lint**
Run `wikillm lint` periodically. It reports orphan pages (no inbound/outbound links), duplicate titles, and top hub pages via the Neo4j graph. Use it to decide what needs new cross-references or its own page. Then `wikillm log "lint | <summary>"`.

## wikillm CLI

```
wikillm init                        scaffold raw/ and wiki/ (idempotent)
wikillm new <type> "<title>"        create a page from template
wikillm sync                        push wiki/*.md into Neo4j Aura (full resync, prunes deleted pages)
wikillm search "<query>"            full-text search over the graph
wikillm lint                        orphans, duplicate titles, hub report
wikillm log "<kind> | <title>"      append a timestamped log.md entry
wikillm stats                       node/relationship counts, orphan count
```

Requires `.env` (copy from `.env.example`) with Neo4j Aura credentials. Run `wikillm sync` after any batch of page edits — the graph is a derived view of the markdown, not a separate source of truth.
