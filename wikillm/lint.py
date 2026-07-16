from __future__ import annotations

from dataclasses import dataclass, field

from .markdown import Page, build_link_graph


@dataclass
class LintReport:
    orphans: list[Page] = field(default_factory=list)
    hubs: list[tuple[Page, int]] = field(default_factory=list)
    unresolved_links: dict[str, list[str]] = field(default_factory=dict)
    duplicate_titles: dict[str, list[str]] = field(default_factory=dict)


def check_pages(pages: list[Page]) -> LintReport:
    by_id = {p.id: p for p in pages}
    graph = build_link_graph(pages)

    seen: dict[str, list[str]] = {}
    for page in pages:
        seen.setdefault(page.title.strip().lower(), []).append(page.id)
    duplicate_titles = {title: ids for title, ids in seen.items() if len(ids) > 1}

    orphans = [p for p in pages if graph.degree(p.id) == 0]

    hubs = sorted(
        ((p, graph.degree(p.id)) for p in pages),
        key=lambda pair: pair[1],
        reverse=True,
    )
    hubs = [(p, d) for p, d in hubs if d > 0][:5]

    return LintReport(
        orphans=orphans,
        hubs=hubs,
        unresolved_links=graph.unresolved,
        duplicate_titles=duplicate_titles,
    )
