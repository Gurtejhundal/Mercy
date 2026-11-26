"""Mercy command line interface."""
from __future__ import annotations
import argparse
import json
import sys
from importlib import resources
from pathlib import Path

from . import TAGLINE
from .scanner import scan_project
from .agent import source_context, validate_questions, apply_review, next_question, review_progress
from .questions import make_questions, make_guided_questions, import_user_pyqs
from .renderer import export_json, export_markdown, export_pdf, export_architecture
from .studio import export_studio, extract_theme


def _install(root: Path, platform: str, hooks: bool, force: bool):
    if not root.is_dir():
        raise ValueError(f'Project directory missing: {root}')
    if hooks and platform == 'codex':
        raise ValueError('The optional session hook is Claude-only. Use --platform claude or both.')
    for name in (['claude','codex'] if platform == 'both' else [platform]):
        target = root / ('.claude/skills/mercy' if name == 'claude' else '.agents/skills/mercy')
        target.mkdir(parents=True, exist_ok=True)
        source = resources.files('mercy').joinpath('integrations',name,'SKILL.md')
        destination = target / 'SKILL.md'
        if destination.exists() and not force:
            print(f'Unchanged (already exists): {destination}. Use --force to overwrite.')
        else:
            destination.write_text(source.read_text(encoding='utf-8'),encoding='utf-8')
            print(f'Installed: {destination}')
        if name == 'codex':
            meta = resources.files('mercy').joinpath('integrations','codex','openai.yaml')
            (target / 'agents').mkdir(exist_ok=True)
            outfile=target / 'agents/openai.yaml'
            if not outfile.exists() or force:
                outfile.write_text(meta.read_text(encoding='utf-8'),encoding='utf-8')
    if hooks:
        hook = root/'.claude/hooks/mercy-session.sh'
        hook.parent.mkdir(parents=True, exist_ok=True)
        if not hook.exists() or force:
            hook.write_text('#!/bin/sh\n# Read-only reminder; never scans or sends project data.\nprintf "Mercy is available. Run /mercy to prepare a project viva.\\n"\n', encoding='utf-8')
        settings = root / '.claude/settings.local.json'
        try:
            existing = json.loads(settings.read_text(encoding='utf-8')) if settings.exists() else {}
        except json.JSONDecodeError as exc:
            raise ValueError('Existing Claude settings contain invalid JSON; no changes made to settings.') from exc
        if not isinstance(existing,dict):
            raise ValueError('Claude settings JSON must be an object.')
        hooks_config = existing.setdefault('hooks',{})
        if not isinstance(hooks_config,dict):
            raise ValueError('Claude hooks settings must be an object.')
        records = hooks_config.setdefault('SessionStart',[])
        if not isinstance(records,list):
            raise ValueError('Claude SessionStart settings must be an array.')
        entry={'hooks':[{'type':'command','command':'sh "${CLAUDE_PROJECT_DIR}/.claude/hooks/mercy-session.sh"'}]}
        if not any(entry == e for e in records): records.append(entry)
        settings.parent.mkdir(parents=True,exist_ok=True)
        settings.write_text(json.dumps(existing,indent=2)+'\n',encoding='utf-8')
        print(f'Optional read-only SessionStart hook added: {settings}')
        print('Review and approve the hook in Claude Code /hooks, then start a new session.')


def main(argv=None):
    parser=argparse.ArgumentParser(prog='mercy', description='Mercy — '+TAGLINE+'. Source-grounded codebase understanding and viva coaching.')
    sub=parser.add_subparsers(dest='command',required=True)
    prep=sub.add_parser('prepare',help='Create interactive offline HTML Studio + JSON + Markdown from a project')
    prep.add_argument('--project',default='.',help='Local repository directory')
    prep.add_argument('--out',default=None,help='Output directory (default: PROJECT/mercy-output)')
    prep.add_argument('--limit',type=int,default=0,help='Maximum generated questions (0 = all)')
    prep.add_argument('--pyq',default=None,help='Optional user-supplied .txt or .md list of past questions (not authenticated)')
    prep.add_argument('--ai',action='store_true',help='Explicitly send summarized metadata to OpenAI for phrasing improvements')
    prep.add_argument('--model',default='gpt-4.1-mini',help='OpenAI chat-completions model for --ai')
    prep.add_argument('--pdf',action='store_true',help='Also create legacy printable PDF (HTML is the default)')
    prep.add_argument('--max-files',type=int,default=400)
    prep.add_argument('--guided',action='store_true',help='Seed ten project topics for one-question-at-a-time host review')
    render=sub.add_parser('render',help='Rebuild HTML/Markdown after reviewing or refining evidence JSON')
    render.add_argument('--input',required=True,help='mercy-evidence.json (editable question answers)')
    render.add_argument('--out',default=None,help='Output directory; defaults to JSON directory')
    render.add_argument('--pdf',action='store_true',help='Also export legacy PDF')
    render.add_argument('--project',default=None,help='Optional local project directory to re-detect its color palette')
    inspect=sub.add_parser('inspect',help='Print source map JSON, with no PDF')
    inspect.add_argument('--project',default='.')
    context=sub.add_parser('context',help='Read bounded, redacted source excerpts for the host agent')
    context.add_argument('--project',default='.')
    selection=context.add_mutually_exclusive_group(required=True)
    selection.add_argument('--query',help='Find relevant source text')
    selection.add_argument('--path',help='Read an indexed relative source path')
    context.add_argument('--start',type=int,default=1,help='First line for --path (up to 40 lines)')
    context.add_argument('--limit',type=int,default=8,help='Maximum search results (1–12)')
    review=sub.add_parser('review',help='Validate and atomically merge agent-reviewed questions')
    review.add_argument('--input',required=True,help='Existing mercy-evidence.json')
    review.add_argument('--review',required=True,help='JSON containing complete questions to replace/add')
    review.add_argument('--project',required=True,help='Project source for checking current citations')
    next_step=sub.add_parser('next',help='Return one guided review task with bounded source excerpts')
    next_step.add_argument('--input',required=True,help='Evidence JSON created with prepare --guided')
    next_step.add_argument('--project',required=True,help='Project source for checking the saved snapshot')
    install=sub.add_parser('install',help='Install local skills into an existing project')
    install.add_argument('--project',default='.')
    install.add_argument('--platform',choices=['claude','codex','both'],default='both')
    install.add_argument('--hooks',action='store_true',help='Explicitly enable an optional, read-only Claude SessionStart reminder')
    install.add_argument('--force',action='store_true',help='Overwrite existing Mercy skill files')
    args=parser.parse_args(argv)
    if args.command not in {'context', 'inspect', 'next'}:
        print('Mercy — '+TAGLINE)
    try:
        if args.command == 'context':
            print(json.dumps(source_context(args.project,query=args.query,path=args.path,start=args.start,limit=args.limit),indent=2,ensure_ascii=False))
            return 0
        if args.command == 'next':
            print(json.dumps(next_question(args.input,args.project),indent=2,ensure_ascii=False))
            return 0
        if args.command == 'review':
            count=apply_review(args.input,args.review,args.project)
            print(f'Applied {count} reviewed questions. Run mercy render --input to update the notebook.')
            return 0
        if args.command == 'install':
            _install(Path(args.project).expanduser().resolve(), args.platform, args.hooks, args.force)
            return 0
        if args.command == 'render':
            source=Path(args.input).expanduser().resolve()
            data=json.loads(source.read_text(encoding='utf-8'))
            audit,qs=data['report'],data['questions']
            validate_questions(audit,qs)
            review_progress(data)
            if args.project: audit['studio_theme'] = extract_theme(args.project,audit)
            out=Path(args.out).expanduser().resolve() if args.out else source.parent
            out.mkdir(parents=True,exist_ok=True)
            workflow=data.get('workflow')
            export_json(audit,qs,out/'mercy-evidence.json',workflow=workflow)
            export_markdown(audit,qs,out/'mercy-viva.md')
            export_studio(audit,qs,out/'mercy-studio.html',root=args.project,workflow=workflow)
            if args.pdf: export_pdf(audit,qs,out/'mercy-viva.pdf')
            export_architecture(audit,out/'mercy-architecture.md',qs)
            print(f'Re-rendered {len(qs)} questions and interactive HTML into {out}')
            return 0
        if args.command == 'inspect':
            print(json.dumps(scan_project(args.project),indent=2,ensure_ascii=False))
            return 0
        if args.max_files < 1 or args.limit < 0:
            parser.error('--max-files must be positive and --limit must be nonnegative.')
        if args.guided and (args.limit or args.ai):
            parser.error('--guided uses host review; omit --limit and --ai.')
        project=Path(args.project).expanduser().resolve()
        out=Path(args.out).expanduser().resolve() if args.out else project/'mercy-output'
        if args.guided and (out/'mercy-evidence.json').exists():
            raise ValueError('Guided evidence already exists. Resume with next, or use a fresh --out directory.')
        # Prevent writing to a source file directly; output directory is intentional.
        audit=scan_project(project,max_files=args.max_files)
        qs=make_guided_questions() if args.guided else make_questions(audit)
        workflow={'kind':'guided-v1','reviewed':{}} if args.guided else None
        if args.limit: qs=qs[:args.limit]
        if args.pyq: qs += import_user_pyqs(args.pyq, qs)
        if args.ai:
            from .llm import enrich
            qs=enrich(audit,qs,model=args.model)
        audit['studio_theme'] = extract_theme(project,audit)
        out.mkdir(parents=True,exist_ok=True)
        export_json(audit,qs,out/'mercy-evidence.json',workflow=workflow)
        export_markdown(audit,qs,out/'mercy-viva.md')
        export_studio(audit,qs,out/'mercy-studio.html',root=project,workflow=workflow)
        if args.pdf: export_pdf(audit,qs,out/'mercy-viva.pdf')
        export_architecture(audit,out/'mercy-architecture.md',qs)
        print(f'MERCY | {audit["project"]} | {len(qs)} questions | {audit["summary"]["read_files"]} files read')
        for filename in (('mercy-studio.html','mercy-viva.md','mercy-architecture.md','mercy-evidence.json') + (('mercy-viva.pdf',) if args.pdf else ())):
            print(out / filename)
        if audit['warnings']:
            print(f'Warning: {len(audit["warnings"])} verification gaps; read the output before your viva.')
        print('Mode: '+ ('OpenAI-enhanced (explicit opt-in)' if args.ai else 'offline / deterministic (no API requests)'))
        return 0
    except (ValueError, RuntimeError, OSError, KeyError, TypeError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
