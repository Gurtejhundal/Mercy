# Native host-agent foundation

- Workspace root is now the runnable Python project; the supplied reference audit remains under `mds`.
- Removed the planet UI and renderer. Reports open on the mind map and citations open the architecture inspector.
- Codex/Claude skills now guide source investigation, reviewed notebook generation and adaptive mock viva coaching using the host model.
- Added `context` for bounded, redacted source excerpts and `review` for validated atomic question updates. Shared render validation rejects invalid proof labels, duplicate IDs, out-of-range/boolean line numbers and unsupported claims without citations.
- Scan fingerprints reject stale reviews, including same-length source changes. Empty source files no longer produce fabricated line-one references.
- Added native-tool tests and updated UI tests. Current evidence is recorded in `VALIDATION.md`.

---

> Historical record of the supplied implementation. Current native-agent behavior is documented in README.md and docs/ARCHITECTURE.md.

# Mercy Studio v0.2.0 — Release Notes

## Breaking UX change

**Before:** `mercy prepare` produced a PDF first.

**Now:** `mercy prepare` produces a **standalone interactive HTML Studio** first. The PDF is optional via `--pdf` with the `pdf` install extra (`pip install -e '.[pdf]'`). Evidence JSON, Markdown and the static architecture map remain available.

## Major additions

- Planetary Atlas: all populated source-derived groups as separate planets; click a group to inspect its rotating projected-3D file sphere, drag to rotate, zoom and click file markers.
- Architecture network: live SVG of resolved local source imports; pan, zoom, keyboard node activation and inspector.
- Flow Tracer: route/file selector that shows an honest static dependency path, with sources and a clear warning that it is not runtime data flow.
- Directory Atlas: expandable file tree and folder->file treemap with local file metadata inspection.
- Concept Keymap: interactive categories leading into the viva Q&A lab, plus child-friendly definitions.
- Viva Question Lab: search, category filtering, show/hide answers, and evidence-to-module navigation.
- Project-theme support: safe literal hex palette sampling and optionally an explicitly supplied `mercy-theme.json` with validated colors, radius and restricted fonts.
- Zero required runtime dependencies for the default offline HTML; optional `reportlab` only for PDF.
- Updated `README.md`, `AGENTS.md`, platform skills, `docs/ARCHITECTURE.md`, `docs/CONCEPT_AUDIT.md`, `docs/INTERACTIVE_ATLAS.md`, `docs/DESIGN_SYSTEM.md`, `docs/QUESTION_STRATEGY.md`, `docs/SAFETY.md`, `docs/ROADMAP.md`, `docs/VALIDATION.md`.
- Added a synthetic `examples/galaxy-demo/` showing all five potential role groups. The repo is **not** a functioning product or trained model.

## Verification performed

- `python -m pytest -q`: **17 passing**.
- Browser smoke check with Chromium + Playwright: generated DOM rendered, five role planets detected, pointer-drag rotation modified yaw, tree folder->file navigation updated inspector, source graph nodes loaded, flow step selection updated inspector, keymap filtered questions, hide answers worked, **no console page errors or unexpected browser requests**.
- Mobile viewport 390×844: `document.body.scrollWidth` matched viewport width; no horizontal overflow in tested view.
- Built and installed a `mercy-viva==0.2.0` wheel with **no dependencies**, verified that the HTML template and Claude/Codex skills were present, then generated an HTML report from the installed wheel.
- Generated sample HTML from `examples/mini-rag` and `examples/galaxy-demo`. Legacy optional PDF also generated successfully with ReportLab available.

## Still limited

- Browser navigation using `file:///` was blocked by this testing environment's administrator policy. Browser smoke testing used `set_content()` with the exact generated HTML. The page contains all CSS/JS/data inline and does not fetch remote resources, but local filesystem navigation was not separately exercised here.
- Planet drawing uses projected 3D geometry on 2D Canvas, not native WebGL/Three.js, and its file grouping is **heuristic**.
- Dependency arrows indicate **imports**, not runtime function calls or network requests. Full end-to-end traced architecture remains a future milestone.
- The project visual style is adapted using allowed tokens, not exhaustively cloned from an arbitrary product UI.
- No full WCAG accessibility assessment, large-codebase stress benchmark, or live external AI request was performed.
