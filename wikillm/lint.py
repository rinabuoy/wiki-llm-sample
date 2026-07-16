from __future__ import annotations

from dataclasses import dataclass, field

from .graph import WikiGraph
from .markdown import Page


@dataclass
class LintReport:
    orphans: list[dict] = field(default_factory=list)
    hubs: list[dict] = field(default_factory=list)
    unresolved_links: dict[str, list[str]] = field(default_factory=dict)
    missing_titles: list[str] = field(default_factory=list)
    duplicate_titles: dict[str, list[str]] = field(default_factory=dict)


def check_pages(pages: list[Page]) -> LintReport:
    report = LintReport()

    seen: dict[str, list[str]] = {}
    for page in pages:
        if not page.title or page.title == page.path.stem:
            if not page.title:
                report.missing_titles.append(page.id)
        seen.setdefault(page.title.strip().lower(), []).append(page.id)

    report.duplicate_titles = {
        title: ids for title, ids in seen.items() if len(ids) > 1
    }
    return report


def check_graph(graph: WikiGraph, report: LintReport) -> LintReport:
    stats = graph.stats()
    report.orphans = stats["orphans"]
    report.hubs = [h for h in stats["hubs"] if h["degree"] > 0][:5]
    return report
