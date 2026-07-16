from pathlib import Path

from wikillm.markdown import Page, parse_page, render_page, slugify


def test_slugify():
    assert slugify("Ada Lovelace") == "ada-lovelace"
    assert slugify("C++ & Rust!") == "c-rust"


def test_parse_page_roundtrip(tmp_path):
    path = tmp_path / "ada-lovelace.md"
    path.write_text(
        "---\n"
        "title: Ada Lovelace\n"
        "type: entity\n"
        "tags: [mathematician]\n"
        "aliases: [Countess of Lovelace]\n"
        "sources: []\n"
        "created: 2026-07-16\n"
        "updated: 2026-07-16\n"
        "---\n\n"
        "Worked with [[Charles Babbage]] on the [[Analytical Engine]].\n",
        encoding="utf-8",
    )

    page = parse_page(path)
    assert page.title == "Ada Lovelace"
    assert page.type == "entity"
    assert page.tags == ["mathematician"]
    assert page.aliases == ["Countess of Lovelace"]
    assert page.links == ["Charles Babbage", "Analytical Engine"]

    rendered = render_page(page)
    assert "title: Ada Lovelace" in rendered
    assert "[[Charles Babbage]]" in rendered


def test_parse_page_no_frontmatter(tmp_path):
    path = tmp_path / "plain.md"
    path.write_text("Just text, no frontmatter.\n", encoding="utf-8")
    page = parse_page(path)
    assert page.title == "plain"
    assert page.type == "page"
    assert page.links == []


def test_unknown_type_falls_back_to_page(tmp_path):
    path = tmp_path / "weird.md"
    path.write_text("---\ntitle: Weird\ntype: banana\n---\n\nbody\n", encoding="utf-8")
    page = parse_page(path)
    assert page.type == "page"
