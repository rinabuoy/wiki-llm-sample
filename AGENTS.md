# Wiki schema and conventions

This repo is a personal knowledge base built by an LLM agent, following the "LLM wiki" pattern: `raw/` holds immutable sources, `wiki/` holds the markdown knowledge base you (the agent) write and maintain, and this file is the schema. A Python tool, `wikillm`, reads `wiki/*.md` and builds an in-memory link graph on demand, so structure (links, tags, orphans, hubs) can be queried directly instead of eyeballed. Everything lives in the markdown files — there is no external database.

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
4. For each entity/concept touched by this source, run `wikillm search "<name>"` first to check whether it already has a page (under this or a different wording) before creating a new one — this is what prevents duplicate/orphan pages as the wiki grows. Update the existing page if found, otherwise `wikillm new entity ...` / `wikillm new concept ...`. Either way, link back to the source with `[[...]]` and list it under `sources:` in frontmatter.
5. Update `wiki/index.md` with any new/changed pages.
6. `wikillm log "ingest | <source title>"`.

**Answer a query**
1. Read `wiki/index.md` first; use `wikillm search "<query>"` for keyword hits across titles, tags, and body text if the index isn't enough.
2. Read the relevant pages, synthesize an answer with citations to page paths.
3. If the answer is worth keeping (a comparison, an analysis, a new connection), file it back as a new wiki page rather than letting it live only in chat — then log it.

**Lint**
Run `wikillm lint` periodically. It reports orphan pages (no inbound/outbound links), duplicate titles, unresolved `[[wikilinks]]`, and top hub pages. Use it to decide what needs new cross-references or its own page. Then `wikillm log "lint | <summary>"`.

## wikillm CLI

```
wikillm init                        scaffold raw/ and wiki/ (idempotent)
wikillm new <type> "<title>"        create a page from template
wikillm search "<query>"            keyword search over titles, tags, and body text
wikillm lint                        orphans, duplicate titles, unresolved links, hub report
wikillm log "<kind> | <title>"      append a timestamped log.md entry
wikillm stats                       page/link counts, orphan count
```

No external services or credentials required — every command reads `wiki/*.md` directly.
