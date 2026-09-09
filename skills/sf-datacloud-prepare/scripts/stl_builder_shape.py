#!/usr/bin/env python3
"""Reshape STL bodies into the shapes the graphical builder can open and save.

Static rewriter for a Data 360 batch-transform body, with no org calls. Two
passes, both driven by builder limits the API does not share:
`expand_formula_nodes` gives every formula/typeCast node exactly one field, and
`attach_grain_extractions` gives every aggregate node the upstream
`extractGrains` partner the builder's Aggregate block is made of.

The graphical builder refuses to save a graph whose formula node declares more
than one field:

    Formula - The node Formula defines 4 fields. A node can only define one field.

The API does not enforce this — a multi-field body validates and runs — so the
constraint is on what the builder can render and save, not on execution. A
definition that only ever ships through the API still has to be openable in the
builder, so one field per node is the shape to emit. Field order inside a node
is preserved when it is expanded, so a field that reads one declared above it
still resolves against an upstream node.

`assert_no_aggregate_over_aggregate` and `check_same_group_reads` are pure
guards you can call before deploy; the CLI rewrites files in place.

    python3 stl_builder_shape.py transform.json [more.json ...]
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys


def expand_formula_nodes(nodes: dict) -> dict:
    """Split every multi-field formula/typeCast node into a chain.

    Downstream `sources` are rewired to the last node of each chain, so the
    graph stays connected and node-visible order is unchanged.
    """
    expanded: dict = {}
    tail: dict[str, str] = {}

    for name, node in nodes.items():
        sources = [tail.get(source, source) for source in node.get("sources", [])]
        split_action = node["action"] in {"formula", "typeCast"}
        fields = node["parameters"].get("fields", []) if split_action else []

        if not split_action or len(fields) <= 1:
            rewired = dict(node)
            if "sources" in node:
                rewired["sources"] = sources
            expanded[name] = rewired
            tail[name] = name
            continue

        previous = sources[0]
        for index, field in enumerate(fields):
            output_name = (
                field["name"]
                if node["action"] == "formula"
                else field["newProperties"]["name"]
            )
            prefix = "FML" if node["action"] == "formula" else "CAST"
            part = f"{prefix}_{output_name.upper()}"
            if part in expanded or part in nodes:
                part = f"{name}_{index + 1}"
            parameters = {"fields": [field]}
            if node["action"] == "formula":
                parameters["expressionType"] = "SQL"
            expanded[part] = {
                "action": node["action"],
                "parameters": parameters,
                "sources": [previous],
            }
            previous = part
        tail[name] = previous

    return expanded


def assert_no_aggregate_over_aggregate(nodes: dict) -> None:
    """Reject an aggregate reading an aggregate — it wedges instead of running.

    Chaining a second aggregate (e.g. COUNT onto a grouped aggregate) can
    validate and be accepted for a run, then sit at PENDING with an empty
    `histories[]` and never reach IN_PROGRESS. A second aggregate has to become
    a second transform. Grain nodes are looked through, since
    `attach_grain_extractions` puts one between every aggregate and its source.
    """
    for node_id, node in nodes.items():
        if node["action"] != "aggregate":
            continue
        for source_id in node.get("sources", []):
            upstream = nodes[source_id]
            while upstream["action"] == "extractGrains":
                source_id = (upstream.get("sources") or [None])[0]
                if source_id is None:
                    break
                upstream = nodes[source_id]
            if upstream["action"] == "aggregate":
                raise AssertionError(
                    f"{node_id} directly consumes aggregate node {source_id}"
                )


def attach_grain_extractions(nodes: dict) -> dict:
    """Return `nodes` with an `extractGrains` node upstream of every aggregate.

    The builder does not model an aggregate as one node. Its Aggregate block is
    a container holding two: an `extractGrains` node that carries the grain and
    an `aggregate` node that carries the functions. Opening a body whose
    aggregate has no such partner makes the builder supply the missing node
    itself, without the `grainExtractions` key, and validation then rejects the
    builder's own graph with the required-attribute signal:

        Specify the grainExtractions attribute for the EXTRACT0 node
            at the path parameters -> grainExtractions.

    Emit `grainExtractions: []`. Do not add a DAY (or other) extraction unless
    the aggregate's `groupings` include that derived column. An unused
    extraction is a builder error; grouping by a calendar grain changes the
    product grain. Empty `[]` specifies the attribute and is inert.
    """
    attached: dict = {}

    for name, node in nodes.items():
        sources = node.get("sources") or []
        if node["action"] != "aggregate" or len(sources) != 1:
            attached[name] = node
            continue

        if nodes.get(sources[0], {}).get("action") == "extractGrains":
            attached[name] = node
            continue

        grain = f"GRAIN_{name}"
        attached[grain] = {
            "action": "extractGrains",
            "parameters": {
                "grainExtractions": []
            },
            "sources": [sources[0]],
        }
        attached[name] = dict(node, sources=[grain])

    return attached


def _declared(node: dict) -> list:
    action, params = node["action"], node["parameters"]
    if action == "load":
        return [f["name"] if isinstance(f, dict) else f for f in params.get("fields", [])]
    if action in ("formula", "computeRelative"):
        return [f["name"] for f in params.get("fields", [])]
    if action == "typeCast":
        return [f["newProperties"]["name"] for f in params.get("fields", [])]
    return []


def check_same_group_reads(nodes: dict) -> list:
    """Report formula fields that read a field declared in their own merged group.

    The builder groups consecutive formula nodes into one Transform and evaluates
    that group's fields in parallel, so a field reading another field of the same
    group is reported as referencing something that "doesn't exist yet" and the
    graph cannot be saved. A non-formula node between them ends the group and
    makes the read legal.

    Returns a list of (node, field, referenced_field).
    """
    order, seen = [], set()
    outputs = [k for k, v in nodes.items() if v["action"] == "outputD360"]
    cursor = outputs[0] if outputs else None
    while cursor and cursor not in seen:
        seen.add(cursor)
        order.append(cursor)
        sources = nodes[cursor].get("sources") or []
        cursor = sources[0] if sources else None
    order.reverse()

    group_of, group, index = {}, [], 0
    for name in order:
        if nodes[name]["action"] == "formula":
            group.append(name)
            group_of[name] = index
        elif group:
            group, index = [], index + 1

    declared_in = {}
    for name in order:
        for field in _declared(nodes[name]):
            declared_in[field] = name

    problems = []
    for name in order:
        if nodes[name]["action"] != "formula":
            continue
        for field in nodes[name]["parameters"]["fields"]:
            expression = html.unescape(field["formulaExpression"])
            bare = re.sub(r"'[^']*'", " ", expression)
            tokens = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", bare))
            for ref in sorted((tokens & set(declared_in)) - {field["name"]}):
                owner = declared_in[ref]
                if owner in group_of and group_of[owner] == group_of.get(name):
                    problems.append((name, field["name"], ref))
    return problems


def _split_file(path: str) -> int:
    with open(path) as handle:
        body = json.load(handle)

    nodes = body["definition"]["nodes"]
    before = sum(
        1
        for node in nodes.values()
        if node["action"] == "formula" and len(node["parameters"]["fields"]) > 1
    )
    bare = sum(
        1
        for name, node in nodes.items()
        if node["action"] == "aggregate"
        and not any(
            nodes.get(source, {}).get("action") == "extractGrains"
            for source in node.get("sources") or []
        )
    )
    nodes = expand_formula_nodes(nodes)
    assert_no_aggregate_over_aggregate(nodes)
    body["definition"]["nodes"] = attach_grain_extractions(nodes)
    with open(path, "w") as handle:
        json.dump(body, handle, indent=2)
        handle.write("\n")

    after = len(body["definition"]["nodes"])
    print(
        f"{path}: split {before} multi-field node(s); "
        f"grain-partnered {bare} aggregate(s); {after} nodes total"
    )
    return before


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="transform body JSON file(s) to rewrite in place")
    args = parser.parse_args()
    for path in args.paths:
        _split_file(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
