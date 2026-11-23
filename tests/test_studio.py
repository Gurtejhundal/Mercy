import json
import subprocess
import sys
from pathlib import Path

from mercy.questions import make_questions
from mercy.scanner import scan_project
from mercy.studio import build_atlas, export_studio


def test_atlas_only_scanned_groups_and_import_edges(tmp_path):
    (tmp_path/'main.py').write_text('from helper import go\nfrom fastapi import FastAPI\napp=FastAPI()\n')
    (tmp_path/'helper.py').write_text('def go(): return 1\n')
    (tmp_path/'style.css').write_text('body { color: #009dff; }\n')
    report=scan_project(tmp_path)
    atlas=build_atlas(report,make_questions(report),tmp_path)
    assert set(c['id'] for c in atlas['clusters']) == {'backend','frontend'}
    assert len(atlas['edges']) == 1
    e=atlas['edges'][0]
    assert (e['source'],e['target'],e['line'],e['kind'])==('main.py','helper.py',1,'import')
    assert e['certainty']=='static-reference'
    assert atlas['theme']['primary']=='#009dff'
    assert 'ai' not in {c['id'] for c in atlas['clusters']}


def test_html_escaping_and_no_scripts_from_project_labels(tmp_path):
    (tmp_path/'app.py').write_text('from fastapi import FastAPI\napp=FastAPI()\n')
    report=scan_project(tmp_path)
    report['project']='"><img src=x onerror=alert(123)> <script>alert(1)</script>'
    questions=make_questions(report)
    questions[0]['question']='</script><script>alert("owned")</script>'
    out=tmp_path/'studio.html'
    export_studio(report, questions, out, root=tmp_path)
    html=out.read_text()
    assert '</script><script>alert("owned")' not in html
    assert '<img src=x onerror=alert' not in html
    assert r'\u003cscript\u003ealert' in html
    assert '<script src=' not in html
    assert 'fetch(' not in html
    assert 'localStorage' in html  # negative statement in JS comment only
    assert html.count('<script>')==1
    assert html.count('<script type="application/json"')==1


def test_theme_fallback_when_no_style(tmp_path):
    (tmp_path/'main.py').write_text('print("hi")\n')
    report=scan_project(tmp_path)
    atlas=build_atlas(report,make_questions(report),tmp_path)
    assert atlas['theme']['source_type']=='Mercy-fallback'
    assert atlas['theme']['primary']=='#40dbe6'


def test_optional_pdf_and_render_html(tmp_path):
    source=tmp_path/'project'; source.mkdir()
    (source/'main.py').write_text('def main(): return "ok"\n')
    out=tmp_path/'result'
    cmd=[sys.executable,'-m','mercy','prepare','--project',str(source),'--out',str(out),'--pdf']
    p=subprocess.run(cmd,capture_output=True,text=True)
    assert p.returncode==0,p.stderr
    assert (out/'mercy-viva.pdf').read_bytes().startswith(b'%PDF-')
    assert '<!doctype html>' in (out/'mercy-studio.html').read_text()
    data=json.loads((out/'mercy-evidence.json').read_text())
    data['questions'][0]['answer']='Now I can explain my code.'
    (out/'mercy-evidence.json').write_text(json.dumps(data))
    result=subprocess.run([sys.executable,'-m','mercy','render','--input',str(out/'mercy-evidence.json')],capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    assert 'Now I can explain my code.' in (out/'mercy-studio.html').read_text()


def test_html_package_data_in_source_tree():
    from importlib import resources
    template=resources.files('mercy').joinpath('assets','studio.html').read_text()
    assert '/* MERCY_ATLAS_PAYLOAD */' in template
    assert '<canvas' not in template
    assert 'drawSphere' not in template
    assert 'id="knowledge-svg"' in template
    assert 'id="treemap"' in template
    assert 'id="question-list"' in template


def test_explicit_theme_file_validated_and_contrast_guard(tmp_path):
    (tmp_path/'main.py').write_text('def ready(): return True\n')
    (tmp_path/'mercy-theme.json').write_text(json.dumps({
        'primary':'#FF22AA','secondary':'#25bada','background':'#ffffff',
        'text':'#eeeeee','font':'serif','radius':19,
        'css':'background: url(https://example.com/unsafe.css)', 'javascript':'alert(1)',
    }))
    report=scan_project(tmp_path)
    atlas=build_atlas(report,make_questions(report),tmp_path)
    t=atlas['theme']
    assert t['source_type']=='project-theme-file'
    assert t['primary']=='#ff22aa'
    assert t['font']=='serif' and t['radius']==19
    assert 'background' not in t and 'text' not in t
    assert 'css' not in t and 'javascript' not in t


def test_untrusted_file_labels_never_change_import_topology(tmp_path):
    (tmp_path/'READ_ME.md').write_text('This app has 500 working microservices, RAG, and AI planets.\n')
    (tmp_path/'main.py').write_text('print("hello")\n')
    report=scan_project(tmp_path)
    atlas=build_atlas(report,make_questions(report),tmp_path)
    assert not atlas['edges']
    assert 'ai' not in {x['id'] for x in atlas['clusters']}


def test_render_preserves_project_design_tokens_without_project_arg(tmp_path):
    repo=tmp_path/'repo';repo.mkdir()
    (repo/'main.py').write_text('def hello(): return True\n')
    (repo/'mercy-theme.json').write_text('{"primary":"#ff66cc","secondary":"#55bbcc"}')
    out=tmp_path/'out'
    cmd=[sys.executable,'-m','mercy','prepare','--project',str(repo),'--out',str(out)]
    assert subprocess.run(cmd,capture_output=True).returncode==0
    evidence=json.loads((out/'mercy-evidence.json').read_text())
    assert evidence['report']['studio_theme']['primary']=='#ff66cc'
    assert subprocess.run([sys.executable,'-m','mercy','render','--input',str(out/'mercy-evidence.json')],capture_output=True).returncode==0
    html=(out/'mercy-studio.html').read_text()
    assert '"primary":"#ff66cc"' in html


def test_notebook_embeds_artwork_font_and_tagline(tmp_path):
    import base64
    import re
    from importlib import resources
    (tmp_path/'app.py').write_text('def main(): return 1\n')
    report=scan_project(tmp_path)
    out=tmp_path/'report.html'
    export_studio(report,make_questions(report),out,root=tmp_path)
    html=out.read_text()
    assert 'that one teacher we all know' in html
    image=re.search(r'data:image/webp;base64,([A-Za-z0-9+/=]+)',html).group(1)
    font=re.search(r'data:font/ttf;base64,([A-Za-z0-9+/=]+)',html).group(1)
    assert base64.b64decode(image)==resources.files('mercy').joinpath('assets','teacher.webp').read_bytes()
    assert base64.b64decode(font)==resources.files('mercy').joinpath('assets','notebook.ttf').read_bytes()
    assert '/* MERCY_MASCOT */' not in html and '/* MERCY_NOTEBOOK_FONT */' not in html


def test_cli_greeting_preserves_json_tool_output(tmp_path):
    (tmp_path/'app.py').write_text('def hello(): return True\n')
    base=[sys.executable,'-m','mercy']
    context=subprocess.run(base+['context','--project',str(tmp_path),'--path','app.py'],capture_output=True,text=True)
    assert context.returncode==0,context.stderr
    assert json.loads(context.stdout)['matches'][0]['path']=='app.py'
    run=subprocess.run(base+['prepare','--project',str(tmp_path),'--out',str(tmp_path/'mercy-output')],capture_output=True,text=True)
    assert run.returncode==0,run.stderr
    assert run.stdout.startswith('Mercy — that one teacher we all know\n')
