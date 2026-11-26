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
        answer = q.get('viva_answer') or (q['answer'] if len(q['answer'].split()) <= 45 else q['explain_like_im_10'])
        lines += [f"### {q['id']}. {q.get('viva_question', q['question'])}", '', answer, '',
                  '<details>', '<summary>Details</summary>', '', q['answer'], '',
                  f"**Source:** {fmt_evidence(q['evidence'])}", '',
                  f"**Evidence level:** {q['status']} (source analysis; execution not verified)", '']
        if q['explain_like_im_10'] not in {answer, q['answer']}:
            lines += [q['explain_like_im_10'], '']
        if q.get('verify_next'): lines += [f"**Check:** {q['verify_next']}", '']
        lines += ['</details>', '']
        if q.get('demonstration'):
            lines += ['#### Demo', '']
            for i, step in enumerate(q['demonstration'], 1):
                lines += [f"{i}. **{step['action']}** {step['expected']} ({fmt_evidence(step['evidence'])})", '']
        if q.get('flow'):
            lines += ['#### User flow (source trace)', '']
            labels = {n['id']:n['label'] for n in q['flow']['nodes']}
            lines += [f"- {labels[e['source']]} → {labels[e['target']]}" +
                      (f" ({e['label']})" if e.get('label') else '') +
                      f" — {fmt_evidence(e['evidence'])}" for e in q['flow']['edges']]
        for technology in q.get('stack', []):
            lines += [f"#### {technology['kind'].title()}: {technology['name']}", '', technology['description'], '']
            if technology.get('origin'): lines += ['From: '+technology['origin'], '']
            lines += ['Locations: '+', '.join(technology['paths']), '', 'Source: '+fmt_evidence(technology['evidence']), '']
            lines += [f"- [{r['label']}]({r['url']})" for r in technology.get('resources', [])]
        if q.get('file_notes'):
            lines += ['', '<details>', '<summary>File explanations</summary>', '']
            lines += [f"- **{item['path']}:** {item['description']} ({fmt_evidence(item['evidence'])})" for item in q['file_notes']]
            lines += ['', '</details>', '']
        for component in q.get('components', []):
            lines += [f"- **{component['name']}:** {component['description']} ({fmt_evidence(component['evidence'])})"]
        for directory in q.get('directories', []):
            lines += [f"- **{directory['path']}/:** {directory['description']} ({fmt_evidence(directory['evidence'])})"]
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
        block=[Paragraph(_p(f"{q['id']} {q.get('viva_question', q['question'])}"), st['MercyQuestion']),
             Paragraph('<b>Say this:</b> '+_p(q.get('viva_answer', q['answer'])),st['MercyBody']),
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


def export_architecture(report, output, questions=()):
    """Component dependencies remain resolved imports, never runtime calls."""
    from .presentation import study_aids
    aids = study_aids(report, list(questions), [])
    def label(value):
        return str(value).replace('"', "'").replace('[', '(').replace(']', ')').replace('`', "'").replace('\n', ' ')[:110]
    components = aids['components']
    names = {c['id']:f'N{i}' for i,c in enumerate(components)}
    lines = [f'# Architecture: {report["project"]}', '',
             '> Source analysis. Arrows aggregate resolved imports, not runtime calls.', '',
             '```mermaid', 'flowchart LR']
    lines += [f'    {names[c["id"]]}["{label(c["name"])}"]' for c in components]
    lines += [f'    {names[e["source"]]} --> {names[e["target"]]}' for e in aids['component_edges']]
    if not components:
        lines += ['    X["No reviewed components; add components to the module question"]']
    lines += ['```', '']
    for c in components:
        lines += [f'## {c["name"]}', '', c['description'], '',
                  f'Source: {fmt_evidence(c["evidence"])}', '']
    for edge in aids['component_edges']:
        lines += [f'- `{e["source"]}:{e["line"]}` imports `{e["target"]}`'
                  for e in edge['imports']]
    Path(output).write_text('\n'.join(lines).rstrip()+'\n', encoding='utf-8')
