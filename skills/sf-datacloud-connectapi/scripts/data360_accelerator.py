#!/usr/bin/env python3
import argparse
import html
import json
import pathlib
import re
import sys
import textwrap
import urllib.request
from collections import Counter


DMO_BLOCK_RE = re.compile(
    r'<p><a href="(?P<href>/docs/data/data-cloud-dmo-mapping/guide/c360dm-[^"]+\.html)" '
    r'class="internal-link-guide"><strong>(?P<label>[^<]+)</strong></a></p>\s*'
    r'<p>(?P<description>.*?)</p>',
    re.S,
)


def read_text(source: str) -> str:
    if source.startswith("http://") or source.startswith("https://"):
        with urllib.request.urlopen(source) as response:
            return response.read().decode("utf-8", errors="replace")
    return pathlib.Path(source).read_text(encoding="utf-8")


def load_postman(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as handle:
        payload = json.load(handle)

    rows: list[dict] = []

    def walk(node, group=None):
        if isinstance(node, dict):
            if "request" in node:
                request = node.get("request", {})
                url = request.get("url", {})
                raw = url.get("raw", "") if isinstance(url, dict) else ""
                rows.append(
                    {
                        "group": group or "Ungrouped",
                        "name": node.get("name"),
                        "method": request.get("method"),
                        "url": raw,
                    }
                )
            children = node.get("item", [])
            if isinstance(children, list):
                for child in children:
                    walk(child, node.get("name", group))
        elif isinstance(node, list):
            for child in node:
                walk(child, group)

    walk(payload)
    return rows


def extract_dmos(source: str) -> list[dict]:
    page = read_text(source)
    dmos = []
    seen = set()
    for match in DMO_BLOCK_RE.finditer(page):
        label = html.unescape(match.group("label")).strip()
        href = html.unescape(match.group("href")).strip()
        description = clean_html_text(match.group("description"))
        if label in seen:
            continue
        seen.add(label)
        dmos.append(
            {
                "label": label,
                "href": "https://developer.salesforce.com" + href,
                "description": description,
            }
        )
    return dmos


def clean_html_text(value: str) -> str:
    text = re.sub(r"<[^>]+>", "", value)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def build_endpoint_summary(rows: list[dict]) -> dict:
    grouped = Counter(row["group"] for row in rows)
    return {
        "endpointCount": len(rows),
        "groups": dict(sorted(grouped.items(), key=lambda item: item[0].lower())),
    }


def build_dmo_connect_map(dmos: list[dict]) -> list[dict]:
    return [
        {
            "label": dmo["label"],
            "docUrl": dmo["href"],
            "description": dmo["description"],
            "runtimeNameResolution": [
                "GET /ssot/profile/metadata",
                "GET /ssot/profile/metadata/:dataModelName",
                "GET /ssot/data-model-objects",
                "GET /ssot/data-model-objects/:dataModelObjectName",
            ],
            "genericConnectEndpoints": [
                "GET /ssot/profile/:dataModelName",
                "GET /ssot/profile/:dataModelName/:id",
                "GET /ssot/profile/:dataModelName/:id/:childDataModelName",
                "GET /ssot/profile/:dataModelName/:id/calculated-insights/:ciName",
                "POST /ssot/queryv2",
                "POST /ssot/query-sql",
            ],
            "note": (
                "The documentation label is not guaranteed to match the runtime profile "
                "or table API name. Resolve the actual dataModelName through metadata first."
            ),
        }
        for dmo in dmos
    ]


def print_json(value):
    print(json.dumps(value, indent=2))


def command_summarize_postman(args):
    rows = load_postman(args.postman)
    print_json(build_endpoint_summary(rows))


def command_search_endpoints(args):
    query = args.query.lower()
    matches = [
        row
        for row in load_postman(args.postman)
        if query in (row["group"] or "").lower()
        or query in (row["name"] or "").lower()
        or query in (row["url"] or "").lower()
    ]
    print_json(matches[: args.limit])


def command_extract_dmos(args):
    print_json(extract_dmos(args.dmo_html))


def command_dmo_connect_map(args):
    dmos = extract_dmos(args.dmo_html)
    if args.label:
        normalized = args.label.lower()
        dmos = [dmo for dmo in dmos if dmo["label"].lower() == normalized]
    print_json(build_dmo_connect_map(dmos))


def command_build_catalogs(args):
    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = load_postman(args.postman)
    dmos = extract_dmos(args.dmo_html)
    endpoint_summary = build_endpoint_summary(rows)
    dmo_map = build_dmo_connect_map(dmos)

    (out_dir / "postman_endpoint_catalog.json").write_text(
        json.dumps(rows, indent=2), encoding="utf-8"
    )
    (out_dir / "postman_endpoint_families.json").write_text(
        json.dumps(endpoint_summary, indent=2), encoding="utf-8"
    )
    (out_dir / "dmo_catalog.json").write_text(
        json.dumps(dmos, indent=2), encoding="utf-8"
    )
    (out_dir / "dmo_connect_map.json").write_text(
        json.dumps(dmo_map, indent=2), encoding="utf-8"
    )
    (out_dir / "connectapi_quickref.md").write_text(
        build_quickref_markdown(endpoint_summary, dmos), encoding="utf-8"
    )

    print_json(
        {
            "written": [
                str(out_dir / "postman_endpoint_catalog.json"),
                str(out_dir / "postman_endpoint_families.json"),
                str(out_dir / "dmo_catalog.json"),
                str(out_dir / "dmo_connect_map.json"),
                str(out_dir / "connectapi_quickref.md"),
            ],
            "endpointCount": endpoint_summary["endpointCount"],
            "dmoCount": len(dmos),
        }
    )


def build_quickref_markdown(endpoint_summary: dict, dmos: list[dict]) -> str:
    groups = "\n".join(
        f"- {name}: {count}"
        for name, count in sorted(
            endpoint_summary["groups"].items(), key=lambda item: (-item[1], item[0].lower())
        )
    )
    samples = "\n".join(f"- {dmo['label']}: {dmo['href']}" for dmo in dmos[:20])
    return textwrap.dedent(
        f"""\
        # Data 360 Connect API Quick Reference

        Endpoint count: {endpoint_summary["endpointCount"]}

        ## Endpoint families
        {groups}

        ## Sample DMOs
        {samples}

        ## Generic DMO retrieval pattern
        - GET /ssot/profile/metadata
        - GET /ssot/profile/metadata/:dataModelName
        - GET /ssot/profile/:dataModelName
        - GET /ssot/profile/:dataModelName/:id
        - POST /ssot/queryv2
        - POST /ssot/query-sql
        """
    )


def command_mcp_snippet(args):
    env = {
        "SF_TARGET_ORG_ALIAS": args.target_org,
        "DEFAULT_LIST_TABLE_FILTER": args.table_filter,
        "SF_API_VERSION": args.api_version,
    }
    if args.dataspace:
        env["DEFAULT_DATASPACE"] = args.dataspace
    if args.workload_name:
        env["DEFAULT_WORKLOAD_NAME"] = args.workload_name
    snippet = {
        "mcpServers": {
            args.server_name: {
                "command": args.python,
                "args": [args.server],
                "env": env,
            }
        }
    }
    print_json(snippet)


def command_write_mcp_config(args):
    env = {
        "SF_TARGET_ORG_ALIAS": args.target_org,
        "DEFAULT_LIST_TABLE_FILTER": args.table_filter,
        "SF_API_VERSION": args.api_version,
    }
    if args.dataspace:
        env["DEFAULT_DATASPACE"] = args.dataspace
    if args.workload_name:
        env["DEFAULT_WORKLOAD_NAME"] = args.workload_name

    payload = {
        "mcpServers": {
            args.server_name: {
                "command": args.python,
                "args": [args.server],
                "env": env,
            }
        }
    }
    out_path = pathlib.Path(args.out)
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print_json({"written": str(out_path)})


def command_snippet(args):
    snippets = {
        "apex-query": textwrap.dedent(
            """\
            ConnectApi.CdpQueryInput input = new ConnectApi.CdpQueryInput();
            input.sql = 'SELECT COUNT(*) total_count FROM ssot__Individual__dlm';
            ConnectApi.CdpQueryOutputV2 output = ConnectApi.CdpQuery.queryAnsiSqlV2(input);
            List<Object> rowData = output.data[0].rowData;
            """
        ),
        "apex-segment-create": textwrap.dedent(
            """\
            ConnectApi.CdpSegmentDbtModelInput model = new ConnectApi.CdpSegmentDbtModelInput();
            model.name = 'segment_model';
            model.sql = 'SELECT ssot__Individual__dlm.ssot__Id__c FROM ssot__Individual__dlm';

            ConnectApi.CdpSegmentDbtInput dbt = new ConnectApi.CdpSegmentDbtInput();
            dbt.models = new List<ConnectApi.CdpSegmentDbtModelInput>{ model };

            ConnectApi.CdpSegmentInput input = new ConnectApi.CdpSegmentInput();
            input.developerName = 'my_segment';
            input.displayName = 'My Segment';
            input.segmentOnApiName = 'ssot__Individual__dlm';
            input.segmentType = ConnectApi.SegmentType.Dbt;
            input.publishSchedule = ConnectApi.PublishSchedule.NoRefresh;
            input.includeDbt = dbt;

            ConnectApi.CdpSegmentOutput output = ConnectApi.CdpSegment.createSegment(input);
            """
        ),
        "curl-query-sql": textwrap.dedent(
            """\
            curl -X POST "$INSTANCE_URL/services/data/v66.0/ssot/query-sql?dataspace=default" \\
              -H "Authorization: Bearer $ACCESS_TOKEN" \\
              -H "Content-Type: application/json" \\
              -d '{"sql":"SELECT COUNT(*) FROM ssot__Individual__dlm"}'
            """
        ),
    }
    snippet = snippets.get(args.kind)
    if snippet is None:
        raise SystemExit(f"Unknown snippet kind: {args.kind}")
    print(snippet.rstrip())


def build_parser():
    parser = argparse.ArgumentParser(description="Data 360 Connect API accelerator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    summarize_postman = subparsers.add_parser("summarize-postman")
    summarize_postman.add_argument("--postman", required=True)
    summarize_postman.set_defaults(func=command_summarize_postman)

    search_endpoints = subparsers.add_parser("search-endpoints")
    search_endpoints.add_argument("--postman", required=True)
    search_endpoints.add_argument("--query", required=True)
    search_endpoints.add_argument("--limit", type=int, default=25)
    search_endpoints.set_defaults(func=command_search_endpoints)

    extract = subparsers.add_parser("extract-dmos")
    extract.add_argument("--dmo-html", required=True)
    extract.set_defaults(func=command_extract_dmos)

    dmo_map = subparsers.add_parser("dmo-connect-map")
    dmo_map.add_argument("--dmo-html", required=True)
    dmo_map.add_argument("--label")
    dmo_map.set_defaults(func=command_dmo_connect_map)

    build = subparsers.add_parser("build-catalogs")
    build.add_argument("--postman", required=True)
    build.add_argument("--dmo-html", required=True)
    build.add_argument("--out-dir", required=True)
    build.set_defaults(func=command_build_catalogs)

    mcp_snippet = subparsers.add_parser("mcp-snippet")
    mcp_snippet.add_argument("--python", required=True)
    mcp_snippet.add_argument("--server", required=True)
    mcp_snippet.add_argument("--target-org", required=True)
    mcp_snippet.add_argument("--server-name", default="datacloud-query")
    mcp_snippet.add_argument("--dataspace")
    mcp_snippet.add_argument("--workload-name", default="data-360-mcp-query-oss")
    mcp_snippet.add_argument("--table-filter", default="ssot\\_%")
    mcp_snippet.add_argument("--api-version", default="v63.0")
    mcp_snippet.set_defaults(func=command_mcp_snippet)

    write_mcp = subparsers.add_parser("write-mcp-config")
    write_mcp.add_argument("--python", required=True)
    write_mcp.add_argument("--server", required=True)
    write_mcp.add_argument("--target-org", required=True)
    write_mcp.add_argument("--out", required=True)
    write_mcp.add_argument("--server-name", default="datacloud-query")
    write_mcp.add_argument("--dataspace")
    write_mcp.add_argument("--workload-name", default="data-360-mcp-query-oss")
    write_mcp.add_argument("--table-filter", default="ssot\\_%")
    write_mcp.add_argument("--api-version", default="v63.0")
    write_mcp.set_defaults(func=command_write_mcp_config)

    snippet = subparsers.add_parser("snippet")
    snippet.add_argument("--kind", required=True)
    snippet.set_defaults(func=command_snippet)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
