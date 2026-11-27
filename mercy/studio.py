"""Export a standalone, interactive, offline HTML atlas from grounded scan metadata.

The output never executes repository code. Redacted source is explicit opt-in.
Reviewed component connections remain distinct from resolved imports.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from colorsys import rgb_to_hls
from importlib import resources
from pathlib import Path
import json
import base64
import hashlib
import re

from . import __version__
from .agent import _source, _numbered_excerpt, _current_report, review_progress
from .scanner import _ignore_name, CODE_SUFFIX
from .presentation import study_aids

ROLE_LABELS = {
    'frontend': 'Interface',
    'backend': 'Backend',
    'ai': 'Intelligence',
    'data': 'Data',
    'infra': 'Infrastructure',
}
ROLE_COLORS = {
    'frontend': '#40dbe6',
    'backend': '#7e99ff',
    'ai': '#c999ff',
    'data': '#5addac',
    'infra': '#f3ad6a',
}
GLOSSARY = [
    {'term': 'Frontend', 'simple': 'The screens and buttons people see.', 'example': 'Like the counter at a café.'},
    {'term': 'Backend', 'simple': 'Code that receives requests and decides what happens.', 'example': 'Like the kitchen preparing an order.'},
    {'term': 'API', 'simple': 'A doorway where one program asks another for help.', 'example': 'The cashier passing your order to the kitchen.'},
    {'term': 'Route', 'simple': 'An address that receives one kind of request.', 'example': '/login is like a marked service window.'},
    {'term': 'Database', 'simple': 'A structured place to store and find information.', 'example': 'An organized notebook with many labelled pages.'},
    {'term': 'AI inference', 'simple': 'Using a model that already knows how to predict or answer.', 'example': 'Taking an exam after studying.'},
    {'term': 'Model training', 'simple': 'Teaching a model by updating it with examples.', 'example': 'Studying many practice questions before the exam.'},
    {'term': 'Dataset', 'simple': 'A collection of examples or records used for learning or lookup.', 'example': 'A workbook full of examples.'},
    {'term': 'Embedding', 'simple': 'A number-based representation of meaning.', 'example': 'Giving similar sentences nearby map coordinates.'},
    {'term': 'RAG', 'simple': 'Find useful notes first, then ask an AI to answer with them.', 'example': 'An open-book exam instead of guessing.'},
    {'term': 'Import', 'simple': 'One file names code from another file that it may use.', 'example': 'Borrowing a tool from a neighbour; not proof it was used.'},
    {'term': 'Authentication', 'simple': 'Checking who someone is.', 'example': 'Showing your ID to enter a building.'},
    {'term': 'Authorization', 'simple': 'Checking what someone is allowed to do.', 'example': 'A visitor can enter the lobby, not the server room.'},
    {'term': 'Dependency graph', 'simple': 'A map of files referencing other files.', 'example': 'A list of which rooms have doors to other rooms.'},
]


def _role(info: dict, report: dict) -> str:
    """Heuristic grouping, explicitly not proof of runtime boundaries."""
    path = info['path'].lower()
    name = Path(path).name
    suffix = Path(path).suffix
    if suffix in {'.html', '.css', '.scss', '.sass', '.vue', '.svelte', '.jsx', '.tsx'} or any(part in path.split('/') for part in ('pages','components','ui','frontend','client','views','screens','public')):
        return 'frontend'
    if suffix in {'.sql', '.prisma'} or any(part in path.split('/') for part in ('migrations','datasets','data','db','storage','database','models_db')):
        return 'data'
    if any(word in name for word in ('rag','embed','retriev','inference','train','predict','llm','ai_agent','model_api','pipeline')) or any(part in path.split('/') for part in ('ml','ai','intelligence','agents','pipelines','vectorstore')):
        return 'ai'
    if suffix in {'.yaml','.yml','.toml','.md','.json','.sh'} or name in {'dockerfile','makefile','procfile','requirements.txt'} or any(part in path.split('/') for part in ('infra','deploy','.github','config','docs')):
        return 'infra'
    for label in ('rag','embeddings','training','llm_api','chunking'):
        if any(x['path'] == info['path'] for x in report.get('signals', {}).get(label, [])):
            return 'ai'
    return 'backend'


def _color_rgb(c: str) -> tuple[float,float,float]:
    c = c.lstrip('#')
    if len(c) == 3:
        c = ''.join(n*2 for n in c)
    return tuple(int(c[i:i+2],16)/255 for i in (0,2,4))


def _contrast(a: str, b: str) -> float:
    def lum(s: str):
        rgb = _color_rgb(s)
        parts = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in rgb]
        return .2126*parts[0]+.7152*parts[1]+.0722*parts[2]
    hi, lo = sorted((lum(a),lum(b)),reverse=True)
    return (hi+.05)/(lo+.05)


def extract_theme(root: str | Path, report: dict) -> dict:
    """Sample valid color hints; allow explicit, strictly whitelisted project theme overrides.

    This is a *design-token bridge*, not an automatic UI clone. Never import user styles.
    """
    root = Path(root).resolve()
    counts: Counter[str] = Counter()
    candidates = [f['path'] for f in report['files'] if Path(f['path']).suffix.lower() in {'.css', '.scss', '.sass', '.html', '.vue', '.svelte'}]
    source = []
    for relative in candidates[:24]:
        if _ignore_name(Path(relative).name):
            continue
        try:
            raw = _source(root, relative)[:45_000]
        except (OSError, ValueError):
            continue
        source.append(relative)
        for value in re.findall(r'(?<![\w-])#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})(?![A-Fa-f0-9])', raw):
            color = '#'+value.lower()
            if len(color) == 4:
                color = '#'+''.join(x*2 for x in color[1:])
            h,l,s = rgb_to_hls(*_color_rgb(color))
            if 0.23 < l < 0.83 and s > 0.22:
                counts[color] += 1
    palette = [color for color, _ in counts.most_common(12)]
    first = palette[0] if palette else '#40dbe6'
    second = next((c for c in palette[1:] if abs(rgb_to_hls(*_color_rgb(c))[0] - rgb_to_hls(*_color_rgb(first))[0]) > 0.12), '#ac91ff')
    theme = {'primary': first, 'secondary': second,
             'source': source[:5], 'source_type': 'project-styles' if palette else 'Mercy-fallback',
             'note': ('Project colors were sampled from local style files; layout remains Mercy Studio.' if palette
                      else 'No safe project palette could be identified; Mercy uses its own contrast-tested colors.')}
    # Optional project-owned override, validated as data, never arbitrary CSS.
    # This file may be written by the user or (only with permission) a coding agent.
    config = root / 'mercy-theme.json'
    try:
        obj = None
        if config.is_file() and not config.is_symlink() and config.stat().st_size <= 4096:
            obj = json.loads(config.read_text(encoding='utf-8'))
    except (ValueError, OSError, UnicodeError):
        obj = None
    if isinstance(obj,dict):
        valid = re.compile(r'^#[A-Fa-f0-9]{6}$')
        for key in ('primary','secondary','background','panel','text','muted'):
            value = obj.get(key)
            if isinstance(value,str) and valid.fullmatch(value):
                theme[key] = value.lower()
        if isinstance(obj.get('radius'),int) and not isinstance(obj.get('radius'),bool) and 5 <= obj['radius'] <= 28:
            theme['radius'] = obj['radius']
        if obj.get('font') in ('system','serif','mono'):
            theme['font'] = obj['font']
        # Check enough contrast against the supplied page colors, not a guarantee
        # that *every* UI state satisfies WCAG.
        if 'background' in theme and 'text' in theme and _contrast(theme['background'],theme['text']) < 4.5:
            del theme['background']
            del theme['text']
            theme['note'] += ' Rejected low-contrast background/text override.'
        theme['source_type'] = 'project-theme-file'
        theme['source'] = ['mercy-theme.json']
        theme['note'] += ' Explicit user theme tokens were validated, but layout remains Mercy Studio.'
    return theme

def build_atlas(report: dict, questions: list[dict], root: str | Path | None = None) -> dict:
    files = []
    if root is None:
        theme = report.get('studio_theme') or {'primary':'#40dbe6','secondary':'#ac91ff', 'source':[], 'source_type':'Mercy-fallback', 'note':'No project style files inspected.'}
    else:
        theme = extract_theme(root, report)
    for f in report['files']:
        role = _role(f, report)
        files.append({'path':f['path'], 'role':role, 'language':f['language'], 'lines':f['lines'],
                      'routes':f['routes'], 'symbols':f['symbols'],
                      'imports':f['imports'], 'kind':'file'})
    for d in report['datasets']:
        files.append({'path': d['path'], 'role':'data', 'language':Path(d['path']).suffix.lstrip('.'),
                      'lines':0, 'routes':[], 'symbols':[], 'imports':[], 'kind':'data-candidate'})
    members: dict[str,list] = defaultdict(list)
    for f in files:
        members[f['role']].append(f['path'])
    clusters = [{'id':r,'name':ROLE_LABELS[r], 'color':ROLE_COLORS[r], 'files':members[r],
                 'count':len(members[r]), 'proof':'heuristic grouping from names and file types'}
                for r in ROLE_LABELS if members.get(r)]
    role_by_path = {f['path']:f['role'] for f in files}
    edges = [{**e, 'kind':'import', 'certainty':'static-reference',
              'source_role':role_by_path.get(e['source'], 'backend'),
              'target_role':role_by_path.get(e['target'], 'backend')} for e in report['edges']
             if e['source'] in role_by_path and e['target'] in role_by_path]
    crossings = Counter((e['source_role'], e['target_role']) for e in edges if e['source_role']!=e['target_role'])
    routes = [{**r, 'file':f['path']} for f in report['files'] for r in f['routes']]
    signals = {k:[{'path':p['path'],'line':p['line']} for p in vals] for k, vals in report['signals'].items()}
    concept_status = {}
    for term, tags in {'RAG':['rag'], 'Embedding':['embeddings'], 'Model training':['training'],
                       'Dataset':['dataset_loader'], 'Authentication':['auth'], 'Database':['database'],
                       'Backend':['backend'], 'Frontend':['frontend'], 'AI inference':['llm_api']}.items():
        concept_status[term] = any(report['signals'].get(t) for t in tags)
    return {
        'format_version':3,
        'generator_version':__version__,
        **study_aids(report, questions, clusters),
        'project':report['project'], 'summary':report['summary'], 'warnings':report['warnings'],
        'theme':theme, 'clusters':clusters, 'files':files, 'edges':edges,
        'crossings':[{'a':a,'b':b,'count':v} for (a,b),v in crossings.items()],
        'routes':routes, 'frameworks':sorted(report['frameworks'].keys()),
        'framework_evidence':{name:[{'path':hit['path'], 'line':hit['line']} for hit in hits]
                              for name,hits in report['frameworks'].items()},
        'questions':questions, 'glossary':[{**c,'detected':concept_status.get(c['term'],False)} for c in GLOSSARY],
        'signals':signals, 'datasets':report['datasets'],
        'disclaimers':[
            'Architecture uses cited source relationships when reviewed; otherwise arrows show resolved imports. Neither proves a runtime call.',
            'File roles are heuristics derived from file type/name. Real architecture may differ.',
            'Question evidence is a code clue, not proof that a feature is working in production.',
            'No repository source code is embedded. This HTML contains paths, module names, and scan metadata; review before sharing.',
        ],
    }


def export_studio(report: dict, questions: list[dict], output: str | Path, root: str | Path | None = None, *, workflow=None, include_source=False) -> dict:
    atlas = build_atlas(report, questions, root)
    if include_source:
        if root is None:
            raise ValueError('Embedding source needs an explicit project directory.')
        _current_report(report, root)
        source_root = Path(root).expanduser().resolve()
        snapshots, budget = {}, 2_000_000
        for file in report['files']:
            if (_ignore_name(Path(file['path']).name)
                    or Path(file['path']).suffix.lower() not in CODE_SUFFIX | {'.html', '.css', '.scss', '.sql', '.sh'}):
                continue
            raw = _source(source_root, file['path'])
            if hashlib.sha256(raw.encode()).hexdigest() != file.get('sha256'):
                raise ValueError('Source changed since scanning: '+file['path'])
            budget -= len(raw.encode())
            if budget < 0:
                raise ValueError('Source preview exceeds the 2 MB read budget; omit --include-source.')
            lines = raw.splitlines()
            snapshots[file['path']] = _numbered_excerpt(lines, 1, len(lines))
        atlas['source_previews'] = snapshots
        atlas['disclaimers'][-1] = 'This report includes redacted, line-numbered source previews (lines capped at 160 characters). Review it before sharing; redaction is not a confidentiality guarantee.'
    if workflow is not None:
        atlas['review'] = review_progress({'questions':questions,'workflow':workflow})
    payload = json.dumps(atlas, ensure_ascii=False, separators=(',',':'))
    # The browser's HTML parser sees script closing tags even in application/json.
    # Escape dangerous delimiters and Unicode JS line separators; everything is inert JSON.
    payload = (payload.replace('&',r'\u0026').replace('<',r'\u003c')
               .replace('>',r'\u003e').replace('\u2028',r'\u2028').replace('\u2029',r'\u2029'))
    template = resources.files('mercy').joinpath('assets', 'studio.html').read_text(encoding='utf-8')
    if '/* MERCY_ATLAS_PAYLOAD */' not in template:
        raise RuntimeError('HTML template missing data marker.')
    for marker, filename in [('MERCY_NOTEBOOK_FONT', 'notebook.ttf'), ('MERCY_MASCOT', 'teacher.webp')]:
        encoded = base64.b64encode(resources.files('mercy').joinpath('assets', filename).read_bytes()).decode('ascii')
        template = template.replace('/* '+marker+' */', encoded)
    logos = resources.files('mercy').joinpath('assets', 'technology-logos.json').read_text(encoding='utf-8').strip()
    template = template.replace('/* MERCY_TECH_LOGOS */', logos)
    result = template.replace('/* MERCY_ATLAS_PAYLOAD */', payload)
    Path(output).write_text(result, encoding='utf-8')
    return atlas
