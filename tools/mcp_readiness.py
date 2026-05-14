#!/usr/bin/env python3
"""Check local MCP readiness for Data360 Beast companion servers."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SERVERS = [
    {
        "name": "sf-docs",
        "repository": "https://github.com/kvirtue123/sf-docs-mcp",
        "requiredFor": "Fresh official Salesforce Help and Developer docs retrieval",
        "runtimeCommands": ["node"],
        "expectedPaths": [
            "~/.data360beast/mcp-servers/sf-docs-mcp/dist/mcp-server.js",
            "~/.codex/mcp-servers/sf-docs-mcp/dist/mcp-server.js"
        ],
        "envAny": []
    },
    {
        "name": "data360",
        "repository": "https://github.com/forcedotcom/d360-mcp-server",
        "requiredFor": "Broad live Data 360 Connect API operations",
        "runtimeCommands": ["java"],
        "expectedPaths": [
            "~/.data360beast/mcp-servers/d360-mcp-server/target/data360-mcp-server-1.0.0.jar",
            "~/.codex/mcp-servers/d360-mcp-server/target/data360-mcp-server-1.0.0.jar"
        ],
        "envAny": [
            ["DATA360_CLIENT_ID", "DATA360_CLIENT_SECRET"],
            ["DATA360_ACCESS_TOKEN", "DATA360_INSTANCE_URL"]
        ]
    },
    {
        "name": "datacloud-mcp-query",
        "repository": "https://github.com/forcedotcom/datacloud-mcp-query",
        "requiredFor": "Query SQL, table listing, and table description only",
        "runtimeCommands": ["python3"],
        "expectedPaths": [
            "~/.data360beast/mcp-servers/datacloud-mcp-query",
            "~/.codex/mcp-servers/datacloud-mcp-query",
            ".venv/datacloud-mcp-query"
        ],
        "envAny": [
            ["SF_ORG_ALIAS"],
            ["SF_TARGET_ORG_ALIAS"],
            ["SF_CLIENT_ID", "SF_CLIENT_SECRET"],
            ["SF_ACCESS_TOKEN", "SF_INSTANCE_URL"]
        ]
    }
]


def expand(path: str) -> Path:
    return (ROOT / path).resolve() if path.startswith(".") else Path(path).expanduser()


def env_group_ready(group: list[str]) -> bool:
    return all(os.environ.get(name) for name in group)


def server_status(server: dict) -> dict:
    command_status = {cmd: shutil.which(cmd) is not None for cmd in server["runtimeCommands"]}
    path_status = {path: expand(path).exists() for path in server["expectedPaths"]}
    env_ready = any(env_group_ready(group) for group in server["envAny"]) if server["envAny"] else True
    installed = any(path_status.values())
    runtime_ready = all(command_status.values())
    ready = installed and runtime_ready and env_ready
    return {
        "name": server["name"],
        "repository": server["repository"],
        "requiredFor": server["requiredFor"],
        "ready": ready,
        "installed": installed,
        "runtimeReady": runtime_ready,
        "envReady": env_ready,
        "commands": command_status,
        "paths": path_status,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text")
    args = parser.parse_args()

    statuses = [server_status(server) for server in SERVERS]
    if args.json:
        print(json.dumps({"servers": statuses}, indent=2))
        return 0

    for status in statuses:
        flag = "READY" if status["ready"] else "MISSING"
        print(f"{flag}: {status['name']} - {status['requiredFor']}")
        if not status["ready"]:
            print(f"  installed={status['installed']} runtime={status['runtimeReady']} env={status['envReady']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
