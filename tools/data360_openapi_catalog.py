#!/usr/bin/env python3
"""Build and query a compact Data 360 Connect API catalog from OpenAPI YAML."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml


DEFAULT_SPEC = Path("docs/data360/connectapi/cdp-connect-api-Swagger.yaml")
DEFAULT_OUTDIR = Path("docs/data360/connectapi")
HTTP_METHODS = {"get", "put", "post", "delete", "patch", "head", "options", "trace"}


def clean_text(value: Any, limit: int | None = None) -> str:
    if value is None:
        return ""
    text = str(value)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if limit and len(text) > limit:
        return text[: limit - 1].rstrip() + "..."
    return text


def ref_name(ref: str | None) -> str:
    if not ref:
        return ""
    return ref.rsplit("/", 1)[-1]


def schema_brief(schema: Any) -> dict[str, Any]:
    if not isinstance(schema, dict):
        return {}
    if "$ref" in schema:
        return {"ref": ref_name(schema.get("$ref"))}
    if "allOf" in schema:
        return {"allOf": [schema_brief(item) for item in schema.get("allOf", [])]}
    if "oneOf" in schema:
        return {"oneOf": [schema_brief(item) for item in schema.get("oneOf", [])]}
    if "anyOf" in schema:
        return {"anyOf": [schema_brief(item) for item in schema.get("anyOf", [])]}
    kind = schema.get("type")
    if kind == "array":
        return {"type": "array", "items": schema_brief(schema.get("items", {}))}
    brief: dict[str, Any] = {}
    if kind:
        brief["type"] = kind
    if schema.get("format"):
        brief["format"] = schema["format"]
    if schema.get("enum"):
        enum = schema["enum"]
        brief["enum"] = enum[:20] if isinstance(enum, list) else enum
    props = schema.get("properties")
    if isinstance(props, dict):
        brief["properties"] = {
            name: schema_brief(prop) for name, prop in list(props.items())[:25]
        }
        if len(props) > 25:
            brief["propertyCount"] = len(props)
    if schema.get("required"):
        brief["required"] = schema["required"]
    return brief


def schema_label(schema: Any) -> str:
    brief = schema_brief(schema)
    if not brief:
        return ""
    if "ref" in brief:
        return brief["ref"]
    if "type" in brief:
        if brief["type"] == "array":
            items = brief.get("items", {})
            if isinstance(items, dict) and items.get("ref"):
                return f"array<{items['ref']}>"
            if isinstance(items, dict) and items.get("type"):
                return f"array<{items['type']}>"
            return "array"
        return str(brief["type"])
    for combiner in ("allOf", "oneOf", "anyOf"):
        if combiner in brief:
            labels = [schema_label(item) for item in brief[combiner]]
            labels = [label for label in labels if label]
            return f"{combiner}({', '.join(labels[:4])})"
    return ""


def infer_family(path: str, operation: dict[str, Any]) -> str:
    tags = operation.get("tags")
    if isinstance(tags, list) and tags:
        return clean_text(tags[0])
    parts = [part for part in path.split("/") if part and not part.startswith("{")]
    if not parts:
        return "General"
    if parts[0] == "ssot" and len(parts) > 1:
        return parts[1].replace("-", " ").title()
    return parts[0].replace("-", " ").title()


def availability_text(operation: dict[str, Any]) -> str:
    blob = " ".join(
        clean_text(operation.get(key))
        for key in ("description", "summary")
        if operation.get(key)
    )
    patterns = [
        r"Available Version:\*{0,2}\s*([0-9.]+)",
        r"available in API version\s+([0-9.]+)",
        r"available as of API version\s+([0-9.]+)",
        r"API version\s+([0-9.]+)\s+and later",
        r"version\s+([0-9.]+)\s+and later",
    ]
    for pattern in patterns:
        match = re.search(pattern, blob, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    for key in ("x-sfdc-min-api-version", "x-min-api-version", "x-api-version"):
        if operation.get(key):
            return str(operation[key])
    return ""


def extract_parameters(
    path_parameters: list[dict[str, Any]], operation: dict[str, Any]
) -> list[dict[str, Any]]:
    merged = []
    seen: set[tuple[str, str]] = set()
    for param in path_parameters + operation.get("parameters", []):
        if not isinstance(param, dict):
            continue
        key = (param.get("name", ""), param.get("in", ""))
        if key in seen:
            continue
        seen.add(key)
        schema = param.get("schema", {})
        merged.append(
            {
                "name": param.get("name", ""),
                "in": param.get("in", ""),
                "required": bool(param.get("required")),
                "schema": schema_brief(schema),
                "description": clean_text(param.get("description"), 240),
            }
        )
    return merged


def extract_request_body(operation: dict[str, Any]) -> dict[str, Any]:
    body = operation.get("requestBody")
    if not isinstance(body, dict):
        return {}
    content = body.get("content", {})
    content_entries = []
    if isinstance(content, dict):
        for content_type, payload in content.items():
            if not isinstance(payload, dict):
                continue
            examples = []
            if "example" in payload:
                examples.append("inline")
            if isinstance(payload.get("examples"), dict):
                examples.extend(payload["examples"].keys())
            content_entries.append(
                {
                    "contentType": content_type,
                    "schema": schema_brief(payload.get("schema", {})),
                    "schemaLabel": schema_label(payload.get("schema", {})),
                    "examples": examples[:20],
                }
            )
    return {
        "required": bool(body.get("required")),
        "description": clean_text(body.get("description"), 240),
        "content": content_entries,
    }


def extract_responses(operation: dict[str, Any]) -> list[dict[str, Any]]:
    responses = operation.get("responses", {})
    result = []
    if not isinstance(responses, dict):
        return result
    for status, response in responses.items():
        if not isinstance(response, dict):
            continue
        content = response.get("content", {})
        content_entries = []
        if isinstance(content, dict):
            for content_type, payload in content.items():
                if not isinstance(payload, dict):
                    continue
                content_entries.append(
                    {
                        "contentType": content_type,
                        "schema": schema_brief(payload.get("schema", {})),
                        "schemaLabel": schema_label(payload.get("schema", {})),
                    }
                )
        result.append(
            {
                "status": str(status),
                "description": clean_text(response.get("description"), 240),
                "content": content_entries,
            }
        )
    return result


def collect_operations(spec: dict[str, Any]) -> list[dict[str, Any]]:
    operations = []
    paths = spec.get("paths", {})
    if not isinstance(paths, dict):
        return operations
    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        path_parameters = [
            param for param in path_item.get("parameters", []) if isinstance(param, dict)
        ]
        for method, operation in path_item.items():
            if method.lower() not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            family = infer_family(path, operation)
            operations.append(
                {
                    "family": family,
                    "method": method.upper(),
                    "path": path,
                    "operationId": operation.get("operationId", ""),
                    "summary": clean_text(operation.get("summary"), 220),
                    "description": clean_text(operation.get("description"), 500),
                    "availability": availability_text(operation),
                    "tags": operation.get("tags", []),
                    "parameters": extract_parameters(path_parameters, operation),
                    "requestBody": extract_request_body(operation),
                    "responses": extract_responses(operation),
                    "security": operation.get("security", []),
                }
            )
    return sorted(operations, key=lambda item: (item["family"], item["path"], item["method"]))


def collect_schemas(spec: dict[str, Any]) -> list[dict[str, Any]]:
    schemas = spec.get("components", {}).get("schemas", {})
    if not isinstance(schemas, dict):
        return []
    result = []
    for name, schema in schemas.items():
        if not isinstance(schema, dict):
            continue
        props = schema.get("properties", {})
        result.append(
            {
                "name": name,
                "type": schema.get("type", ""),
                "description": clean_text(schema.get("description"), 320),
                "required": schema.get("required", []),
                "propertyCount": len(props) if isinstance(props, dict) else 0,
                "properties": {
                    prop_name: {
                        "schema": schema_brief(prop_schema),
                        "description": clean_text(
                            prop_schema.get("description") if isinstance(prop_schema, dict) else "",
                            180,
                        ),
                    }
                    for prop_name, prop_schema in list(props.items())[:50]
                    if isinstance(prop_schema, dict)
                }
                if isinstance(props, dict)
                else {},
            }
        )
    return sorted(result, key=lambda item: item["name"].lower())


def family_summary(operations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for operation in operations:
        grouped[operation["family"]].append(operation)
    summaries = []
    for family, items in grouped.items():
        methods = defaultdict(int)
        for item in items:
            methods[item["method"]] += 1
        examples = [
            {
                "method": item["method"],
                "path": item["path"],
                "summary": item["summary"],
                "operationId": item["operationId"],
            }
            for item in items[:8]
        ]
        summaries.append(
            {
                "family": family,
                "operationCount": len(items),
                "methods": dict(sorted(methods.items())),
                "examples": examples,
            }
        )
    return sorted(summaries, key=lambda item: (-item["operationCount"], item["family"].lower()))


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def markdown_table(rows: list[list[str]], headers: list[str]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell.replace("|", "\\|") for cell in row) + " |")
    return "\n".join(lines)


def write_markdown_indexes(
    outdir: Path,
    spec: dict[str, Any],
    operations: list[dict[str, Any]],
    families: list[dict[str, Any]],
    schemas: list[dict[str, Any]],
) -> None:
    info = spec.get("info", {})
    summary = [
        "# Salesforce Data 360 Connect REST API Catalog",
        "",
        f"- Title: {clean_text(info.get('title'))}",
        f"- Version: {clean_text(info.get('version'))}",
        f"- Operations: {len(operations)}",
        f"- Families: {len(families)}",
        f"- Component schemas: {len(schemas)}",
        "",
        "Generated from the official OpenAPI YAML. Keep endpoint detail here and keep skills concise.",
        "",
        "Use `python3 tools/data360_openapi_catalog.py search <term>` from the project root for fast lookup.",
        "",
    ]
    outdir.joinpath("api-surface-summary.md").write_text("\n".join(summary), encoding="utf-8")

    family_rows = []
    for family in families:
        methods = ", ".join(f"{method} {count}" for method, count in family["methods"].items())
        examples = "; ".join(
            f"{item['method']} {item['path']}" for item in family["examples"][:3]
        )
        family_rows.append([family["family"], str(family["operationCount"]), methods, examples])
    outdir.joinpath("family-index.md").write_text(
        "# Data 360 Connect API Families\n\n"
        + markdown_table(family_rows, ["Family", "Operations", "Methods", "Representative endpoints"])
        + "\n",
        encoding="utf-8",
    )

    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for operation in operations:
        by_family[operation["family"]].append(operation)
    chunks = ["# Data 360 Connect API Endpoint Index", ""]
    for family in sorted(by_family.keys(), key=str.lower):
        chunks.extend([f"## {family}", ""])
        rows = []
        for item in by_family[family]:
            params = ", ".join(
                f"{param['name']}:{param['in']}{'*' if param['required'] else ''}"
                for param in item["parameters"]
            )
            request = ", ".join(
                entry.get("schemaLabel", "")
                for entry in item.get("requestBody", {}).get("content", [])
                if entry.get("schemaLabel")
            )
            responses = ", ".join(
                f"{response['status']} {', '.join(entry.get('schemaLabel', '') for entry in response.get('content', []) if entry.get('schemaLabel'))}".strip()
                for response in item["responses"][:6]
            )
            rows.append(
                [
                    item["method"],
                    item["path"],
                    item["operationId"],
                    item["summary"],
                    params,
                    request,
                    responses,
                ]
            )
        chunks.append(
            markdown_table(
                rows,
                ["Method", "Path", "Operation ID", "Summary", "Parameters", "Request", "Responses"],
            )
        )
        chunks.append("")
    outdir.joinpath("endpoint-index.md").write_text("\n".join(chunks), encoding="utf-8")


def build_catalog(spec_path: Path, outdir: Path) -> None:
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    if not isinstance(spec, dict):
        raise SystemExit(f"Unable to parse OpenAPI spec: {spec_path}")
    operations = collect_operations(spec)
    schemas = collect_schemas(spec)
    families = family_summary(operations)
    outdir.mkdir(parents=True, exist_ok=True)
    catalog = {
        "source": str(spec_path),
        "title": clean_text(spec.get("info", {}).get("title")),
        "version": clean_text(spec.get("info", {}).get("version")),
        "operationCount": len(operations),
        "familyCount": len(families),
        "schemaCount": len(schemas),
        "families": families,
        "operations": operations,
    }
    compact = [
        {
            "family": item["family"],
            "method": item["method"],
            "path": item["path"],
            "operationId": item["operationId"],
            "summary": item["summary"],
            "availability": item["availability"],
        }
        for item in operations
    ]
    write_json(outdir / "endpoint-catalog.json", catalog)
    write_json(outdir / "endpoint-catalog.compact.json", compact)
    write_json(outdir / "schema-catalog.json", schemas)
    write_markdown_indexes(outdir, spec, operations, families, schemas)
    print(
        f"Wrote {len(operations)} operations, {len(families)} families, "
        f"and {len(schemas)} schemas to {outdir}"
    )


def load_catalog(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def search_catalog(catalog_path: Path, query: str, limit: int) -> None:
    catalog = load_catalog(catalog_path)
    terms = [term.lower() for term in query.split() if term.strip()]
    matches = []
    for item in catalog.get("operations", []):
        haystack = " ".join(
            str(item.get(key, ""))
            for key in ("family", "method", "path", "operationId", "summary", "description")
        ).lower()
        if all(term in haystack for term in terms):
            matches.append(item)
    rows = []
    for item in matches[:limit]:
        rows.append(
            [
                item.get("family", ""),
                item.get("method", ""),
                item.get("path", ""),
                item.get("operationId", ""),
                item.get("summary", ""),
            ]
        )
    if not rows:
        print("No matching endpoints.")
        return
    print(markdown_table(rows, ["Family", "Method", "Path", "Operation ID", "Summary"]))
    if len(matches) > limit:
        print(f"\nShowing {limit} of {len(matches)} matches.")


def show_operation(catalog_path: Path, selector: str) -> None:
    catalog = load_catalog(catalog_path)
    selector_lower = selector.lower()
    for item in catalog.get("operations", []):
        candidates = [
            item.get("operationId", ""),
            f"{item.get('method', '')} {item.get('path', '')}",
            item.get("path", ""),
        ]
        if any(selector_lower == candidate.lower() for candidate in candidates):
            print(json.dumps(item, indent=2, sort_keys=True))
            return
    for item in catalog.get("operations", []):
        haystack = " ".join(
            str(item.get(key, "")) for key in ("operationId", "method", "path", "summary")
        ).lower()
        if selector_lower in haystack:
            print(json.dumps(item, indent=2, sort_keys=True))
            return
    print("No matching operation.", file=sys.stderr)
    raise SystemExit(1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command")

    build = subparsers.add_parser("build", help="Build catalog files from OpenAPI YAML")
    build.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    build.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)

    search = subparsers.add_parser("search", help="Search generated endpoint catalog")
    search.add_argument("query")
    search.add_argument("--catalog", type=Path, default=DEFAULT_OUTDIR / "endpoint-catalog.json")
    search.add_argument("--limit", type=int, default=30)

    show = subparsers.add_parser("show", help="Show one generated endpoint entry as JSON")
    show.add_argument("selector")
    show.add_argument("--catalog", type=Path, default=DEFAULT_OUTDIR / "endpoint-catalog.json")

    args = parser.parse_args(argv)
    if args.command in (None, "build"):
        build_catalog(args.spec, args.outdir)
    elif args.command == "search":
        search_catalog(args.catalog, args.query, args.limit)
    elif args.command == "show":
        show_operation(args.catalog, args.selector)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
