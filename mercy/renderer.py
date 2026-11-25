"""Export viva study packs to Markdown/JSON and optionally paginated PDF."""
from __future__ import annotations
from html import escape
from pathlib import Path
import json
import os
import stat
import tempfile


def fmt_evidence(hits):
    return ', '.join(f"{x['path']}:{x['line']}" for x in hits) or 'No repository proof located'


def export_markdown(report, questions, output):
    lines = [f'# MERCY | {report["project"]} | Viva Preparation', '',
             '> Evidence-first preparation. A source reference shows a code clue, not proof that a feature works in production.', '',
             '## Repository scan', '',
             f'- Files read: {report["summary"]["read_files"]}',
             f'- Data-shaped files: {report["summary"]["data_files"]}',
             f'- Routes detected: {report["summary"]["routes_found"]}',
             f'- Resolved local imports: {report["summary"]["module_links"]}',
             f'- Tech markers: {", ".join(sorted(report["frameworks"])) or "Not identified"}', '',
             '## Module connections', '']
    lines += [f'- `{e["source"]}` -> `{e["target"]}` (import `{e["via"]}`)' for e in report['edges'][:100]] or ['- No local module imports were resolved.']
    lines += ['', '## Important verification gaps', '']
    lines += [f'- {w}' for w in report['warnings']] or ['- No scanner warnings. Runtime behavior remains untested.']
    last = None
    for q in questions:
        if q['category'] != last:
            lines += ['', f'## {q["category"]}', '']; last=q['category']
        lines += [f'### {q["id"]}. {q["question"]}', '',
                  f'**Short viva answer:** {q["answer"]}', '',
                  f'**Explain simply:** {q["explain_like_im_10"]}', '',
                  f'**Evidence:** {fmt_evidence(q["evidence"])}', '',
                  f'**Proof level:** {q["status"]}', '']
        if q.get('verify_next'): lines += [f'**Verify:** {q["verify_next"]}', '']
    Path(output).write_text('\n'.join(lines).rstrip()+'\n', encoding='utf-8')


def export_json(report, questions, output, *, workflow=None):
    output = Path(output)
    if output.is_symlink():
        raise ValueError('Evidence output must not be a symbolic link.')
    data = {'report':report,'questions':questions}
    if workflow is not None:
        data['workflow'] = workflow
    payload = json.dumps(data, indent=2, ensure_ascii=False)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=output.parent,
                                         prefix='.mercy-evidence-', delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        if output.exists():
            temporary.chmod(stat.S_IMODE(output.stat().st_mode))
        os.replace(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _p(text):
    return escape(str(text)).replace('\n', '<br/>')


def export_pdf(report, questions, output):
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, HRFlowable, PageBreak
    except ImportError as exc:
        raise RuntimeError('PDF export requires ReportLab. Install with: pip install "mercy-viva[pdf]"') from exc
    INK = colors.HexColor('#1B2733')
    BLUE = colors.HexColor('#295E88')
    LIGHT = colors.HexColor('#687789')
    dest = str(output)
    doc = SimpleDocTemplate(dest, pagesize=(595.28,841.89), topMargin=49, bottomMargin=48,
         leftMargin=51, rightMargin=51, title=f'Mercy viva | {report["project"]}', author='Mercy')
    st = getSampleStyleSheet()
    st.add(ParagraphStyle(name='MercyTitle', fontName='Helvetica-Bold', fontSize=24, leading=29, textColor=INK, spaceAfter=12))
    st.add(ParagraphStyle(name='MercyHeading', fontName='Helvetica-Bold', fontSize=13.5, leading=18, textColor=BLUE, spaceBefore=18, spaceAfter=8))
    st.add(ParagraphStyle(name='MercyQuestion', fontName='Helvetica-Bold', fontSize=10.7, leading=15, textColor=INK, spaceAfter=7))
    st.add(ParagraphStyle(name='MercyBody', fontName='Helvetica', fontSize=9.1, leading=13.8, textColor=INK, spaceAfter=6))
    st.add(ParagraphStyle(name='MercyNote', fontName='Helvetica', fontSize=8.1, leading=11.5, textColor=LIGHT, spaceAfter=6))
    st.add(ParagraphStyle(name='MercyCentered', fontName='Helvetica', fontSize=9, leading=14, alignment=TA_CENTER))
    story=[Spacer(1,24), Paragraph('MERCY',st['MercyTitle']),
           Paragraph('Project Viva Preparation',st['MercyHeading']),
           Paragraph(f'Project: {_p(report["project"])}',st['MercyBody']),
           Paragraph('Your project, explained simply. Answers cite files where evidence exists. Unverified claims are clearly marked.',st['MercyBody']),
           Spacer(1,15), HRFlowable(width='100%',color=BLUE,thickness=1.5),Spacer(1,12),
           Paragraph('Codebase snapshot',st['MercyHeading']),
           Paragraph(f'Read {report["summary"]["read_files"]} files | Found {report["summary"]["routes_found"]} routes | {len(questions)} viva questions',st['MercyBody']),
           Paragraph('Technology clues: '+_p(', '.join(sorted(report['frameworks'])) or 'Not established'),st['MercyBody']),
           Paragraph('Important: Reading code does not confirm that deployment, authentication, training or tests actually work.',st['MercyNote']),
           Paragraph('What the scanner could not verify',st['MercyHeading'])]
    for w in report['warnings'][:8]: story.append(Paragraph('&#8226; '+_p(w), st['MercyBody']))
    story.append(Paragraph('Module connections',st['MercyHeading']))
    for e in report['edges'][:16]:
        story.append(Paragraph(_p(f"{e['source']} -> {e['target']}"), st['MercyNote']))
    if not report['edges']:
        story.append(Paragraph('No local module imports were resolved automatically.', st['MercyNote']))
    story.append(PageBreak())
    last = None
    for q in questions:
        if q['category'] != last:
            story.append(Paragraph(_p(q['category']),st['MercyHeading'])); last=q['category']
        block=[Paragraph(_p(f"{q['id']} [{q['difficulty']}] {q['question']}"), st['MercyQuestion']),
             Paragraph('<b>Say this:</b> '+_p(q['answer']),st['MercyBody']),
             Paragraph('<b>In simple words:</b> '+_p(q['explain_like_im_10']),st['MercyBody']),
             Paragraph('Evidence: '+_p(fmt_evidence(q['evidence'])),st['MercyNote'])]
        if q.get('verify_next'):
            block.append(Paragraph('Check next: '+_p(q['verify_next']),st['MercyNote']))
        block.append(Spacer(1,8))
        story.append(KeepTogether(block))
    def footer(c, d):
        c.saveState()
        c.setFont('Helvetica',8)
        c.setFillColor(LIGHT)
        c.drawString(51,28,'MERCY - Evidence before confidence')
        c.drawRightString(544,28,f'Page {d.page}')
        c.restoreState()
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def export_architecture(report, output):
    """Conservative architecture map: import edges do not imply runtime calls."""
    def q(s):
        return str(s).replace('"','\'').replace('[','(').replace(']',')')[:110]
    paths=sorted({e['source'] for e in report['edges']} | {e['target'] for e in report['edges']})[:36]
    names={p:f'N{i}' for i,p in enumerate(paths)}
    lines=[f'# Mercy architecture clues: {report["project"]}', '',
           '> **Caution:** imports are dependency clues, not verified runtime data flow.', '',
           '## Local module imports', '', '```mermaid', 'flowchart LR']
    lines += [f'    {name}["{q(p)}"]' for p,name in names.items()]
    lines += [f'    {names[e["source"]]} --> {names[e["target"]]}' for e in report['edges']
              if e['source'] in names and e['target'] in names][:65]
    if not paths: lines.append('    X["No resolved local imports"]')
    lines += ['```','', '## Detected routes', '', '| Endpoint | Source |', '|---|---|']
    for f in report['files']:
        for route in f['routes']:
            lines.append(f'| `{route["path"]}` | `{f["path"]}:{route["line"]}` |')
    if not report['summary']['routes_found']: lines.append('| No route declarations verified | - |')
    lines += ['', '## Technology hints', '', '| Tech | Evidence |', '|---|---|']
    for fw, entries in sorted(report['frameworks'].items()):
        lines.append(f'| {fw} | {fmt_evidence(entries[:3])} |')
    if not report['frameworks']: lines.append('| Not identified | - |')
    lines += ['', '## Dataset and model provenance', '']
    lines += [f'- Data-shaped file candidate: `{d["path"]}` — purpose not verified.' for d in report['datasets']] or ['- No local dataset file confirmed.']
    lines += ['- Training steps found: '+str(len(report['signals'].get('training',[])))+' (code markers; not proof of a completed run).',
              '- AI API markers found: '+str(len(report['signals'].get('llm_api',[])))+'.',
              '- Retrieval markers found: '+str(len(report['signals'].get('rag',[])))+' (not a complete RAG proof).','',
              '## What to trace manually', '',
              '1. One user action and the actual frontend call.',
              '2. The exact API handler and its input/output schema.',
              '3. The database query or model call, if any.',
              '4. What happens on failure and how errors reach the user.',
              '5. Training evidence: data provenance, experiment logs, model weights, and evaluation metrics (if the project trains a model).', '']
    Path(output).write_text('\n'.join(lines),encoding='utf-8')
