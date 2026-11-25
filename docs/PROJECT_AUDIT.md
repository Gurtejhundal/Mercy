# Project audit — 2026-11-25

What this repo does: Mercy gives Codex/Claude bounded source evidence and produces an offline project-study notebook. The host supplies reviewed explanations; the CLI scans, checks citations and renders artifacts. Assumed load: one person scanning a local repository, bounded to 400 discovered files and a 1.6 MB source-read budget by default.

Evidence level: source-supported. The cases below follow the inspected implementation. Regression cases have been added; local execution was not authorized during this audit, so these are not claimed as runtime reproductions or passing tests.

## Must fix — addressed in this change

1. **A failed evidence save could destroy reviewed answers** (`mercy/renderer.py:41`).
   - **What this is:** Prepare and render save the editable JSON used to rebuild the report.
   - **Problem:** The previous direct write truncated the destination before the write completed. A disk-write failure could leave the only reviewed evidence file incomplete.
   - **Fix:** Serialize first, stage beside the destination, flush and atomically replace. Preserve existing permissions and reject symlink destinations. Failure cases are covered in `tests/test_renderer.py`.
   - **If we skip it:** A failed regeneration can destroy the answers it was meant to preserve. This case is now guarded in source.

2. **Palette refresh could crash or inspect a path outside the project** (`mercy/studio.py:86`).
   - **What this is:** Optional theme sampling rereads stylesheet paths from the saved scan.
   - **Problem:** Removing a stylesheet between scan and render raised an uncaught file error at the size check. A manually edited snapshot could also name `../outside/style.css` or a symlinked directory.
   - **Fix:** Reuse the source reader's path, regular-file and symlink checks; skip secret-prone names; catch missing/unreadable files. Theme-config inspection also stays inside its error handler.
   - **If we skip it:** An optional visual hint can prevent notebook regeneration or cross the declared project boundary. Regression coverage is in `tests/test_studio.py`.

3. **Ordinary imports could disappear or point at unrelated files** (`mercy/scanner.py:82`).
   - **What this is:** The scanner resolves import names into local file links.
   - **Problem:** `from "./helper.js"` gained another extension during resolution, `import helpers` missed `helpers/__init__.py`, and `from . import answer` lost the submodule name. A bare JS package name such as `react` could incorrectly match a local `react.js`.
   - **Fix:** Handle explicit extensions, Python initializers and relative submodule names. Keep Python and JS extension candidates separate, and leave bare JS packages unresolved.
   - **If we skip it:** The HTML and Markdown can teach an incomplete or false dependency map. Regression cases are in `tests/test_mercy.py`.

4. **The raw report could link to a source file that was never read** (`mercy/scanner.py:234`).
   - **What this is:** Discovered paths and indexed source files are different sets when size/read budgets skip files.
   - **Problem:** `app.py` importing an oversized `large.py` could create a raw edge to `large.py`, even though it was absent from the source inventory. HTML later filtered the edge, while counts and Markdown could retain it.
   - **Fix:** Resolve imports only against successfully indexed source paths.
   - **If we skip it:** Different companions disagree about the same scan. An oversized-target regression is in `tests/test_mercy.py`.

5. **Asset embedding could rewrite the actual answer text** (`mercy/studio.py:199`).
   - **What this is:** The exporter replaces placeholders with its embedded font and teacher image.
   - **Problem:** An answer containing literal `/* MERCY_MASCOT */` or `/* MERCY_NOTEBOOK_FONT */` was replaced with base64 asset data after it entered the JSON payload.
   - **Fix:** Complete trusted asset substitution before inserting the escaped question data.
   - **If we skip it:** Human-edited answers do not survive render exactly. A literal-marker regression is in `tests/test_studio.py`.

6. **Malformed hook settings produced a traceback** (`mercy/cli.py:50`).
   - **What this is:** The explicitly requested Claude hook installer merges settings into existing JSON.
   - **Problem:** Valid JSON such as `{"hooks":[]}` or `{"hooks":{"SessionStart":"bad"}}` reached dictionary/list methods on the wrong type.
   - **Fix:** Validate both nested types and raise a readable CLI error while leaving the settings file unchanged.
   - **If we skip it:** Installation fails with an internal error instead of telling the user which settings need repair. Regression cases are in `tests/test_mercy.py`. Skill/hook files may already have been installed before settings validation; installation is not a multi-file transaction.

7. **Custom scan limits prevented later review** (`mercy/agent.py:118`).
   - **What this is:** Review rescans source to check its saved inventory and fingerprints.
   - **Problem:** A bank prepared with `--max-files 1` was checked against a default 400-file scan, so a project with two files was always rejected as changed.
   - **Fix:** Record the scan limits and reuse them when checking the snapshot. Legacy evidence keeps the original defaults.
   - **If we skip it:** Incremental review cannot finish for deliberately bounded scans. A custom-budget regression is in `tests/test_agent.py`.

## Should fix — remaining limits

8. **The JS parser can mistake example text for an import** (`mercy/scanner.py:44`).
   - **What this is:** JS/TS import extraction uses a regular expression over source text.
   - **Problem:** `const sample = 'from "./helper.js"';` can look like an import if that local file exists. Side-effect imports such as `import "./setup.js";` are also outside the current pattern. Extension resolution fixes do not solve parsing.
   - **Fix:** Use a language-aware parser, with explicit coverage for strings, comments, side-effect imports and re-exports, before presenting JS graphs as complete.
   - **If we skip it:** JS graphs remain partial static clues that need source review. This audit does not certify parser completeness.

9. **Companion files can come from different render attempts** (`mercy/cli.py:130`).
   - **What this is:** JSON, Markdown, HTML and optional PDF are written in sequence.
   - **Problem:** A failure while writing HTML can leave newly saved evidence/Markdown beside an older HTML file. Atomic evidence saving protects answers, but does not make the whole export a transaction.
   - **Fix:** Stage the complete companion set before publishing it and expose a shared generation identifier. Until then, use `render --out` with a fresh directory when preserving a prior complete report matters.
   - **If we skip it:** After an export error, users must regenerate before treating all companions as one snapshot.

## Product limits, not runtime guarantees

`prepare` is a deterministic starter generator, not completed project analysis (`mercy/questions.py:53`). Its generic questions include AI/ML material even for projects where that topic may not apply. The host must replace irrelevant answers with inspected explanations through the documented review workflow. The redesigned opening brief, chapters, evidence labels, source inspector and verification checklist expose the saved analysis more clearly; they do not manufacture missing evidence. See `docs/STUDIO_REVIEW.md` for the information-architecture review.

Citation validation checks paths, line bounds and source fingerprints; it cannot prove the prose is true (`mercy/agent.py:89`, `mercy/agent.py:195`). No model training, dataset provenance, endpoint behavior, authentication, deployment or accuracy was verified by this audit. New guided bookkeeping records submitted answers and detects later edits, missing topics and untouched starters. It does not certify answer truth; see `docs/GUIDED_REVIEW.md`. SVG performance at hundreds of files and real assistive-technology behavior remain unmeasured.

Verdict: seven concrete failure cases have source fixes and regression coverage. JS parsing and multi-file export consistency remain documented work.

Lean: removed two unused declarations; added no dependencies.

Not checked: local project tests/CLI execution pending explicit permission, real browser interaction/layout, screen readers, optional PDF output, optional external AI calls, fresh-host plugin discovery and deployed-service behavior. Existing CI results must be checked against the final remote commit separately.
