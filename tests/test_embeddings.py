from wikillm.embeddings import cosine_similarity, get_page_embeddings
from wikillm.markdown import parse_page
from wikillm.search import hybrid_search


def _write(tmp_path, name, content):
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return parse_page(path)


def _stub_embed_fn(calls):
    """Deterministic embed: vector = char counts, so identical text -> identical vector."""

    def embed(texts):
        calls.append(list(texts))
        vectors = []
        for text in texts:
            vec = [0.0] * 26
            for ch in text.lower():
                if "a" <= ch <= "z":
                    vec[ord(ch) - ord("a")] += 1.0
            vectors.append(vec)
        return vectors

    return embed


def test_cosine_similarity_basic():
    assert cosine_similarity([1, 0], [1, 0]) == 1.0
    assert cosine_similarity([1, 0], [0, 1]) == 0.0
    assert cosine_similarity([0, 0], [1, 1]) == 0.0


def test_get_page_embeddings_only_recomputes_changed_pages(tmp_path):
    cache_file = tmp_path / "cache.json"
    a = _write(tmp_path, "a.md", "---\ntitle: A\ntype: entity\n---\n\nfirst body\n")
    b = _write(tmp_path, "b.md", "---\ntitle: B\ntype: entity\n---\n\nsecond body\n")

    calls = []
    embed_fn = _stub_embed_fn(calls)

    vectors1 = get_page_embeddings([a, b], embed_fn=embed_fn, cache_file=cache_file)
    assert len(calls) == 1
    assert set(vectors1.keys()) == {"a.md", "b.md"}

    # second call with unchanged pages should hit the cache, not recompute
    vectors2 = get_page_embeddings([a, b], embed_fn=embed_fn, cache_file=cache_file)
    assert len(calls) == 1
    assert vectors2 == vectors1

    # editing one page's body should only re-embed that page
    b.body = "changed body"
    get_page_embeddings([a, b], embed_fn=embed_fn, cache_file=cache_file)
    assert len(calls) == 2
    assert calls[1] == ["B\nchanged body"]


def test_get_page_embeddings_prunes_deleted_pages(tmp_path):
    cache_file = tmp_path / "cache.json"
    a = _write(tmp_path, "a.md", "---\ntitle: A\ntype: entity\n---\n\nbody\n")
    b = _write(tmp_path, "b.md", "---\ntitle: B\ntype: entity\n---\n\nbody\n")
    embed_fn = _stub_embed_fn([])

    get_page_embeddings([a, b], embed_fn=embed_fn, cache_file=cache_file)
    vectors = get_page_embeddings([a], embed_fn=embed_fn, cache_file=cache_file)
    assert set(vectors.keys()) == {"a.md"}

    import json

    assert set(json.loads(cache_file.read_text()).keys()) == {"a.md"}


def test_hybrid_search_falls_back_when_embeddings_unavailable(tmp_path):
    from wikillm.embeddings import EmbeddingsUnavailable

    def raising_embed_fn(texts):
        raise EmbeddingsUnavailable("no model")

    a = _write(tmp_path, "a.md", "---\ntitle: Ada Lovelace\ntype: entity\n---\n\nMathematician.\n")
    hits, vector_used = hybrid_search([a], "Ada Lovelace", embed_fn=raising_embed_fn)
    assert vector_used is False
    assert [h.page.id for h in hits] == ["a.md"]


def test_hybrid_search_surfaces_semantically_similar_page_without_keyword_match(tmp_path):
    # The stub embedding is a per-letter histogram, so "gnitupmoc reenoip" (the
    # query's words, reversed) has an identical vector to "computing pioneer"
    # while sharing zero exact keyword tokens with it — standing in for how a
    # real embedding model matches meaning that keyword search would miss.
    a = _write(
        tmp_path,
        "a.md",
        "---\ntitle: Ada Lovelace\ntype: entity\n---\n\ngnitupmoc reenoip engine notes\n",
    )
    b = _write(
        tmp_path,
        "b.md",
        "---\ntitle: Unrelated\ntype: entity\n---\n\nzzz qqq zzz qqq\n",
    )

    embed_fn = _stub_embed_fn([])
    hits, vector_used = hybrid_search([a, b], "computing pioneer", embed_fn=embed_fn)

    assert vector_used is True
    assert hits[0].page.id == "a.md"
    assert hits[0].keyword_score == 0
    assert hits[0].semantic_score > 0.8
