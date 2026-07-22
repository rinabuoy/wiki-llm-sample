from __future__ import annotations

from dataclasses import dataclass, field

from .config import Neo4jConfig, Neo4jConfigError
from .markdown import WIKILINK_RE, Page, build_resolver

LABEL_MAP = {
    "entity": "Entity",
    "concept": "Concept",
    "source": "Source",
    "topic": "Topic",
    "page": "Page",
}
ALL_TYPE_LABELS = ":".join(sorted(set(LABEL_MAP.values()) - {"Page"}))

EMBEDDING_DIMENSIONS = 384  # BAAI/bge-small-en-v1.5, see wikillm/embeddings.py


@dataclass
class SyncReport:
    synced: int
    deleted: int
    embedded: int
    unresolved_links: dict[str, list[str]] = field(default_factory=dict)


class WikiGraph:
    """Pushes wiki/*.md into Neo4j Aura. Markdown stays the source of truth —
    this is a rebuildable production mirror, never hand-edited."""

    def __init__(self, config: Neo4jConfig | None = None):
        try:
            from neo4j import GraphDatabase
        except ImportError as e:
            raise Neo4jConfigError(
                "neo4j driver is not installed. Run `pip install -e '.[graph]'` "
                "to enable Neo4j Aura sync."
            ) from e
        self.config = config or Neo4jConfig.from_env()
        self.driver = GraphDatabase.driver(
            self.config.uri, auth=(self.config.username, self.config.password)
        )

    def close(self):
        self.driver.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def _session(self):
        return self.driver.session(database=self.config.database)

    def ensure_constraints(self, embedding_dimensions: int = EMBEDDING_DIMENSIONS):
        with self._session() as session:
            session.run(
                "CREATE CONSTRAINT page_id IF NOT EXISTS "
                "FOR (p:Page) REQUIRE p.id IS UNIQUE"
            )
            session.run(
                "CREATE CONSTRAINT tag_name IF NOT EXISTS "
                "FOR (t:Tag) REQUIRE t.name IS UNIQUE"
            )
            session.run(
                "CREATE FULLTEXT INDEX pageFulltext IF NOT EXISTS "
                "FOR (p:Page) ON EACH [p.title, p.body]"
            )
            session.run(
                f"""
                CREATE VECTOR INDEX pageEmbedding IF NOT EXISTS
                FOR (p:Page) ON p.embedding
                OPTIONS {{indexConfig: {{
                    `vector.dimensions`: {embedding_dimensions},
                    `vector.similarity_function`: 'cosine'
                }}}}
                """
            )

    def sync(
        self, pages: list[Page], embeddings: dict[str, list[float]] | None = None
    ) -> SyncReport:
        embeddings = embeddings or {}
        self.ensure_constraints()
        resolver = build_resolver(pages)
        current_ids = {p.id for p in pages}
        unresolved: dict[str, list[str]] = {}

        with self._session() as session:
            deleted = session.execute_write(self._delete_stale, current_ids)
            for page in pages:
                targets = []
                misses = []
                for raw in WIKILINK_RE.findall(page.body):
                    key = raw.strip().lower()
                    target_id = resolver.get(key)
                    if target_id and target_id != page.id:
                        targets.append(target_id)
                    elif not target_id:
                        misses.append(raw.strip())
                if misses:
                    unresolved[page.id] = misses
                session.execute_write(
                    self._upsert_page, page, targets, embeddings.get(page.id)
                )
            session.execute_write(self._prune_orphan_tags)

        return SyncReport(
            synced=len(pages),
            deleted=deleted,
            embedded=len(embeddings),
            unresolved_links=unresolved,
        )

    @staticmethod
    def _delete_stale(tx, current_ids: set[str]) -> int:
        result = tx.run(
            "MATCH (p:Page) WHERE NOT p.id IN $ids "
            "DETACH DELETE p RETURN count(p) AS n",
            ids=list(current_ids),
        )
        return result.single()["n"]

    @staticmethod
    def _upsert_page(tx, page: Page, link_target_ids: list[str], embedding: list[float] | None):
        label = LABEL_MAP.get(page.type, "Page")
        tx.run(
            f"""
            MERGE (p:Page {{id: $id}})
            REMOVE p:{ALL_TYPE_LABELS}
            SET p:{label},
                p.title = $title,
                p.type = $type,
                p.tags = $tags,
                p.aliases = $aliases,
                p.created = $created,
                p.updated = $updated,
                p.body = $body,
                p.path = $path
            """,
            id=page.id,
            title=page.title,
            type=page.type,
            tags=page.tags,
            aliases=page.aliases,
            created=page.created,
            updated=page.updated,
            body=page.body,
            path=str(page.path),
        )

        if embedding is not None:
            tx.run(
                "MATCH (p:Page {id: $id}) SET p.embedding = $embedding",
                id=page.id,
                embedding=embedding,
            )

        tx.run("MATCH (p:Page {id: $id})-[r:HAS_TAG]->() DELETE r", id=page.id)
        for tag in page.tags:
            tx.run(
                """
                MATCH (p:Page {id: $id})
                MERGE (t:Tag {name: $tag})
                MERGE (p)-[:HAS_TAG]->(t)
                """,
                id=page.id,
                tag=tag,
            )

        tx.run("MATCH (p:Page {id: $id})-[r:LINKS_TO]->() DELETE r", id=page.id)
        for target_id in link_target_ids:
            tx.run(
                """
                MATCH (p:Page {id: $id})
                MATCH (q:Page {id: $target_id})
                MERGE (p)-[:LINKS_TO]->(q)
                """,
                id=page.id,
                target_id=target_id,
            )

        tx.run("MATCH (p:Page {id: $id})-[r:DERIVED_FROM]->() DELETE r", id=page.id)
        for source_id in page.sources:
            tx.run(
                """
                MATCH (p:Page {id: $id})
                MATCH (s:Page {id: $source_id})
                MERGE (p)-[:DERIVED_FROM]->(s)
                """,
                id=page.id,
                source_id=source_id,
            )

    @staticmethod
    def _prune_orphan_tags(tx):
        tx.run("MATCH (t:Tag) WHERE NOT (t)<-[:HAS_TAG]-() DELETE t")

    def search_fulltext(self, query: str, limit: int = 10) -> list[dict]:
        with self._session() as session:
            result = session.run(
                """
                CALL db.index.fulltext.queryNodes('pageFulltext', $query)
                YIELD node, score
                RETURN node.id AS id, node.title AS title, node.type AS type, score
                ORDER BY score DESC
                LIMIT $limit
                """,
                query=query,
                limit=limit,
            )
            return [dict(r) for r in result]

    def search_vector(self, query_vector: list[float], limit: int = 10) -> list[dict]:
        with self._session() as session:
            result = session.run(
                """
                MATCH (p:Page)
                SEARCH p IN (VECTOR INDEX pageEmbedding FOR $vector LIMIT $limit) SCORE AS score
                RETURN p.id AS id, p.title AS title, p.type AS type, score
                ORDER BY score DESC
                """,
                vector=query_vector,
                limit=limit,
            )
            return [dict(r) for r in result]

    def stats(self) -> dict:
        with self._session() as session:
            by_type = session.run(
                "MATCH (p:Page) RETURN p.type AS type, count(*) AS n ORDER BY n DESC"
            ).data()
            rel_counts = session.run(
                "MATCH ()-[r]->() RETURN type(r) AS rel, count(*) AS n ORDER BY n DESC"
            ).data()
            orphans = session.run(
                "MATCH (p:Page) WHERE NOT (p)--() "
                "RETURN p.id AS id, p.title AS title ORDER BY p.title"
            ).data()
            hubs = session.run(
                """
                MATCH (p:Page)
                OPTIONAL MATCH (p)-[r:LINKS_TO]-()
                WITH p, count(r) AS degree
                RETURN p.id AS id, p.title AS title, degree
                ORDER BY degree DESC
                LIMIT 10
                """
            ).data()
            embedded = session.run(
                "MATCH (p:Page) WHERE p.embedding IS NOT NULL RETURN count(p) AS n"
            ).single()["n"]
            return {
                "by_type": by_type,
                "relationships": rel_counts,
                "orphans": orphans,
                "hubs": hubs,
                "embedded": embedded,
            }
