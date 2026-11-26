"""Reviewed study aids. Citations validate location, never semantic truth."""
from __future__ import annotations

import re
from urllib.parse import urlsplit

LOGOS = {'python', 'fastapi', 'html5', 'javascript', 'huggingface', 'nvidia', 'ffmpeg', 'sqlite', 'react'}


def validate_presentation(question: dict, known: dict[str, int]) -> None:
    def text(value, name, words):
        if not isinstance(value, str) or not value.strip() or len(value.split()) > words:
            raise ValueError(f'{name} needs nonempty text of at most {words} words.')

    def refs(value):
        if not isinstance(value, list) or not value:
            raise ValueError('Study aids need source evidence.')
        for ref in value:
            if (not isinstance(ref, dict) or not isinstance(ref.get('path'), str)
                    or ref['path'] not in known or type(ref.get('line')) is not int
                    or not 1 <= ref['line'] <= known[ref['path']]):
                raise ValueError('Study aid evidence is outside the saved scan.')

    def records(value, name, limit):
        if not isinstance(value, list) or len(value) > limit or not all(isinstance(x, dict) for x in value):
            raise ValueError(f'{name} must be an array of at most {limit} records.')
        return value

    def identifier(value):
        if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', value):
            raise ValueError('Study aid IDs need letters, digits, underscores or hyphens.')

    def resources(value):
        for resource in records(value, 'resources', 6):
            text(resource.get('label'), 'Resource label', 8)
            url = resource.get('url')
            if not isinstance(url, str) or len(url) > 2048 or re.search(r'[\s\\<>"\x00-\x1f]', url):
                raise ValueError('Resources need a safe HTTPS URL.')
            parsed = urlsplit(url)
            if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
                raise ValueError('Resources need a safe HTTPS URL.')

    resources(question.get('resources', []))
    if 'overview' in question and type(question['overview']) is not bool:
        raise ValueError('overview must be a boolean.')
    for item in records(question.get('connections', []), 'connections', 30):
        identifier(item.get('source')); identifier(item.get('target'))
        text(item.get('label'), 'Connection label', 6)
        refs(item.get('evidence'))
    for key, maximum in [('viva_question', 14), ('viva_answer', 45)]:
        if key in question:
            text(question[key], key, maximum)
    for item in records(question.get('components', []), 'components', 12):
        identifier(item.get('id'))
        text(item.get('name'), 'Component name', 6)
        text(item.get('description'), 'Component description', 25)
        paths = item.get('files')
        if not isinstance(paths, list) or not paths or any(not isinstance(p, str) or p not in known for p in paths):
            raise ValueError('Components need indexed source files.')
        refs(item.get('evidence'))
    components = question.get('components', [])
    if len({c['id'] for c in components}) != len(components):
        raise ValueError('Component IDs must be unique.')
    for item in records(question.get('directories', []), 'directories', 60):
        path = item.get('path')
        if (not isinstance(path, str) or not path or path.startswith('/') or '..' in path.split('/')
                or not any(p.startswith(path.rstrip('/') + '/') for p in known)):
            raise ValueError('Directory must contain indexed files.')
        text(item.get('description'), 'Directory description', 25)
        refs(item.get('evidence'))
    for item in records(question.get('file_notes', []), 'file_notes', 400):
        if not isinstance(item.get('path'), str) or item['path'] not in known:
            raise ValueError('File explanations need an indexed source path.')
        text(item.get('description'), 'File explanation', 45)
        refs(item.get('evidence'))
    for item in records(question.get('stack', []), 'stack', 20):
        identifier(item.get('id'))
        if not isinstance(item.get('kind'), str) or item['kind'] not in {'frontend', 'backend', 'model', 'storage', 'tool'}:
            raise ValueError('Stack entries need a valid kind.')
        text(item.get('name'), 'Technology name', 10)
        text(item.get('description'), 'Technology description', 45)
        if item.get('logo') is not None and (not isinstance(item['logo'], str) or item['logo'] not in LOGOS):
            raise ValueError('Use a bundled technology logo.')
        if 'origin' in item:
            text(item['origin'], 'Technology origin', 35)
        paths = item.get('paths')
        if not isinstance(paths, list) or not paths:
            raise ValueError('Technology entries need indexed files or folders.')
        for path in paths:
            if (not isinstance(path, str) or not path or path.startswith('/') or '..' in path.split('/')
                    or not (path in known or any(p.startswith(path.rstrip('/') + '/') for p in known))):
                raise ValueError('Technology location is outside the saved scan.')
        refs(item.get('evidence'))
        resources(item.get('resources', []))
    for item in records(question.get('demonstration', []), 'demonstration', 10):
        text(item.get('action'), 'Demo action', 20)
        text(item.get('expected'), 'Demo expectation', 30)
        refs(item.get('evidence'))
    if 'flow' not in question:
        return
    flow = question['flow']
    if not isinstance(flow, dict):
        raise ValueError('flow needs nodes and edges.')
    nodes = records(flow.get('nodes'), 'flow nodes', 20)
    edges = records(flow.get('edges'), 'flow edges', 30)
    ids = set()
    kinds = {}
    for node in nodes:
        identifier(node.get('id'))
        if node['id'] in ids or node.get('kind') not in {'start', 'action', 'decision', 'end'}:
            raise ValueError('Flow nodes need unique IDs and a valid kind.')
        ids.add(node['id']); kinds[node['id']] = node['kind']
        text(node.get('label'), 'Flow label', 12)
        refs(node.get('evidence'))
    if not nodes or not any(k == 'start' for k in kinds.values()) or not any(k == 'end' for k in kinds.values()):
        raise ValueError('A flow needs a start and an end.')
    pairs = set()
    for edge in edges:
        if (not isinstance(edge.get('source'), str) or not isinstance(edge.get('target'), str)
                or edge['source'] not in ids or edge['target'] not in ids):
            raise ValueError('Flow edge refers to an unknown node.')
        pair = (edge['source'], edge['target'])
        if pair in pairs:
            raise ValueError('Duplicate flow edge.')
        pairs.add(pair)
        if 'label' in edge:
            text(edge['label'], 'Branch label', 6)
        if kinds[edge['source']] == 'decision' and not edge.get('label'):
            raise ValueError('Decision branches need labels.')
        refs(edge.get('evidence'))
    reachable = {n for n in ids if kinds[n] == 'start'}
    for _ in nodes:
        reachable.update(e['target'] for e in edges if e['source'] in reachable)
    if reachable != ids:
        raise ValueError('Every flow node must be reachable from a start.')
    for node in nodes:
        outgoing = [e for e in edges if e['source'] == node['id']]
        if node['kind'] == 'end' and outgoing:
            raise ValueError('End nodes cannot have outgoing edges.')
        if node['kind'] != 'end' and not outgoing:
            raise ValueError('Only end nodes may finish a flow.')
        if node['kind'] == 'decision' and (len(outgoing) < 2 or len({e['label'] for e in outgoing}) != len(outgoing)):
            raise ValueError('Decisions need at least two differently labelled branches.')
    finishing = {n for n in ids if kinds[n] == 'end'}
    for _ in nodes:
        finishing.update(e['source'] for e in edges if e['target'] in finishing)
    if finishing != ids:
        raise ValueError('Every flow node needs a path to an end.')


def study_aids(report: dict, questions: list[dict], clusters: list[dict]) -> dict:
    """Keep reviewed components; aggregate only actual resolved import edges."""
    components = [c for q in questions for c in q.get('components', [])]
    if not components:
        components = [{'id':c['id'], 'name':c['name'], 'description':'Suggested group from file names and types.',
                       'files':c['files'], 'evidence':[], 'heuristic':True} for c in clusters]
    if len(components) > 12:
        raise ValueError('Use at most 12 components across the report.')
    ids = [c['id'] for c in components]
    if len(set(ids)) != len(ids):
        raise ValueError('Component IDs must be unique across the report.')
    membership = {}
    for c in components:
        for path in c['files']:
            if path in membership:
                raise ValueError('A source file may belong to only one component.')
            membership[path] = c['id']
    connections = {}
    for edge in report['edges']:
        a, b = membership.get(edge['source']), membership.get(edge['target'])
        if a and b and a != b:
            connections.setdefault((a,b), []).append(edge)
    reviewed = [item for q in questions for item in q.get('connections', [])]
    pairs = set()
    for edge in reviewed:
        pair = (edge['source'], edge['target'])
        if any(node not in ids for node in pair) or pair[0] == pair[1] or pair in pairs:
            raise ValueError('Connections need distinct known components and unique directed pairs.')
        pairs.add(pair)
    if len(reviewed) > 30:
        raise ValueError('Use at most 30 reviewed connections across the report.')
    stack = [item for q in questions for item in q.get('stack', [])]
    if len({item['id'] for item in stack}) != len(stack):
        raise ValueError('Technology IDs must be unique across the report.')
    notes = [item for q in questions for item in q.get('file_notes', [])]
    if len({item['path'] for item in notes}) != len(notes):
        raise ValueError('Use one explanation per source file.')
    return {'components':components, 'connections':reviewed, 'stack':stack, 'file_notes':notes,
            'component_edges':[{'source':a, 'target':b, 'imports':edges} for (a,b),edges in connections.items()],
            'flows':[{'id':q['id'], 'name':q.get('viva_question', q['question']), **q['flow']}
                     for q in questions if q.get('flow')],
            'demonstrations':[{'id':q['id'], 'name':q.get('viva_question', q['question']), 'steps':q['demonstration']}
                              for q in questions if q.get('demonstration')],
            'directories':[d for q in questions for d in q.get('directories', [])]}
