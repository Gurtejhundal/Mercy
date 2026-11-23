# Interactive Atlas — Product and Interaction Specification

## Product

A source-grounded notebook accompanies Mercy's Codex/Claude coaching workflow. Opening the HTML requires no server, internet, model or provider key. All CSS, JavaScript and metadata are embedded. It opens on the Mind Map.

## Views

1. **Mind Map:** project → subject → question branches. Expand with click or keyboard, read answers and citations beside the map, pan blank space, zoom, fit and collapse. Study branches are not implementation claims.
2. **Study Guide:** technology clues, gaps and a guided study path.
3. **Architecture:** actual resolved imports, keyboard-selectable file nodes, pan/zoom and source metadata inspection. File roles are heuristic.
4. **Flow Tracer:** a declared route/file followed through up to seven static references, never a verified runtime pipeline.
5. **Directory Atlas:** accessible folder hierarchy, proportionate folder/file tiles and module inspection.
6. **Viva Questions:** search, filter, reveal answers, plain explanations, uncertainty and source citations.

Citation selection opens the architecture inspector. Escape returns to the mind map. Source filenames remain text, never injected HTML.

## Data model and design

`studio.py` converts the bounded scan and reviewed questions into files, heuristic role groups, import edges, routes, questions, glossary and warnings. Only populated groups appear. Group names do not imply deployed tiers. The notebook uses one light minimalist design; explicit safe theme tokens remain supported. See `DESIGN_SYSTEM.md`.

## Accessibility and performance

- Every section is available via ordinary buttons/navigation; canvas alternatives include a cluster list, file tree, filter lists and named graph nodes.
- Motion can be paused; OS-level reduced-motion is honoured.
- Bounded scan of 400 files by default; no vendor or secret directories; large maps require scrolling/panning.
- The HTML is self-contained. Interactions depend on modern Canvas, SVG and JavaScript, so the text Markdown report remains an alternative for older browsers or screen readers.
- For large real projects, SVG graph crowding is a known limitation. A future release needs node aggregation, virtualized file lists, search and incremental layout.

## Truthfulness acceptance tests

- A fake RAG claim in README does not establish a retrieval pipeline.
- A source dependency graph A → B exists only if scanner resolves that import.
- Files without an inspected role are placed in a heuristic default category; role confidence remains non-authoritative.
- A complete user→database flow must **not** be drawn unless independently verified.
- Page must open offline without `http`, `https`, CDN or external assets.
- Script-breakout strings in project labels must remain inert text.
