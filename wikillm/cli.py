from __future__ import annotations

import argparse
import sys
from collections import Counter
from datetime import date

from rich.console import Console
from rich.table import Table

from .config import INDEX_FILE, LOG_FILE, RAW_DIR, WIKI_DIR
from .lint import check_pages
from .markdown import build_link_graph, iter_pages, new_page
from .search import search as search_pages

console = Console()


def cmd_init(args):
    (RAW_DIR / "assets").mkdir(parents=True, exist_ok=True)
    for sub in ("entities", "concepts", "sources"):
        (WIKI_DIR / sub).mkdir(parents=True, exist_ok=True)

    if not INDEX_FILE.exists():
        INDEX_FILE.write_text("# Index\n\n## Entities\n\n## Concepts\n\n## Sources\n", encoding="utf-8")
    if not LOG_FILE.exists():
        LOG_FILE.write_text("# Log\n\n", encoding="utf-8")

    console.print("[green]Initialized wiki structure.[/green]")


def cmd_new(args):
    path = new_page(args.type, args.title, tags=args.tags or [])
    console.print(f"[green]Created[/green] {path.relative_to(WIKI_DIR.parent)}")


def cmd_search(args):
    pages = list(iter_pages())
    hits = search_pages(pages, args.query, limit=args.limit)
    if not hits:
        console.print("[yellow]No matches.[/yellow]")
        return
    table = Table(show_header=True)
    table.add_column("Score")
    table.add_column("Type")
    table.add_column("Title")
    table.add_column("Path")
    for hit in hits:
        table.add_row(f"{hit.score:.1f}", hit.page.type, hit.page.title, hit.page.id)
    console.print(table)


def cmd_lint(args):
    pages = list(iter_pages())
    report = check_pages(pages)

    if report.duplicate_titles:
        console.print("[red]Duplicate titles:[/red]")
        for title, ids in report.duplicate_titles.items():
            console.print(f"  {title}: {', '.join(ids)}")

    if report.unresolved_links:
        console.print("[yellow]Unresolved links:[/yellow]")
        for page_id, links in report.unresolved_links.items():
            console.print(f"  {page_id}: {', '.join(links)}")

    if report.orphans:
        console.print("[yellow]Orphan pages (no links in or out):[/yellow]")
        for page in report.orphans:
            console.print(f"  {page.title} ({page.id})")

    if report.hubs:
        console.print("[cyan]Top hub pages:[/cyan]")
        for page, degree in report.hubs:
            console.print(f"  {page.title} — {degree} links")

    if not (report.duplicate_titles or report.unresolved_links or report.orphans):
        console.print("[green]No issues found.[/green]")


def cmd_log(args):
    entry = f"## [{date.today().isoformat()}] {args.entry}\n\n"
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(entry)
    console.print(f"[green]Logged:[/green] {entry.strip()}")


def cmd_stats(args):
    pages = list(iter_pages())
    graph = build_link_graph(pages)

    by_type = Counter(p.type for p in pages)
    table = Table(title="Pages by type")
    table.add_column("Type")
    table.add_column("Count")
    for type_name, count in by_type.most_common():
        table.add_row(type_name, str(count))
    console.print(table)

    total_links = sum(len(targets) for targets in graph.resolved.values())
    orphan_count = sum(1 for p in pages if graph.degree(p.id) == 0)
    console.print(f"[cyan]Total pages:[/cyan] {len(pages)}")
    console.print(f"[cyan]Total links:[/cyan] {total_links}")
    console.print(f"[yellow]Orphans:[/yellow] {orphan_count}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wikillm", description="LLM-maintained markdown wiki")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="Scaffold raw/ and wiki/ directories")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("new", help="Create a new wiki page from a template")
    p.add_argument("type", choices=("entity", "concept", "source", "topic", "page"))
    p.add_argument("title")
    p.add_argument("--tags", nargs="*", default=[])
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("search", help="Search wiki pages by title, tags, and body text")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("lint", help="Health-check the wiki: orphans, duplicates, unresolved links, hubs")
    p.set_defaults(func=cmd_lint)

    p = sub.add_parser("log", help="Append a timestamped entry to wiki/log.md")
    p.add_argument("entry")
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("stats", help="Show wiki summary statistics")
    p.set_defaults(func=cmd_stats)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
