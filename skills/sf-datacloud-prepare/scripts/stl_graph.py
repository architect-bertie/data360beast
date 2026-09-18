"""Shared, org-free graph checks. Unknown operations are never assumed read-only."""
from __future__ import annotations

READ_ACTIONS = {
    'load', 'formula', 'typeCast', 'aggregate', 'join', 'filter', 'sqlFilter',
    'extractGrains', 'deduplicate', 'computeRelative', 'append', 'appendV2',
}


def validate_graph(nodes: dict) -> None:
    if not isinstance(nodes, dict) or not nodes:
        raise ValueError('expected a nonempty node map')
    done, visiting = set(), set()

    def visit(name):
        if name in visiting:
            raise ValueError(f'cycle at node {name}')
        if name in done:
            return
        if name not in nodes:
            raise ValueError(f'unknown source node {name}')
        visiting.add(name)
        sources = nodes[name].get('sources') or []
        if not isinstance(sources, list) or not all(isinstance(s, str) for s in sources):
            raise ValueError(f'invalid sources on {name}')
        for source in sources:
            visit(source)
        visiting.remove(name)
        done.add(name)

    for name in nodes:
        visit(name)


def allocate_name(preferred: str, occupied: set[str]) -> str:
    name, suffix = preferred, 1
    while name in occupied:
        name = f'{preferred}_{suffix}'
        suffix += 1
    occupied.add(name)
    return name


def validate_scratch(full: dict, scratch: str) -> None:
    if not scratch or not isinstance(scratch, str):
        raise ValueError('scratch DLO is required')
    nodes = full['definition']['nodes']
    validate_graph(nodes)
    for node in nodes.values():
        action = node.get('action')
        if action not in READ_ACTIONS | {'outputD360'}:
            raise ValueError(f'unsupported operation in probe source: {action}')
        if action == 'outputD360' and node['parameters'].get('name') == scratch:
            raise ValueError('scratch DLO must differ from every original output')


def validate_probe(body: dict, scratch: str) -> None:
    nodes = body['definition']['nodes']
    validate_graph(nodes)
    outputs = []
    for node in nodes.values():
        action = node.get('action')
        if action == 'outputD360':
            outputs.append(node)
            if node['parameters'].get('name') != scratch:
                raise ValueError('probe contains a write outside the scratch DLO')
            if node['parameters'].get('type', 'dataLakeObject') != 'dataLakeObject':
                raise ValueError('probe output must be a scratch DLO')
        elif action not in READ_ACTIONS:
            raise ValueError(f'unsupported operation in probe: {action}')
    if len(outputs) != 1:
        raise ValueError('probe must have exactly one scratch output')
