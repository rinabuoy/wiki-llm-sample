from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Callable

from .config import ROOT
from .markdown import Page

CACHE_FILE = ROOT / ".wikillm_cache" / "embeddings.json"
MODEL_NAME = "BAAI/bge-small-en-v1.5"

EmbedFn = Callable[[list[str]], list[list[float]]]

_model = None


class EmbeddingsUnavailable(RuntimeError):
    pass


def _default_embed_fn(texts: list[str]) -> list[list[float]]:
    global _model
    if _model is None:
        try:
            from fastembed import TextEmbedding
        except ImportError as e:
            raise EmbeddingsUnavailable(
                "fastembed is not installed. Run `pip install -e '.[vector]'` "
                "to enable semantic search."
            ) from e
        _model = TextEmbedding(model_name=MODEL_NAME)
    return [vec.tolist() for vec in _model.embed(texts)]


def _content_hash(page: Page) -> str:
    text = f"{page.title}\n{' '.join(sorted(page.tags))}\n{page.body}"
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _load_cache(cache_file: Path) -> dict:
    if not cache_file.exists():
        return {}
    return json.loads(cache_file.read_text(encoding="utf-8"))


def _save_cache(cache_file: Path, cache: dict):
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps(cache), encoding="utf-8")


def get_page_embeddings(
    pages: list[Page],
    embed_fn: EmbedFn | None = None,
    cache_file: Path = CACHE_FILE,
) -> dict[str, list[float]]:
    embed_fn = embed_fn or _default_embed_fn
    cache = _load_cache(cache_file)

    stale = []
    for page in pages:
        h = _content_hash(page)
        entry = cache.get(page.id)
        if entry is None or entry["hash"] != h:
            stale.append((page, h))

    if stale:
        vectors = embed_fn([f"{p.title}\n{p.body}" for p, _ in stale])
        for (page, h), vector in zip(stale, vectors):
            cache[page.id] = {"hash": h, "vector": vector}

    current_ids = {p.id for p in pages}
    removed = [pid for pid in cache if pid not in current_ids]
    for pid in removed:
        del cache[pid]

    if stale or removed:
        _save_cache(cache_file, cache)

    return {page.id: cache[page.id]["vector"] for page in pages}


def embed_query(query: str, embed_fn: EmbedFn | None = None) -> list[float]:
    embed_fn = embed_fn or _default_embed_fn
    return embed_fn([query])[0]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
