from __future__ import annotations

import re
from dataclasses import dataclass

from .markdown import Page

WORD_RE = re.compile(r"\w+")


@dataclass
class SearchHit:
    page: Page
    score: float


def _terms(text: str) -> list[str]:
    return [w.lower() for w in WORD_RE.findall(text)]


def search(pages: list[Page], query: str, limit: int = 10) -> list[SearchHit]:
    query_terms = _terms(query)
    if not query_terms:
        return []

    hits = []
    for page in pages:
        title_terms = _terms(page.title)
        body_terms = _terms(page.body)
        tag_terms = _terms(" ".join(page.tags))

        score = 0.0
        for term in query_terms:
            score += 5.0 * title_terms.count(term)
            score += 2.0 * tag_terms.count(term)
            score += 1.0 * body_terms.count(term)

        if score > 0:
            hits.append(SearchHit(page=page, score=score))

    hits.sort(key=lambda h: h.score, reverse=True)
    return hits[:limit]
