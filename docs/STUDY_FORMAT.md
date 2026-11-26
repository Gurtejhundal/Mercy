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

Paths above are illustrative; use indexed project paths. Each component needs an ID, a name (6 words), a description (25 words), files and evidence. At most 12 components across the report. IDs are unique across the report and each file belongs to only one component. The diagram aggregates **resolved imports** between those files. It never invents runtime edges. External integrations can be discussed in answers; a diagram does not invent local files for external services.

Directory descriptions are at most 25 words. Explain actual contents, e.g. “Website pages and styles,” rather than merely saying “frontend.” Do not assume every `public` folder contains only media. Without reviewed components or directory descriptions, the report labels its name/type-based suggestions as heuristic.

## User flow and demonstration

On the workflow question, add `flow` and `demonstration`:

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
