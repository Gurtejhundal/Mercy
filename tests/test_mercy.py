from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path
from mercy.scanner import scan_project
from mercy.questions import make_questions


def test_no_faux_rag_from_readme(tmp_path):
    (tmp_path/'README.md').write_text('# Amazing RAG AI trained on 99 million samples\n')
    (tmp_path/'app.py').write_text('from openai import OpenAI\nclient = OpenAI()\n')
    r=scan_project(tmp_path)
    assert 'rag' not in r['signals']
    assert 'training' not in r['signals']
    questions=make_questions(r)
    assert 'not established' in next(q for q in questions if q['question'].startswith('What is RAG'))['answer']


def test_secrets_excluded_and_never_printed(tmp_path):
    (tmp_path/'.env').write_text('API_KEY=SHOULD_NOT_LEAK\n')
    (tmp_path/'app.py').write_text('api_key = "SHOULD_NOT_LEAK"\nfrom fastapi import FastAPI\napp=FastAPI()\n')
    (tmp_path/'data.csv').write_text('x,y\n1,2\n')
    r=scan_project(tmp_path)
    assert 'SHOULD_NOT_LEAK' not in json.dumps(r)
    assert '.env' not in json.dumps(r)
    assert r['datasets'][0]['path']=='data.csv'


def test_symlink_outside_not_followed(tmp_path):
    exterior = tmp_path.parent/'secret-target.txt'
    exterior.write_text('SENSITIVE_EXTERNAL')
    (tmp_path/'outside.py').symlink_to(exterior)
    report=scan_project(tmp_path)
    assert 'outside.py' not in [x['path'] for x in report['files']]


def test_evidence_links_and_routes(tmp_path):
    (tmp_path/'main.py').write_text('from helper import thing\nfrom fastapi import FastAPI\napp=FastAPI()\n@app.get("/health")\ndef hi(): return thing()\n')
    (tmp_path/'helper.py').write_text('def thing(): return 1\n')
    report=scan_project(tmp_path)
    assert {'source':'main.py','target':'helper.py','via':'helper','line':1} in report['edges']
    assert report['summary']['routes_found']==1
    assert report['files'][1]['routes'][0]['line']==4


def test_cli_generates_html_and_md_by_default(tmp_path):
    root=tmp_path/'repo'; root.mkdir()
    (root/'app.py').write_text('from fastapi import FastAPI\napp = FastAPI()\n')
    out=tmp_path/'report'
    p=subprocess.run([sys.executable,'-m','mercy','prepare','--project',str(root),'--out',str(out)],capture_output=True,text=True)
    assert p.returncode==0,p.stderr
    html=(out/'mercy-studio.html').read_text()
    assert '<canvas' not in html
    assert 'aria-label="Mind Map"' in html
    assert not (out/'mercy-viva.pdf').exists()
    assert (out/'mercy-architecture.md').exists()
    evidence=json.loads((out/'mercy-evidence.json').read_text())
    assert len(evidence['questions']) >= 40
    assert 'offline' in p.stdout


def test_install_both_and_opt_in_hook(tmp_path):
    p=subprocess.run([sys.executable,'-m','mercy','install','--project',str(tmp_path),'--hooks'],capture_output=True,text=True)
    assert p.returncode==0,p.stderr
    assert (tmp_path/'.claude/skills/mercy/SKILL.md').is_file()
    assert (tmp_path/'.agents/skills/mercy/SKILL.md').is_file()
    settings=json.loads((tmp_path/'.claude/settings.local.json').read_text())
    assert len(settings['hooks']['SessionStart'])==1
    p=subprocess.run([sys.executable,'-m','mercy','install','--project',str(tmp_path),'--hooks'],capture_output=True,text=True)
    assert p.returncode==0
    settings=json.loads((tmp_path/'.claude/settings.local.json').read_text())
    assert len(settings['hooks']['SessionStart'])==1


def test_no_ai_without_key(tmp_path,monkeypatch):
    monkeypatch.delenv('OPENAI_API_KEY',raising=False)
    (tmp_path/'main.py').write_text('print("hi")\n')
    p=subprocess.run([sys.executable,'-m','mercy','prepare','--project',str(tmp_path),'--ai'],capture_output=True,text=True,env={k:v for k,v in __import__('os').environ.items() if k!='OPENAI_API_KEY'})
    assert p.returncode != 0
    assert 'requires OPENAI_API_KEY' in p.stderr


def test_render_rejects_unknown_source_and_refines_answers(tmp_path):
    root=tmp_path/'repo'; root.mkdir()
    (root/'main.py').write_text('def answer(): return 42\n')
    out=tmp_path/'out'
    subprocess.run([sys.executable,'-m','mercy','prepare','--project',str(root),'--out',str(out)],check=True,capture_output=True)
    source=out/'mercy-evidence.json'
    data=json.loads(source.read_text())
    data['questions'][0]['answer']='My revised explanation of the project.'
    source.write_text(json.dumps(data))
    run=subprocess.run([sys.executable,'-m','mercy','render','--input',str(source)],capture_output=True,text=True)
    assert run.returncode==0,run.stderr
    assert 'My revised explanation' in (out/'mercy-viva.md').read_text()
    assert 'My revised explanation' in (out/'mercy-studio.html').read_text()
    data['questions'][0]['evidence']=[{'path':'fake.py','line':42}]
    source.write_text(json.dumps(data))
    run=subprocess.run([sys.executable,'-m','mercy','render','--input',str(source)],capture_output=True,text=True)
    assert run.returncode!=0
    assert 'not present' in run.stderr


def test_user_supplied_pyqs_are_not_automatically_claimed_as_proven(tmp_path):
    from mercy.questions import import_user_pyqs
    qfile=tmp_path/'sample-pyqs.txt'
    qfile.write_text('1. What is your tech stack?\n2. Can you prove 99% model accuracy?\n')
    extra=import_user_pyqs(str(qfile),[])
    assert len(extra)==2
    assert extra[1]['status']=='not_verified'
    assert not extra[1]['evidence']
