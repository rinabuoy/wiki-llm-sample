from wikillm.graph import WikiGraph
from wikillm.markdown import parse_page


def _write(tmp_path, name, content):
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return parse_page(path)


class FakeResult:
    def __init__(self, single_value=None):
        self._single_value = single_value

    def single(self):
        return self._single_value


class FakeTx:
    def __init__(self):
        self.queries = []

    def run(self, query, **params):
        self.queries.append((query, params))
        if "DETACH DELETE" in query:
            return FakeResult({"n": 0})
        return FakeResult()


class FakeSession:
    def __init__(self, tx):
        self.tx = tx

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def execute_write(self, fn, *args):
        return fn(self.tx, *args)

    def run(self, query, **params):
        return self.tx.run(query, **params)


def make_graph():
    """Bypass __init__ (which requires a real Neo4j driver) to unit-test the
    Cypher-building logic against a fake session/transaction instead."""
    graph = object.__new__(WikiGraph)
    graph.config = None
    tx = FakeTx()
    graph._session = lambda: FakeSession(tx)
    return graph, tx


def test_sync_upserts_page_tags_links_and_embedding(tmp_path):
    a = _write(tmp_path, "a.md", "---\ntitle: A\ntype: entity\ntags: [x]\n---\n\nSee [[B]].\n")
    b = _write(tmp_path, "b.md", "---\ntitle: B\ntype: concept\n---\n\nbody\n")

    graph, tx = make_graph()
    report = graph.sync([a, b], embeddings={"a.md": [0.1, 0.2]})

    assert report.synced == 2
    assert report.embedded == 1
    assert report.unresolved_links == {}

    queries = [q for q, _ in tx.queries]
    assert any(
        "SET p.embedding" in q and params.get("id") == "a.md" for q, params in tx.queries
    )
    assert not any(
        "SET p.embedding" in q and params.get("id") == "b.md" for q, params in tx.queries
    )
    assert any("MERGE (t:Tag" in q for q in queries)
    assert any("MERGE (p)-[:LINKS_TO]->(q)" in q for q in queries)


def test_sync_reports_unresolved_links(tmp_path):
    a = _write(tmp_path, "a.md", "---\ntitle: A\ntype: entity\n---\n\nSee [[Nowhere]].\n")
    graph, _ = make_graph()
    report = graph.sync([a])
    assert report.unresolved_links == {"a.md": ["Nowhere"]}


def test_sync_with_no_embeddings_skips_embedding_writes(tmp_path):
    a = _write(tmp_path, "a.md", "---\ntitle: A\ntype: entity\n---\n\nbody\n")
    graph, tx = make_graph()
    report = graph.sync([a])
    assert report.embedded == 0
    assert not any("SET p.embedding" in q for q, _ in tx.queries)


def test_ensure_constraints_creates_vector_index(tmp_path):
    graph, tx = make_graph()
    graph.ensure_constraints()
    queries = [q for q, _ in tx.queries]
    assert any("CREATE VECTOR INDEX" in q and "384" in q for q in queries)
    assert any("CREATE FULLTEXT INDEX" in q for q in queries)
