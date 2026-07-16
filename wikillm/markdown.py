from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml

from .config import PAGE_TYPES, WIKI_DIR

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]+)?\]\]")

TEMPLATES = {
    "entity": "## Overview\n\n## Key facts\n\n## Related\n",
    "concept": "## Definition\n\n## Discussion\n\n## Related\n",
    "source": "## Summary\n\n## Key takeaways\n\n## Cited by\n",
    "topic": "## Overview\n\n## Subtopics\n\n## Related\n",
    "page": "",
}


@dataclass
class Page:
    path: Path
    title: str
    type: str = "page"
    tags: list[str] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    created: str | None = None
    updated: str | None = None
    body: str = ""
    extra: dict = field(default_factory=dict)

    @property
    def id(self) -> str:
        try:
            return self.path.relative_to(WIKI_DIR).as_posix()
        except ValueError:
            return self.path.name

    @property
    def links(self) -> list[str]:
        return [m.strip() for m in WIKILINK_RE.findall(self.body)]


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "untitled"


def parse_page(path: Path) -> Page:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return Page(path=path, title=path.stem, body=text)

    raw_meta, body = match.groups()
    meta = yaml.safe_load(raw_meta) or {}

    known = {"title", "type", "tags", "aliases", "sources", "created", "updated"}
    extra = {k: v for k, v in meta.items() if k not in known}

    return Page(
        path=path,
        title=meta.get("title", path.stem),
        type=meta.get("type", "page") if meta.get("type") in PAGE_TYPES else "page",
        tags=list(meta.get("tags") or []),
        aliases=list(meta.get("aliases") or []),
        sources=list(meta.get("sources") or []),
        created=meta.get("created"),
        updated=meta.get("updated"),
        body=body.lstrip("\n"),
        extra=extra,
    )


def render_page(page: Page) -> str:
    meta = {
        "title": page.title,
        "type": page.type,
        "tags": page.tags,
        "aliases": page.aliases,
        "sources": page.sources,
        "created": page.created,
        "updated": page.updated,
    }
    meta.update(page.extra)
    frontmatter = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True).strip()
    return f"---\n{frontmatter}\n---\n\n{page.body.strip()}\n"


def iter_pages(wiki_dir: Path = WIKI_DIR):
    for path in sorted(wiki_dir.rglob("*.md")):
        if path.name in ("index.md", "log.md"):
            continue
        yield parse_page(path)


def build_resolver(pages: list[Page]) -> dict[str, str]:
    resolver: dict[str, str] = {}
    for page in pages:
        keys = {page.title, page.path.stem, *page.aliases}
        for key in keys:
            resolver[key.strip().lower()] = page.id
    return resolver


@dataclass
class LinkGraph:
    resolved: dict[str, list[str]]
    unresolved: dict[str, list[str]]

    def out_degree(self, page_id: str) -> int:
        return len(self.resolved.get(page_id, []))

    def in_degree(self, page_id: str) -> int:
        return sum(1 for targets in self.resolved.values() if page_id in targets)

    def degree(self, page_id: str) -> int:
        return self.out_degree(page_id) + self.in_degree(page_id)


def build_link_graph(pages: list[Page]) -> LinkGraph:
    resolver = build_resolver(pages)
    resolved: dict[str, list[str]] = {}
    unresolved: dict[str, list[str]] = {}
    for page in pages:
        targets = []
        misses = []
        for raw in WIKILINK_RE.findall(page.body):
            key = raw.strip().lower()
            target_id = resolver.get(key)
            if target_id and target_id != page.id:
                targets.append(target_id)
            elif not target_id:
                misses.append(raw.strip())
        resolved[page.id] = targets
        if misses:
            unresolved[page.id] = misses
    return LinkGraph(resolved=resolved, unresolved=unresolved)


PAGE_TYPE_DIRS = {
    "entity": "entities",
    "concept": "concepts",
    "source": "sources",
    "topic": "topics",
    "page": "",
}


def new_page(page_type: str, title: str, tags: list[str] | None = None) -> Path:
    if page_type not in PAGE_TYPES:
        raise ValueError(f"Unknown page type '{page_type}'. Choose from {PAGE_TYPES}")

    subdir = WIKI_DIR / PAGE_TYPE_DIRS[page_type]
    subdir.mkdir(parents=True, exist_ok=True)
    dest = subdir / f"{slugify(title)}.md"
    if dest.exists():
        raise FileExistsError(f"{dest} already exists")

    today = date.today().isoformat()
    page = Page(
        path=dest,
        title=title,
        type=page_type,
        tags=tags or [],
        created=today,
        updated=today,
        body=TEMPLATES.get(page_type, ""),
    )
    dest.write_text(render_page(page), encoding="utf-8")
    return dest
