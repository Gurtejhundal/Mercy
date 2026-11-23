# Mercy

### that one teacher we all know

**From “I used AI to build this” to “I understand how this project works.”**

[Website](https://Gurtejhundal.github.io/Mercy/) · [Sample notebook](https://Gurtejhundal.github.io/Mercy/demo.html)

<img src="public/assets/teacher.webp" width="220" alt="Mercy, an unimpressed ink-doodle teacher with a messy bun and glasses">

Mercy is an AI coaching workflow inside **Codex or Claude Code**, backed by a local Python evidence toolkit. The host model investigates source code, explains it with citations, improves a study notebook and conducts a mock viva. No separate model server or provider key is required. The HTML is a self-contained offline report, not a chat backend.

It is designed for students who need a simple answer to: *Where is the backend? What connects to what? Where is the dataset? Did we train a model, or call somebody's API? What is RAG? Show me the actual code.*

> **Reality check:** Mercy does static analysis. Its visual links are **imports**, not verified runtime calls or a certified data-flow diagram. It cannot prove that a model was trained, that authentication works, or that a service is deployed simply by reading files.

## Start Mercy in this workspace

The Python package now lives at the repository root. Python 3.10+ is enough to run its local tools without installing runtime dependencies:

```bash
python3 -m mercy install --project . --platform both
```

In Codex, invoke **`$mercy explain this codebase and help me prepare for my viva`**. In Claude Code, use **`/mercy explain this codebase and help me prepare for my viva`**. Start a new host session if newly installed skills are not yet discovered.

Mercy has three modes: investigate a focused code question, prepare a reviewed notebook, or coach a mock viva one question at a time. It does not modify your application or run it as part of ordinary analysis. Code excerpts are visible to the host model under that host's privacy settings; “no separate model server” does not mean the host itself runs offline.

### Evidence tools used by the agent

```bash
python3 -m mercy inspect --project examples/mini-rag
python3 -m mercy context --project examples/mini-rag --query "answer_question"
python3 -m mercy context --project examples/mini-rag --path rag.py --start 5
python3 -m mercy prepare --project examples/mini-rag --out mercy-output/example
python3 -m mercy review --project examples/mini-rag --input mercy-output/example/mercy-evidence.json --review mercy-output/example/review.json
python3 -m mercy render --input mercy-output/example/mercy-evidence.json
```

`prepare` creates starter questions from static clues. The host agent supplies the reasoning: inspect source, replace generic answers, add relevant questions, then run `review` and `render`. `context` returns bounded, redacted, numbered text matches. `review` validates complete question records and current source fingerprints, merges existing/new IDs and saves atomically. A review is a JSON object with only a `questions` array using the [question schema](docs/QUESTION_STRATEGY.md). It cannot replace scan metadata.

Preserve existing reviewed notebooks. For a fresh scan after source changes, prepare into a new folder under `mercy-output` and recheck answers before carrying them forward. Older evidence without source fingerprints can still render; refresh it before using the new review command.

## Try the included example

Open `output-example/mercy-studio.html` in any modern desktop browser. The example is deliberately misleading: the folder is named `mini-rag`, but the code does not demonstrate a real retrieval pipeline. Mercy must not claim it uses RAG merely because the project is named that way.

### What you can do in the HTML

| Area | Interaction | What it means |
|---|---|---|
| **Study Guide** | Read project signals, missing evidence and the three-step study path | Source snapshot only |
| **Architecture** | Pan, zoom, select file nodes and inspect import arrows | A → B **means A imports B**, not a verified runtime call |
| **Flow Tracer** | Select a detected route/file and follow a static dependency trail | Not a verified request-to-database pipeline |
| **Directory Atlas** | Expand folder tree; open a folder tile; click individual file tiles | Directory tree reflects indexed paths, not all files if scan was capped |
| **Mind Map** | Expand subjects into questions; read answers and citations beside the map; pan, zoom and fit | General concepts are not automatically present in your project |
| **Viva Questions** | Search, filter by subject, hide/reveal answers, click file:line evidence | Question bank contains real evidence references and explicit unknowns |

The user interface is **responsive** and uses accessible file trees and keyboard-selectable SVG nodes. It uses a black-and-white ink notebook: ruled paper, handwritten headings, the supplied teacher character, a branching mind map and source inspectors. The font and artwork are embedded in generated HTML for offline use. It **samples safe hex color hints from the analyzed project's CSS** as metadata; the notebook keeps a fixed black-and-white visual style. It cannot automatically understand a full product design system or infer branding from a JavaScript application without appropriate local style files.

## Install and run (Ubuntu/Linux/macOS)

Requires Python 3.10+. From the extracted `Mercy` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
mercy prepare --project /path/to/your/repository
```

Open `/path/to/your/repository/mercy-output/mercy-studio.html` **directly in your browser**. The entire page, its graph data, and its functionality are embedded in that single HTML file.

Generated files:

- `mercy-studio.html` — **primary deliverable:** mind map, import graph, dependency trail, treemap and question lab.
- `mercy-evidence.json` — editable and machine-readable scan evidence + Q&A; source for regeneration.
- `mercy-viva.md` — text alternative with the complete question answers.
- `mercy-architecture.md` — Mermaid-style static import clues and provenance hints.

A legacy PDF is **off by default** and ReportLab is not required for HTML. If you specifically want PDF, first install the optional extra from the Mercy checkout (`pip install -e '.[pdf]'`), then pass `--pdf`:

```bash
mercy prepare --project . --pdf
```

The HTML includes file paths, exported symbols, framework names, routes and question answers. Review it before you share it with anyone, especially if the underlying project is confidential. No raw project source bodies are embedded by this exporter.

## Enable Mercy inside Claude Code and Codex

First ensure the `mercy` CLI is installed and available on your PATH. Then:

```bash
mercy install --project /path/to/repository --platform both
```

- **Claude Code:** invoke `/mercy` inside the target repo.
- **Codex:** invoke `$mercy` inside the target repo.

`@mercy` is **not** a universal skill invocation; different coding agents have different mechanisms. The skills use the host model to investigate source with `mercy context`, apply reviewed answers with `mercy review`, and regenerate the notebook with `mercy render`. A focused question needs no new report.

Optional Claude Code hook, **not needed** for normal usage:

```bash
mercy install --project /path/to/repository --platform both --hooks
```

This adds only a small `SessionStart` reminder hook that must be reviewed/approved in Claude. It does not bypass any agent permission or run scans automatically. There is no Codex hook setup in this version.

## Command reference

```bash
mercy prepare --project .                   # offline HTML + evidence JSON + Markdown
mercy prepare --project . --limit 20        # first 20 core questions
mercy prepare --project . --pyq my-pyq.txt # user-supplied questions, origin not authenticated
mercy prepare --project . --pdf             # optional legacy PDF too
mercy inspect --project .                   # print scan metadata only; no files written
mercy context --project . --query "route handler" # numbered source matches
mercy context --project . --path app.py --start 10 # bounded source excerpt
mercy review --project . --input mercy-output/mercy-evidence.json --review mercy-output/review.json
mercy render --input mercy-output/mercy-evidence.json               # regenerate HTML and Markdown
mercy render --input mercy-output/mercy-evidence.json --project .   # also resample project theme
mercy render --input mercy-output/mercy-evidence.json --pdf         # optionally regenerate PDF
```

For **explicitly approved** API-assisted rewording, `--ai` is supported by the older engine and requires `OPENAI_API_KEY`. The native host skills never invoke this legacy option. The local CLI default does not make requests. Do not enable `--ai` in private or client projects without authorization: even reduced code metadata can be sensitive.

### How design-language adaptation works

Mercy also supports an explicit and safe `mercy-theme.json` in the **analyzed project root**, which stores validated palette hints and legacy design tokens without accepting arbitrary CSS:

```json
{
  "primary": "#3f624b",
  "secondary": "#b4825d",
  "background": "#f8f9f5",
  "panel": "#ffffff",
  "text": "#242d27",
  "muted": "#657066",
  "font": "system",
  "radius": 12
}
```

Allowed colors are 6-digit hex strings; `font` can be `system`, `serif`, or `mono`; `radius` is an integer from 5 to 28. Mercy rejects low-contrast background/text combinations. The current ink notebook keeps a fixed visual style; validated tokens are retained in evidence for compatibility rather than applied to its surfaces. These design tokens are saved in the evidence JSON so `mercy render` preserves them even when you do not pass `--project` again. `examples/galaxy-demo/mercy-theme.json` demonstrates it.


Mercy finds a bounded sample of **literal hex colors** from readable, non-symlink CSS/HTML/Vue/Svelte style files that were already indexed during the scan. It selects an accent palette from non-neutral colors. The notebook keeps a consistent black-ink style; sampled colors are retained as palette metadata. This is **palette adaptation, not visual cloning**: typography, component shapes, and contrast protections remain Mercy-specific. See [`docs/DESIGN_SYSTEM.md`](docs/DESIGN_SYSTEM.md) for the detailed rules and limitations.

## Security and fidelity

Mercy does **not** execute imported project code, launch a server, open databases, follow symlinks, read `.env` files, or send repository data to external services by default. The browser page contains no external scripts, networking calls, or localStorage usage. It uses safe DOM text insertion and escapes JSON embedded in HTML to prevent HTML/script-breakout by malicious file names.

- File groups contain only indexed paths; no groups are fabricated.
- File roles are heuristic (path, extension, source code clue), not guaranteed service boundaries.
- Architecture links are statically resolved imports. Mind-map branches organize study topics and questions.
- Flow Tracer is explicitly labelled as a **reference trail**, never a verified runtime data flow.
- Dataset-like files and AI API libraries are **clues**, not proof of training, retrieval, accuracy or inference deployment.
- The scanner is bounded and skips several high-risk/large files; the map may be incomplete.

## Development and tests

```bash
pip install pytest
python3 -m pytest -q
python3 -m unittest discover -s tests -p test_agent.py -v
node --test tests/studio_ui.test.cjs
```

The test suite checks CLI output, HTML safety, file edges, data provenance, theme extraction and skill installation. The browser interaction smoke test uses optional Playwright/Chromium and is documented in `docs/VALIDATION.md`.

## Repository layout

```text
Mercy/
├── mercy/
│   ├── agent.py           # source context, proof validation, atomic answer review
│   ├── scanner.py         # local, bounded code metadata scan
│   ├── questions.py       # plain-language Q&A with evidence and uncertainty
│   ├── studio.py          # atlas payload + color sampling + safe HTML embedding
│   ├── assets/studio.html # single-file offline mind map, graph, tree and Q&A
│   ├── renderer.py        # evidence JSON, Markdown, optional legacy PDF
│   ├── cli.py             # prepare, inspect, context, review, render, install
│   └── integrations/      # packaged native agent skill files
├── skills/                # source copies of agent instructions
├── hooks/                 # optional reminder hook example
├── docs/                  # concept, architecture, UI/UX, safety, roadmap, tests
├── examples/mini-rag/     # intentionally misleading example
├── output-example/        # generated single-file HTML + JSON + Markdown
└── tests/
```

## Boundaries and next release

This version provides a **native Codex/Claude coaching workflow and an offline study report**. The host model performs reasoning; the CLI provides bounded source access and validated report updates. It is not a runtime architecture verifier or a full AST call graph. Future work: approved runtime traces, end-to-end frontend/API/backend/storage mapping, AST symbol graphs across more languages, semantic search over code, and project-theme adapters that understand design tokens. Details in [`docs/ROADMAP.md`](docs/ROADMAP.md).

Mercy distinguishes source clues, host reasoning and runtime proof. A citation validates a location, not the truth of every sentence an AI writes.

## Website and notebook artwork

`public/` is a buildless static website, deployed by `.github/workflows/pages.yml` to GitHub Pages. It introduces the native coaching workflow and links to `public/demo.html`, a real report generated from `examples/mini-rag`. The report exporter embeds its own font and teacher image; report files do not depend on website assets or a CDN.

The teacher drawing was supplied by the project owner. Patrick Hand by Patrick Wagesreiter is included under the SIL Open Font License; see `mercy/assets/OFL.txt` and `public/assets/OFL.txt`.

On native skill invocation Mercy starts with **“Mercy — that one teacher we all know”**. Human-readable CLI commands display the same line; `inspect` and `context` keep clean JSON output for tool callers.
