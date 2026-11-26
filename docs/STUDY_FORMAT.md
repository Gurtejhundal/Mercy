# Viva study format

Write one direct question (at most 14 words) and a spoken answer (at most 45 words, normally 1–2 sentences). Use familiar words. Preserve conditions that change the answer: “No, this is a local limit” is better than an inaccurate confident claim. Avoid essays, implementation trivia and repeated taglines. Keep detailed reasoning in `answer`; the report puts it under **Details**.

Every question retains the existing required fields: `id`, `category`, `difficulty`, `question`, `answer`, `explain_like_im_10`, `status`, `evidence`. Guided submissions also require `viva_question` and `viva_answer`. `verify_next` is required for unverified guided answers. Existing evidence without the new fields still renders; it uses the original answer when short, otherwise its simple explanation. No automatic truncation discards conditions.

The host submits complete question records in `{"questions": [...]}` through `mercy review`. The source snapshot, bounded word counts, indexed paths, line ranges and diagram structure are checked locally. These checks cannot establish that an explanation is true.

## Components and folders

On the module question, add `components` and `directories` when source supports them:

```json
{
  "components": [{
    "id": "api", "name": "Question API",
    "description": "Accepts a question and returns an answer.",
    "files": ["app.py"],
    "evidence": [{"path": "app.py", "line": 9}]
  }],
  "directories": [{
    "path": "web", "description": "Website pages and browser scripts.",
    "evidence": [{"path": "web/index.html", "line": 1}]
  }]
}
```

Paths above are illustrative; use indexed project paths. Each component needs an ID, a name (6 words), a description (25 words), files and evidence. At most 12 components across the report. IDs are unique across the report and each file belongs to only one component. Add optional `connections: [{source, target, label, evidence}]` between those component IDs: at most 30 directed pairs, short labels (6 words), no self-loops or duplicates. Inspect handlers/call sites, including browser HTTP. The whole-system diagram uses these source-traced relationships; without them it falls back to **resolved imports**. Neither proves execution. External integrations can be discussed in answers; a diagram does not invent local files for external services.

Directory descriptions are at most 25 words. Explain actual contents, e.g. “Website pages and styles,” rather than merely saying “frontend.” Do not assume every `public` folder contains only media. Without reviewed components or directory descriptions, the report labels its name/type-based suggestions as heuristic.

## User flow

On the workflow question, add `flow`. Legacy `demonstration` records still validate and remain in JSON, but no Demo section is displayed:

```json
{
  "flow": {
    "nodes": [
      {"id":"start", "label":"Prepare a question", "kind":"start", "evidence":[{"path":"app.py","line":9}]},
      {"id":"send", "label":"Submit to /ask", "kind":"action", "evidence":[{"path":"app.py","line":9}]},
      {"id":"end", "label":"Read the answer", "kind":"end", "evidence":[{"path":"app.py","line":11}]}
    ],
    "edges": [
      {"source":"start", "target":"send", "evidence":[{"path":"app.py","line":9}]},
      {"source":"send", "target":"end", "evidence":[{"path":"app.py","line":11}]}
    ]
  },
  "demonstration": [{
    "action":"Submit a question to /ask.",
    "expected":"With a working provider setup, the handler returns the model’s answer.",
    "evidence":[{"path":"app.py","line":9}]
  }]
}
```

A user flow tells what a person does and sees. Inspect handlers and call sites; imports alone cannot establish this story. `kind` is `start`, `action`, `decision` or `end`. Labels are at most 12 words. Every node and edge needs evidence; all nodes must be reachable from a start and able to reach an end. End nodes have no outgoing edges. Decision diamonds need at least two differently labelled branches (e.g. Yes/No), grounded in real conditions. Include retry and failure paths where relevant; do not force a decision into code with no such branch. Limits: 20 nodes, 30 edges per flow.

Demo steps have `action` (20 words), `expected` (30 words) and evidence. At most 10 steps. Describe actions the learner can demonstrate and the expected source behavior. This is a walkthrough, not proof of an executed application. Omit unsupported aids and explain the gap in the relevant answer. Never invent a workflow to fill an empty page.

`mercy next` returns the answer contract and field shapes alongside one bounded review task, so installed plugins do not depend on the learner repository containing this document.

## Project overview and explorer explanations

Project Overview replaces the chapter reader. On the dependencies question, add a `stack` array. Each entry has:

- `id`, unique across the report; `kind`: `frontend`, `backend`, `model`, `storage` or `tool`.
- `name` (10 words), `description` (45 words), `paths` (indexed files or folders), and source `evidence`.
- Optional `origin` (35 words): model author, conversion/package source and download location. Distinguish these and explain which source is established by code versus an upstream resource. Never infer training, active provider selection or successful downloads.
- Optional `logo`: `python`, `fastapi`, `html5`, `javascript`, `huggingface`, `nvidia`, `ffmpeg`, `sqlite` or `react`. Use the technology/provider mark honestly; unknown marks use a text monogram.
- `resources`: up to six `{label, url}` links. URLs must use HTTPS, have a hostname and contain no credentials, whitespace or backslashes. Use authoritative model cards, upstream repositories or documentation. The report only opens them when the learner chooses a link.

On the module question, add `file_notes`: up to 400 `{path, description, evidence}` records. Paths must be indexed files and unique across the report; descriptions are at most 45 words. Explain what a file is about rather than repeating its name. Directory descriptions remain separate. Unreviewed files show their indexed symbols or an explicit gap; no purpose is fabricated from a filename.

The Folders view has a nested explorer on the left and the selected item’s explanation on the right. Architecture opens the whole system; component tabs focus its incoming and outgoing reviewed relationships (or imports as fallback). The user flowchart stays a separate source-traced user journey.

## Viva foundations in Project Overview

Add `overview: true` to selected question records; the existing category groups them in the overview. The same answers remain searchable in Questions. Use short, project-specific answers for the user problem, target users, benefits, data types/sources, training versus inference, weight formats/locations, algorithms, meaningful parameters, formulas and their code, evaluation, chunk counts, RAG, CSV purpose, classification labels versus code classes, full forms, inspiration and output. Include only relevant concepts; say when a requested item is absent or unverified. Never manufacture the author’s personal story.

A question may include `resources: [{label, url}]` with the same safe HTTPS rules as stack entries. Identify upstream facts as upstream; their datasets and benchmark numbers are not local training or measured application accuracy. Separate a formula’s implementation, its reference, a numerical example and actual empirical validation.

When the user requests embedded code, `--include-source --project PATH` adds redacted indexed source to the right-hand inspector. Ordinary path buttons open folders; source citations open and highlight the selected line. This option checks the saved snapshot and reads only code/styles, with a 2 MB total budget, 90 KB file limit and 160-character line cap. It skips datasets, model weights and JSON/text settings. Source is inert text; it is never executed. Reports without source opt-in still show explanations and citations. Do not publish private source previews merely to obtain a browser screenshot.
