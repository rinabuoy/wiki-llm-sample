from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = ROOT / "wiki"
RAW_DIR = ROOT / "raw"
INDEX_FILE = WIKI_DIR / "index.md"
LOG_FILE = WIKI_DIR / "log.md"

PAGE_TYPES = ("entity", "concept", "source", "topic", "page")
