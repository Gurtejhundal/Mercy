> Historical record of the supplied implementation. Current native-agent behavior is documented in README.md and docs/ARCHITECTURE.md.

# Mercy 0.2.0 — Concept Audit (Interactive Version)

## Core product improvement

Previous concept: scan code → write a beginner-friendly PDF of probable viva questions. **New direction:** scan code → create a single-file interactive study environment with project topology, concept lessons, flow-tracing clues and searchable source-linked questions. The PDF becomes an optional export, not the primary experience.

The upgrade is meaningful because architecture is *spatial*: new students often understand a system better when they can click from a directory to an import to an explanation instead of memorizing pages. But the risks also increase: a glowing planet graph looks authoritative even when its grouping or links are uncertain.

## Major flaws and concrete responses

| Priority | Flaw | Mitigation | Present status |
|---|---|---|---|
| P0 | A convincing graphic can falsely imply that a live system architecture was verified | Every cluster is explicitly `heuristic`; every link is explicitly `static import`; don't draw nonexistent steps | **Implemented** |
| P0 | Five pretty planets could be fabricated even if only two code categories exist | Render only populated source-derived clusters (maximum named roles: 5) | **Implemented** |
| P0 | An `@mercy` magic command is not consistent across Claude Code/Codex | Use official skill invocation `/mercy` and `$mercy`; hooks optional/approved | **Implemented** |
| P0 | HTML injection via hostile repository filenames, symbols or question text | Escape JSON for HTML script parser; DOM uses `textContent`, never paste untrusted content as `innerHTML` | **Implemented** |
| P0 | Secret or private source data leaked into shareable HTML | Default to local scan, exclude high-risk files, embed only reduced metadata; tell user metadata is still sensitive | **Implemented with caveats** |
| P1 | UI overwhelms a novice with orbital art | Guided Mission Control; section labels, plain definitions, file click, source inspector, mock-viva-compatible question lab | **Implemented first pass** |
| P1 | Imported files mistaken for function calls or API flows | Show import chains, never pretend that they are runtime traces | **Implemented** |
| P1 | Large projects produce tangled graphs and overly tiny labels | Directory clusters; bounded scanner; pan/zoom; future aggregation/search | **Partial** |
| P1 | Motion and canvas reduce accessibility | Pause, OS reduced-motion, button list and file tree, textual Q&A and Markdown alternative | **Implemented first pass** |
| P1 | User expects project's design language; arbitrary Mercy colors are off-brand | Sample safe CSS hex accents, retain contrast and default; document that this is not full design-system cloning | **Partial** |
| P1 | A file rename or commit update can invalidate a study page | Rerun prepare/render; future commit-aware diffs | **Not automated** |
| P2 | A standalone HTML might become too large / slow with all code | Embed only metadata, not raw source; cap scanning and simplify particle drawing | **Implemented first pass** |
| P2 | “NotebookLM-like” implies real semantic knowledge graphs without code evidence | Distinguish interactive concept keymap from inferred runtime graph; semantic understanding awaits validated deeper agent tracing | **Explicitly scoped** |
| P2 | No actual learner comprehension measurement | Flashcard reveal, question filters; future mock viva scoring and personalized learning | **Partial** |

## Why the planet approach can be useful

The **galaxy** answers: “What big parts of this repository are present?” Clicking a **planet** answers: “Which files are classified into this part?” Clicking a **file star** answers: “What routes/imports/functions were statically detected?” Clicking a **viva evidence link** answers: “Show me where you got that claim.” This is a drill-down hierarchy with an explanatory purpose, not decoration.

## Hard product constraints

1. Never invent a dataset, model-training result, RAG retrieval step, authorization check, test pass or deployment.
2. Never imply a complete architecture has been verified when there are only import lines.
3. Never auto-run hooks or scan source from an unrelated project on install.
4. Never depend on the learner knowing graph theory, ML vocabulary or advanced terminal commands.
5. Never require a hosted app for the primary report.
6. Never turn the output into an unusable 3D toy: every view must have a clear action that supports learning.

## What works in 0.2.0

- Offline HTML planet clusters, globe rotation, zoom and module selection.
- Interactive import architecture with pan/zoom and accessible module inspector.
- Static reference trail flowchart, tree/treemap explorer, category keymap, Q&A lab.
- Safe source-based color cue sampling, without reading raw source into the browser.
- Existing evidence-based core question bank, user supplied PYQs and optional cloud answer rewording.
- Both Codex and Claude skills and approval-gated optional Claude reminder hook.

## What remains nontrivial

**Real dataflow:** following a UI click through a frontend fetch call, backend handler, service method, database query and response needs framework-specific and/or runtime tracing. This version does **not** implement those verified traces.

**ML deep audit:** finding a `fit()` marker is insufficient to reconstruct training and evaluation; the agent must verify scripts, data splits, seeds, weights, loss curves, metrics, dataset license and actual pipeline executions.

**Visual equivalence:** source CSS colors are not enough to understand layout, spacing, typography and component conventions. The current adaptation is color-based. To inherit the full design language, a project needs explicit design tokens and a guarded adapter.

**3D depth:** the current planetarium uses a 2D Canvas with projected 3D sphere points, not Three.js or a literal 3D Earth texture. It is intentionally zero-dependency and offline.

## Success metrics for future work

- Percentage of visible links with an inspectable source `file:line` and zero fabricated edges.
- Beginner ability to point to the correct code path after exploring the page (measured through unfamiliar viva follow-ups).
- False-positive rates for training, dataset provenance, auth and RAG.
- File-browser accessibility and keyboard coverage, including screen readers.
- Rendering time / responsiveness at 50, 200 and 400 indexed files.
- How often the user clicks evidence rather than just reading generic advice.

**Verdict:** The interactive idea is stronger than a PDF-only product, but only if the representation is honest, testable and usable. Attractive false topology would actively make a student's viva performance worse.
