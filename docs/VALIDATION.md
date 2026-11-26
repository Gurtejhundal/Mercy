# Notebook information architecture — 2026-11-25

Audit and guided-review additions: source fixes cover import resolution, skipped import targets, safe palette refresh, literal answer preservation, atomic evidence writes and hook-setting validation. Guided regression cases cover bounded next-task packets, incomplete/edited/missing records, unverified-answer counts, source freshness, custom scan limits, resume protection and render compatibility. These new cases have not been run locally while execution permission is pending. No external-model benchmark or guarantee of model accuracy is claimed. Codex/plugin skill validators passed. Claude frontmatter parses as YAML; the generic Codex validator rejects its existing Claude-specific keys, so that validator is not claimed as a Claude-host check.

- Python source syntax parsing passed for the changed exporter and Python regression file. Node syntax checks passed for the template script and UI regression file. `git diff --check` passed.
- Existing mini-rag and galaxy HTML previews were refreshed by applying the new template to their saved evidence with standard-library file operations, without invoking Mercy. Their 49 and 52 answers were retained. `public/demo.html` matches the refreshed mini-rag preview.
- Static HTML inspection found no duplicate IDs, unresolved template markers or remote asset links in these three previews. Embedded atlas JSON parsed successfully.
- Added regression coverage for chapter navigation, complete answers and citation lines, warning visibility, symbol inspection, source-path search, evidence filters, answer toggle state, legacy atlas data, empty answer banks and framework citations.
- Project tests and CLI prepare/review/render execution were **not run**: explicit permission is required by this repository's instructions and has not yet been received. The added tests are not claimed to pass.
- Browser policy rejected local-file preview. No workaround was attempted. Desktop/mobile pixels, real gestures and screen-reader behavior remain unverified.

The records below describe earlier versions and are not fresh verification of this redesign.

---

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

## Viva guide redesign — 2026-11-25

Current local checks after the redesign:

- **59 Python checks passed**, one optional PDF test skipped because ReportLab is not installed. Thirty standard-library unittest cases ran directly; the thirty pytest-style functions ran through an isolated temporary-directory fixture harness (29 passed, one skipped). Pytest itself is not installed locally.
- **11 Node checks passed**: concise guide/default view, full notes behind Details, source-line inspection, ordinary wheel versus Ctrl+wheel/pinch handlers, decision/terminal shapes and branch labels, component nodes/import evidence, search/filter/rehearsal ARIA state, demos/folders, inert untrusted labels, scanner notes, and legacy/empty banks; plus the website checks.
- CLI preparation, validated review and render regenerated both bundled sample banks. Their source snapshots still match. The saved PeakCut bank was backed up and reviewed before regeneration: 18 short answers, maximum 31 words, six components, one cited upload flow and five demonstration steps. Original detailed answers remain in JSON and Details. The scanned PeakCut app/tests and external providers were not run.
- The exported example was copied to `public/demo.html`; source citations, embedded assets, local anchors and the no-network template checks passed. No PDF was generated.
- Skill frontmatter validation passed. No new dependency was introduced.

These are source, CLI and DOM checks. Browser local-file navigation was blocked earlier in this session; no alternate transport was used to bypass it. No fresh desktop/mobile pixel capture, physical trackpad/touch gesture check or full screen-reader audit was completed. Pinch handlers are checked as events, not calibrated hardware behavior. Source bounds and a completed review do not guarantee model reasoning accuracy.

## Marker identity, explorer and model sources — 2026-11-26

- Local standard-library suite: **31 cases passed**. Pytest-style function harness: **29 passed, one optional PDF case skipped** (ReportLab is not installed locally). Node: **12 checks passed**.
- The checks cover technology/model-source field validation, safe HTTPS resources, indexed locations, embedded technology marks, nested native disclosures, selected folder/file explanations, source-line selection and parent expansion, focused component dependencies, inert labels, rehearsal and the preserved flowchart gestures/shapes.
- The PeakCut report was backed up before editing. Its 18 short answers and workflow/demo data are retained. It now has seven technology/source entries, 99 file explanations and 16 folder descriptions. Two empty package-marker files use the explicit empty-source fallback. Model sources were traced in the local loaders and checked against upstream model cards/repositories; no model, provider or scanned application was executed.
- Logos are bundled static Simple Icons SVGs. Generated reports remain self-contained; external resources are only explicit links. The release wheel smoke now generates a report to verify its packaged assets.
- The browser again rejected access to the local report under its file-URL policy. No localhost server, alternate browser surface or other bypass was used. DOM checks do not establish physical gestures, screen-reader behavior or local pixel layout.

The published synthetic Galaxy sample was subsequently checked in the browser: marker typography and violet highlights rendered; nested `ui/components` expansion selected the correct right-hand explanations; a file selection displayed its reviewed purpose; the focused architecture drew direct dependencies without crossing unrelated components. This did not expose or run the local PeakCut application. Local-file access and physical gesture checks remain outside this browser evidence.

A follow-up keeps the desktop explorer stable on selection and returns the page to the top when changing sections. The local suites then passed **32 unittest cases and 13 Node checks**. Release/version metadata now checks that the current version has matching plugin manifests and release notes. The first release attempt built and smoke-tested the installed wheel successfully but stopped publishing because its notes file was missing; the notes and trigger are included in the follow-up.
