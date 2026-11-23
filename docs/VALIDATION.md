# Native-agent foundation — 2026-11-23

Current validation:

- 11 standard-library unit tests pass: source context bounds/redaction, blocked traversal and symlinks, proof validation, complete review merge, source inventory/hash changes, legacy snapshot rejection, atomic failure recovery, empty source, and CLI context → review → render.
- 16 existing Python checks pass when invoked with temporary directories. Pytest is unavailable here; the optional ReportLab/PDF check remains skipped.
- 5 Node UI logic tests pass against a DOM double: mind-map expansion/answers/citations, stale-filter recovery and inert text, empty reports, pan/zoom/fit, and architecture pointer selection.
- Codex skill validator passes. Packaged/source/installed instructions match for both hosts; both YAML frontmatters parse. Skills installed locally without hooks.
- Regenerated sample notebooks and public demo contain no planet/canvas code. Generated payload JSON and JavaScript syntax checks pass.
- Fresh host-session skill discovery, actual host-driven behavioral benchmarks, rendered desktop/mobile layout, real gestures and screen-reader behavior have not been verified. The earlier browser local-file policy block remains; it was not bypassed.

Run the dependency-free new checks:

```bash
python3 -m unittest discover -s tests -p test_agent.py -v
node --test tests/studio_ui.test.cjs
```

The records below are historical and do not describe current UI behavior.

---

> Historical record of the supplied implementation. Current native-agent behavior is documented in README.md and docs/ARCHITECTURE.md.

# Validation — Mercy 0.2.0

## Required commands

```bash
python -m pytest -q
python -m mercy prepare --project examples/mini-rag --out output-example
python -m mercy render --input output-example/mercy-evidence.json
python -m mercy prepare --project examples/mini-rag --out /tmp/mercy-test --pdf
```

## Automated coverage

- Misleading RAG README does not imply retrieval or training proof.
- Secret filenames are skipped, redaction remains, symlinks are not followed.
- Import and HTTP-route references include correct source lines.
- Default CLI output creates offline HTML + Markdown + evidence + architecture and **no PDF**.
- `--pdf` creates the optional legacy PDF.
- `render` rebuilds HTML after evidence JSON is edited and rejects nonexistent evidence refs.
- Project color tokens are detected from safe local hex values where possible; fallback remains available.
- HTML payload escapes malicious HTML/script-breakout fragments and does not include external remote assets.
- Planet clusters only exist for roles with indexed files; arcs only match real edges.
- Codex and Claude skill installation and the optional read-only hook work.

## Browser acceptance checks (optional Playwright + Chromium)

Use a local HTML string in Chromium if the browser sandbox blocks `file:///` navigation. Test:

1. Open the sample HTML; verify no page errors, visible canvas, project title and question counts.
2. Click first cluster; verify `U.focus` changed and the file sphere is shown.
3. Drag a selected planet; verify yaw changed. Use scroll/+ buttons; verify zoom changed. Use back button; verify galaxy view restored.
4. Open Questions and search `RAG`; verify filtered Q&A cards appear.
5. Open Directory Atlas; click a folder tile then a file tile; verify the inspector updates.
6. Open Architecture; verify the number of graph nodes equals indexed files and graph arrows equal real import edges.
7. Open Flow Tracer; confirm every visible path can be sourced from an import chain, and is labelled a reference trail.
8. Open Concept Keymap; click a topic and confirm linked questions appear.
9. Repeat key interactions at ~390px viewport; verify no console errors and basic controls remain reachable.

## Unverified things (do not claim otherwise)

- Every real codebase/parsing language supported, no false positives possible, real backend behavior, deployment uptime, or model correctness.
- Full keyboard/screen-reader WCAG audit has not been completed.
- Thorough performance stress benchmarks on repos with many hundreds of files.
- Cloud API rewriting in this environment: API credentials and permission were not supplied.
- Full visual cloning of an existing project.

Document actual test results and sample screenshots separately in the release summary. Do not quietly turn planned checks into passed claims.

## Actual build record — 2026-11-23

- Automated Python suite: **17 passed**.
- Browser interaction smoke on synthetic five-role demo: **passed**; no page exceptions or external requests; selected planet rotation, directory expansion, file inspector, question search/reveal, keymap and static architecture nodes verified.
- Responsive smoke at 390px: **passed**, no body-level horizontal overflow.
- Built and installed wheel: **passed**, standalone HTML asset and both agent skills packaged; CLI generated HTML with empty runtime dependencies list.
- Optional legacy PDF: **passed** with ReportLab installed in the test environment.
- `file://` browser open: **not testable in the sandbox** (administrator block). The generated HTML was rendered with `set_content` instead. Opening the file locally remains the intended distribution method.


## Notebook redesign — 2026-11-23

The prior build record above describes the supplied version, not a fresh browser run.

- 16 existing Python checks passed by invoking their test functions with temporary directories, including CLI prepare/render, injection escaping, evidence preservation and theme handling. Pytest is not installed and was unavailable in the offline cache.
- Optional PDF test skipped: ReportLab is unavailable. PDF generation is outside this redesign.
- Seven Node tests pass with `node --test tests/studio_ui.test.cjs`. They execute template JavaScript with a DOM double: question branches and citations, retained focus, stale filter recovery, inert question text, map zoom/fit/pan, architecture selection after pointer capture, interpolated planet selection, import references, file lists, settled pause, reduced motion and empty/single-cluster reports.
- Regenerated galaxy and mini-rag HTML from existing evidence. The source template and shared interactive demo use the same UI.
- Local-file preview was rejected by the browser URL policy. No workaround was attempted. Desktop/mobile screenshots, real pointer gestures and screen-reader behavior remain unverified for this redesign. Existing preview images belong to the previous design.
