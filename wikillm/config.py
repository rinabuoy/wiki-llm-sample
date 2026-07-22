import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = ROOT / "wiki"
RAW_DIR = ROOT / "raw"
INDEX_FILE = WIKI_DIR / "index.md"
LOG_FILE = WIKI_DIR / "log.md"

PAGE_TYPES = ("entity", "concept", "source", "topic", "page")


class Neo4jConfigError(RuntimeError):
    pass


@dataclass(frozen=True)
class Neo4jConfig:
    uri: str
    username: str
    password: str
    database: str = "neo4j"

    @classmethod
    def from_env(cls) -> "Neo4jConfig":
        try:
            from dotenv import load_dotenv
        except ImportError as e:
            raise Neo4jConfigError(
                "python-dotenv is not installed. Run `pip install -e '.[graph]'` "
                "to enable Neo4j Aura sync."
            ) from e
        load_dotenv(ROOT / ".env")

        uri = os.environ.get("NEO4J_URI")
        username = os.environ.get("NEO4J_USERNAME")
        password = os.environ.get("NEO4J_PASSWORD")
        database = os.environ.get("NEO4J_DATABASE", "neo4j")
        missing = [
            name
            for name, val in [
                ("NEO4J_URI", uri),
                ("NEO4J_USERNAME", username),
                ("NEO4J_PASSWORD", password),
            ]
            if not val
        ]
        if missing:
            raise Neo4jConfigError(
                f"Missing env vars: {', '.join(missing)}. "
                f"Copy .env.example to .env and fill in your Neo4j Aura credentials."
            )
        return cls(uri=uri, username=username, password=password, database=database)
