from wikillm.lint import check_pages
from wikillm.markdown import parse_page
from wikillm.search import search


def _write(tmp_path, name, content):
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return parse_page(path)


def test_orphans_and_hubs(tmp_path):
    a = _write(tmp_path, "a.md", "---\ntitle: A\ntype: entity\n---\n\nLinks to [[C]].\n")
    b = _write(tmp_path, "b.md", "---\ntitle: B\ntype: entity\n---\n\nLinks to [[C]].\n")
    e = _write(tmp_path, "e.md", "---\ntitle: E\ntype: entity\n---\n\nLinks to [[C]].\n")
    c = _write(tmp_path, "c.md", "---\ntitle: C\ntype: entity\n---\n\nNo links out.\n")
    orphan = _write(tmp_path, "d.md", "---\ntitle: D\ntype: entity\n---\n\nMentions nothing.\n")

    report = check_pages([a, b, e, c, orphan])

    assert [p.id for p in report.orphans] == ["d.md"]
    assert report.hubs[0] == (c, 3)
    assert report.unresolved_links == {}


def test_unresolved_link(tmp_path):
    a = _write(tmp_path, "a.md", "---\ntitle: A\ntype: entity\n---\n\nSee [[Nonexistent Page]].\n")
    report = check_pages([a])
    assert report.unresolved_links == {"a.md": ["Nonexistent Page"]}


def test_duplicate_titles(tmp_path):
    a = _write(tmp_path, "a.md", "---\ntitle: Same\ntype: entity\n---\n\nbody\n")
    b = _write(tmp_path, "b.md", "---\ntitle: Same\ntype: concept\n---\n\nbody\n")
    report = check_pages([a, b])
    assert report.duplicate_titles == {"same": ["a.md", "b.md"]}


def test_search_ranks_title_over_body(tmp_path):
    a = _write(tmp_path, "a.md", "---\ntitle: Computing History\ntype: concept\n---\n\nSomething else.\n")
    b = _write(tmp_path, "b.md", "---\ntitle: Unrelated\ntype: concept\n---\n\nA note on computing history.\n")

    hits = search([a, b], "computing history")

    assert [h.page.id for h in hits] == ["a.md", "b.md"]
    assert hits[0].score > hits[1].score


def test_search_no_match_returns_empty(tmp_path):
    a = _write(tmp_path, "a.md", "---\ntitle: A\ntype: entity\n---\n\nbody\n")
    assert search([a], "nothing matches this") == []
