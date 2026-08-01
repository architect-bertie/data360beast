#!/usr/bin/env python3
"""Attach public Data360 Beast claims and decisions to the existing docs graph."""

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("docs_watch", ROOT / "tools" / "docs_watch.py")
docs_watch = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(docs_watch)


def main() -> int:
    path = ROOT / "docs" / "data360" / "docs-knowledge-graph.json"
    graph = json.loads(path.read_text(encoding="utf-8"))
    updated = docs_watch.attach_knowledge_nodes(graph, docs_watch.phase_data())
    path.write_text(json.dumps(updated, indent=2) + "\n", encoding="utf-8")
    print(f"OK: knowledge graph now has {len(updated['nodes'])} nodes and {len(updated['edges'])} edges")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
