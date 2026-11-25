"""Read-only, bounded source inspection. Never executes project code."""
from __future__ import annotations
import ast
import hashlib
import json
import os
import re
from pathlib import Path

SKIP_DIRS = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', '.next', '.nuxt', 'dist', 'build', 'target', 'coverage', '.idea', '.tox', '.mypy_cache', '.pytest_cache', '.turbo', 'vendor', 'mercy-output', 'output-example', 'output-galaxy'}
SKIP_FILES = {'.env', '.env.local', '.env.production', '.env.development', 'id_rsa', 'id_ed25519'}
SENSITIVE_SUFFIX = {'.pem', '.key', '.p12', '.pfx', '.sqlite', '.sqlite3', '.db', '.ipynb', '.log'}
CODE_SUFFIX = {'.py', '.js', '.jsx', '.ts', '.tsx', '.go', '.rs', '.java', '.cpp', '.c', '.h', '.hpp', '.php', '.rb', '.dart', '.kt', '.vue', '.svelte'}
TEXT_SUFFIX = {'.py', '.js', '.jsx', '.ts', '.tsx', '.go', '.rs', '.java', '.cpp', '.c', '.h', '.hpp', '.html', '.css', '.sql', '.yaml', '.yml', '.toml', '.json', '.md', '.txt', '.sh', '.vue', '.svelte', '.php', '.rb', '.dart', '.kt'}
DATA_SUFFIX = {'.csv', '.tsv', '.parquet', '.jsonl', '.arrow', '.feather', '.xlsx', '.npy', '.npz'}
CONFIG_NAMES = {'Dockerfile', 'Makefile', 'Procfile', 'requirements.txt', 'Pipfile', 'poetry.lock', 'package-lock.json', 'pnpm-lock.yaml', 'yarn.lock'}
SENSITIVE_LINE = re.compile(r'(?i)(api[_-]?key|client[_-]?secret|password|private[_-]?key|bearer\s+|access[_-]?token|auth[_-]?token|sk-[A-Za-z0-9_-]{8,}|AKIA[A-Z0-9]{10,})')
SIGNALS = {
 'training': r'\bmodel\.fit\s*\(|\btrainer\.train\s*\(|\bloss\.backward\s*\(|\bfit_transform\s*\(',
 'rag': r'\b(retriev\w*|similarity_search|vectorstore|vector_store|Chroma|FAISS|Pinecone|Weaviate|Qdrant)\b',
 'embeddings': r'\b(embeddings?|SentenceTransformer|text-embedding-|embed_query|embed_documents)\b',
 'llm_api': r'\b(OpenAI\s*\(|Anthropic\s*\(|ChatOpenAI|ChatAnthropic|generativeai|generate_content|chat\.completions|responses\.create|litellm)\b',
 'auth': r'\b(nextauth|NextAuth|passport|jwt|JWT|bcrypt|authlib|clerk|supabase\.auth|signIn|verify_token|authentication)\b',
 'database': r'\b(sqlalchemy|prisma|mongoose|psycopg|sqlite3|django\.db|postgresql|mongodb|redis|supabase|create_engine)\b',
 'testing': r'\b(pytest|unittest|vitest|jest|describe\(|test\(|def test_)\b',
 'frontend': r'\b(React|Next\.js|next/|vue|svelte|tailwind|useState|useEffect)\b',
 'backend': r'\b(FastAPI|Flask|Django|express\(|Express|app\.get\(|app\.post\(|router\.get\(|router\.post\(|@app\.get|@app\.post|@router\.)\b',
 'deployment': r'\b(vercel|netlify|Dockerfile|docker-compose|gunicorn|uvicorn|render\.com|railway)\b',
 'chunking': r'\b(RecursiveCharacterTextSplitter|CharacterTextSplitter|chunk_size|chunk_overlap|split_documents|text_splitter)\b',
 'metrics': r'\b(accuracy_score|f1_score|precision_score|recall_score|confusion_matrix|evaluate\(|roc_auc)\b',
}
FRAMEWORKS = {
 'FastAPI': r'\bfastapi\b|\bFastAPI\s*\(', 'Flask': r'\bflask\b|\bFlask\s*\(',
 'Django': r'\bdjango\b', 'Next.js': r'\bNext\.js\b|\b(?:from\s*|require\s*\(\s*|import\s*\(\s*)[\'\"]next(?:/[\w/-]+)?[\'\"]|^\s*import\s+[\'\"]next/',
 'React': r'\breact\b|from [\'\"]react[\'\"]', 'Express': r'\bexpress\b|\bexpress\s*\(',
 'PostgreSQL': r'\bpostgresql\b|\bpsycopg\b', 'MongoDB': r'\bmongodb\b|\bmongoose\b',
 'LangChain': r'\blangchain\b', 'LlamaIndex': r'\bllama_index\b', 'Chroma': r'\bchromadb\b|\bChroma\s*\(',
 'FAISS': r'\bfaiss\b|\bFAISS\b', 'PyTorch': r'\btorch\b|\bpytorch\b',
 'TensorFlow': r'\btensorflow\b', 'SQLite': r'\bsqlite3\b', 'Redis': r'\bredis\b',
 'OpenAI SDK': r'\bopenai\b|\bChatOpenAI\b', 'Anthropic SDK': r'\banthropic\b|\bChatAnthropic\b'
}
ROUTE_RE = re.compile(r'(@(?:app|router|api|blueprint)\.(?:get|post|put|delete|patch|route)\s*\(\s*[\'\"]([^\'\"]+)|(?:app|router)\.(?:get|post|put|delete|patch)\s*\(\s*[\'\"]([^\'\"]+))')
PY_IMPORT_RE = re.compile(r'^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))')
JS_IMPORT_RE = re.compile(r'(?:from\s*|import\s*\(|require\s*\()\s*[\'\"]([^\'\"]+)[\'\"]')
JS_SYMBOL_RE = re.compile(r'\b(?:export\s+)?(?:async\s+)?(?:function|class|interface|type)\s+([A-Za-z_$][\w$]*)')
PY_SYMBOL_RE = re.compile(r'^\s*(?:async\s+)?(?:def|class)\s+([A-Za-z_]\w*)')
ENV_NAME_RE = re.compile(r'(?:os\.getenv|os\.environ\.get|process\.env\.|getenv|import\.meta\.env\.)(?:\s*\(\s*[\'\"])?([A-Z][A-Z0-9_]{2,})')
URL_RE = re.compile(r'https?://[^\s\'\"<>]{3,100}')


def _ignore_name(name: str) -> bool:
    lower = name.lower()
    return (name in SKIP_FILES or lower.startswith('.env') and name != '.env.example'
            or lower.endswith(tuple(SENSITIVE_SUFFIX)) or 'credential' in lower or 'secret' in lower)


def _safe_line(s: str) -> str:
    if SENSITIVE_LINE.search(s):
        return '[redacted: potentially sensitive line]'
    return s.strip()[:160]


def _discover(root: Path, max_files: int):
    """Only regular files inside root. Symlink targets are never opened."""
    n = 0
    for base, dirs, filenames in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith('.'))
        for name in sorted(filenames):
            p = Path(base) / name
            if p.is_symlink() or not p.is_file() or _ignore_name(name):
                continue
            if p.suffix.lower() not in TEXT_SUFFIX | DATA_SUFFIX and name not in CONFIG_NAMES:
                continue
            if name in {'package-lock.json', 'poetry.lock', 'yarn.lock', 'pnpm-lock.yaml'}:
                continue
            n += 1
            if n > max_files:
                return
            yield p


def _local_imports(path: str, imports: list[dict], valid_paths: set[str]) -> list[dict]:
    results = []
    base = Path(path).parent
    for imported in imports:
        item = imported['name']
        line = imported['line']
        if item.startswith('.'):
            # Python relative imports (.module, ..package) and JS ./path, ../path.
            if item.startswith('./') or item.startswith('../'):
                raw = base / item
            else:
                dots = len(item) - len(item.lstrip('.'))
                raw = base
                for _ in range(max(0, dots - 1)):
                    raw = raw.parent
                raw = raw / Path(*item.lstrip('.').split('.'))
        elif item.startswith('@/'):
            raw = Path('src') / item[2:]
        elif '/' in item and not item.startswith('@'):
            continue
        else:
            raw = Path(*item.split('.'))
        candidates = [raw, raw / 'index', Path('src') / raw]
        targets = [str(c) + ext for c in candidates for ext in ('.py', '.ts', '.tsx', '.js', '.jsx')]
        for target in targets:
            norm = os.path.normpath(target).replace('\\', '/')
            if norm in valid_paths and norm != path:
                results.append({'source': path, 'target': norm, 'via': item, 'line': line})
                break
    return results



def _django_routes(tree: ast.AST) -> list[dict]:
    """Extract literal URL patterns through Django imports without importing Django."""
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == 'django.urls':
            names.update(a.asname or a.name for a in node.names if a.name in {'path', 're_path'})
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == 'django.urls':
                    names.update((alias.asname or alias.name) + '.' + suffix for suffix in ('path', 're_path'))
        elif isinstance(node, ast.ImportFrom) and node.module == 'django':
            for alias in node.names:
                if alias.name == 'urls':
                    names.update((alias.asname or alias.name) + '.' + suffix for suffix in ('path', 're_path'))
    routes = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or ast.unparse(node.func) not in names:
            continue
        pattern = node.args[0] if node.args else next((k.value for k in node.keywords if k.arg == 'route'), None)
        if isinstance(pattern, ast.Constant) and isinstance(pattern.value, str):
            routes.append({'path': pattern.value, 'line': node.lineno, 'kind': 'django-pattern'})
    return sorted(routes, key=lambda route: route['line'])[:40]


def scan_project(root: str | Path, max_files: int = 400, max_bytes: int = 1_600_000) -> dict:
    root = Path(root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f'Not a directory: {root}')
    file_paths = list(_discover(root, max_files))
    known = {p.relative_to(root).as_posix() for p in file_paths}
    report = {'project': root.name, 'files': [], 'signals': {},
              'frameworks': {}, 'datasets': [], 'edges': [], 'environment_variables': [],
              'warnings': [], 'summary': {}, 'external_urls': []}
    consumed = 0
    envs = set(); urls = set()
    for p in file_paths:
        rel = p.relative_to(root).as_posix()
        if p.suffix.lower() in DATA_SUFFIX:
            report['datasets'].append({'path': rel, 'reason': 'data-shaped file; usage not confirmed'})
            continue
        size = p.stat().st_size
        if size > 90_000:
            report['warnings'].append(f'Skipped large source file: {rel}')
            continue
        if consumed + size > max_bytes:
            report['warnings'].append('Global read budget exceeded; some files were skipped.')
            break
        consumed += size
        try:
            src = p.read_text(encoding='utf-8', errors='replace')
        except OSError:
            continue
        lines = src.splitlines()
        # Never send comments or unrestricted source bodies; extract only named signals.
        info = {'path': rel, 'sha256': hashlib.sha256(src.encode()).hexdigest(), 'language': (p.suffix.lower().lstrip('.') or p.name), 'lines': len(lines),
                'imports': [], 'import_locations': [], 'symbols': [], 'routes': []}
        if p.suffix.lower() == '.py':
            try:
                tree = ast.parse(src)
                info['routes'] = _django_routes(tree)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for a in node.names:
                            info['imports'].append(a.name)
                            info['import_locations'].append({'name':a.name,'line':node.lineno})
                    elif isinstance(node, ast.ImportFrom):
                        prefix = '.' * node.level
                        name = prefix + (node.module or '')
                        info['imports'].append(name)
                        info['import_locations'].append({'name':name,'line':node.lineno})
                    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        if len(info['symbols']) < 32:
                            info['symbols'].append({'name': node.name, 'line': node.lineno})
            except SyntaxError:
                report['warnings'].append(f'Python parse failed: {rel}; using text patterns.')
        else:
            info['import_locations'] = [{'name':m.group(1),'line':src.count('\n',0,m.start())+1} for m in list(JS_IMPORT_RE.finditer(src))[:32]] if p.suffix.lower() in CODE_SUFFIX else []
            info['imports'] = [e['name'] for e in info['import_locations']]
            info['symbols'] = [{'name': m.group(1), 'line': src.count('\n', 0, m.start()) + 1} for m in list(JS_SYMBOL_RE.finditer(src))[:32]] if p.suffix.lower() in CODE_SUFFIX else []
        for line_no, line in enumerate(lines, 1):
            if (not line.strip() or line.lstrip().startswith(('#', '//', '*', '<!--')) or
                 line_no > 8000):
                continue
            # Documentation and dependency manifests describe intent, not working code.
            for tag, pattern in (SIGNALS.items() if p.suffix.lower() in CODE_SUFFIX else []):
                if re.search(pattern, line, re.IGNORECASE):
                    hits = report['signals'].setdefault(tag, [])
                    if len(hits) < 16:
                        hits.append({'path': rel, 'line': line_no, 'excerpt': _safe_line(line)})
            if p.suffix.lower() in CODE_SUFFIX:
                for fw, pattern in FRAMEWORKS.items():
                    if re.search(pattern, line, re.IGNORECASE):
                        hits = report['frameworks'].setdefault(fw, [])
                        if len(hits) < 5:
                            hits.append({'path': rel, 'line': line_no, 'excerpt': _safe_line(line)})
                m = ROUTE_RE.search(line)
                if m and len(info['routes']) < 40:
                    info['routes'].append({'path': m.group(2) or m.group(3), 'line': line_no})
                for name in ENV_NAME_RE.findall(line):
                    envs.add(name)
                if any(k in line.lower() for k in ('load_dataset(', 'read_csv(', 'read_parquet(', 'dataset_path')):
                    hits = report['signals'].setdefault('dataset_loader', [])
                    if len(hits) < 16:
                        hits.append({'path': rel, 'line': line_no, 'excerpt': _safe_line(line)})
                for found in URL_RE.findall(line):
                    if len(urls) < 20 and 'localhost' not in found and not SENSITIVE_LINE.search(found):
                        urls.add(found.rstrip('),;'))
        report['files'].append(info)
    for f in report['files']:
        report['edges'] += _local_imports(f['path'], f['import_locations'], known)
    report['environment_variables'] = sorted(envs)
    report['external_urls'] = sorted(urls)[:20]
    report['summary'] = {
        'read_files': len(report['files']), 'data_files': len(report['datasets']),
        'routes_found': sum(len(f['routes']) for f in report['files']),
        'module_links': len(report['edges']), 'tests_found': sum(
            1 for f in report['files'] if 'test' in Path(f['path']).name.lower()
            or '/tests/' in '/' + f['path']),
        'bytes_read': consumed, 'source_files_considered': len(file_paths)
    }
    if len(file_paths) >= max_files:
        report['warnings'].append('Reached maximum file count; this audit is not exhaustive.')
    if not report['signals'].get('training'):
        report['warnings'].append('No direct training-loop evidence found; do not claim this model was trained here.')
    if not report['datasets'] and not report['signals'].get('dataset_loader'):
        report['warnings'].append('No dataset files or loaders located in the inspected source.')
    return report
