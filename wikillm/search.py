from __future__ import annotations

import re
from dataclasses import dataclass

from .embeddings import EmbedFn, EmbeddingsUnavailable, cosine_similarity, embed_query, get_page_embeddings
from .markdown import Page

WORD_RE = re.compile(r"\w+")

SEMANTIC_WEIGHT = 0.5
SEMANTIC_THRESHOLD = 0.45


@dataclass
class SearchHit:
    page: Page
    score: float
    keyword_score: float = 0.0
    semantic_score: float = 0.0


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


def hybrid_search(
    pages: list[Page], query: str, limit: int = 10, embed_fn: EmbedFn | None = None
) -> tuple[list[SearchHit], bool]:
    """Keyword + semantic blend. Returns (hits, vector_search_used)."""
    keyword_scores = {h.page.id: h.score for h in search(pages, query, limit=len(pages))}
    keyword_max = max(keyword_scores.values(), default=0.0)

    semantic_scores: dict[str, float] = {}
    vector_used = False
    try:
        page_vectors = get_page_embeddings(pages, embed_fn=embed_fn)
        query_vector = embed_query(query, embed_fn=embed_fn)
        semantic_scores = {
            pid: cosine_similarity(query_vector, vector) for pid, vector in page_vectors.items()
        }
        vector_used = True
    except EmbeddingsUnavailable:
        pass

    hits = []
    for page in pages:
        kw = keyword_scores.get(page.id, 0.0)
        kw_norm = kw / keyword_max if keyword_max else 0.0
        sem = semantic_scores.get(page.id, 0.0)

        relevant = kw > 0 or sem >= SEMANTIC_THRESHOLD
        if not relevant:
            continue

        score = SEMANTIC_WEIGHT * sem + (1 - SEMANTIC_WEIGHT) * kw_norm if vector_used else kw_norm
        hits.append(SearchHit(page=page, score=score, keyword_score=kw, semantic_score=sem))

    hits.sort(key=lambda h: h.score, reverse=True)
    return hits[:limit], vector_used
