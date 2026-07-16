from __future__ import annotations

from dataclasses import dataclass

from neo4j import GraphDatabase

from .config import Neo4jConfig
from .markdown import Page, WIKILINK_RE

LABEL_MAP = {
    "entity": "Entity",
    "concept": "Concept",
    "source": "Source",
    "topic": "Topic",
    "page": "Page",
}
ALL_TYPE_LABELS = ":".join(sorted(set(LABEL_MAP.values()) - {"Page"}))


@dataclass
class SyncReport:
    synced: int
    deleted: int
    unresolved_links: dict[str, list[str]]


class WikiGraph:
    def __init__(self, config: Neo4jConfig | None = None):
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

    def ensure_constraints(self):
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

    @staticmethod
    def _build_resolver(pages: list[Page]) -> dict[str, str]:
        resolver: dict[str, str] = {}
        for page in pages:
            keys = {page.title, page.path.stem, *page.aliases}
            for key in keys:
                resolver[key.strip().lower()] = page.id
        return resolver

    def sync(self, pages: list[Page]) -> SyncReport:
        self.ensure_constraints()
        resolver = self._build_resolver(pages)
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
                session.execute_write(self._upsert_page, page, targets)
            session.execute_write(self._prune_orphan_tags)

        return SyncReport(synced=len(pages), deleted=deleted, unresolved_links=unresolved)

    @staticmethod
    def _delete_stale(tx, current_ids: set[str]) -> int:
        result = tx.run(
            "MATCH (p:Page) WHERE NOT p.id IN $ids "
            "DETACH DELETE p RETURN count(p) AS n",
            ids=list(current_ids),
        )
        return result.single()["n"]

    @staticmethod
    def _upsert_page(tx, page: Page, link_target_ids: list[str]):
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

        tx.run(
            "MATCH (p:Page {id: $id})-[r:HAS_TAG]->() DELETE r", id=page.id
        )
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

        tx.run(
            "MATCH (p:Page {id: $id})-[r:LINKS_TO]->() DELETE r", id=page.id
        )
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

        tx.run(
            "MATCH (p:Page {id: $id})-[r:DERIVED_FROM]->() DELETE r", id=page.id
        )
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

    def search(self, query: str, limit: int = 10) -> list[dict]:
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
            return {
                "by_type": by_type,
                "relationships": rel_counts,
                "orphans": orphans,
                "hubs": hubs,
            }
