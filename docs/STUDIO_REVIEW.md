# Generated notebook review — 2026-11-25

Scope: source review of the CLI → scanner → question bank/review → atlas → offline HTML pipeline. Findings below are source-supported; user impact is an assessment, not a measured usability result. Runtime, browser layout, assistive technology and external-service behavior require separate verification.

## Assessment

Mercy's strongest design choice is the separation between static evidence and host-agent reasoning. Its main product weakness is the distance between those two steps: a standalone scan can produce a large, polished notebook before its answers explain the actual project. Better information architecture makes that gap easier to see and improves access to the evidence already collected. It cannot replace source investigation.

The generation path is `mercy/cli.py:149` → `mercy/scanner.py:146` → `mercy/questions.py:33` → `mercy/studio.py:199`. The separate reviewed-answer path is `mercy/agent.py:195`. These references establish implementation structure; they do not establish that every supported language or host integration works.

## Highest-impact findings

| Priority | Finding and evidence | Impact | Disposition |
|---|---|---|---|
| High | `make_questions` seeds a generic purpose and generic frontend/server workflow (`mercy/questions.py:53`, `mercy/questions.py:69`). AI/ML questions are appended unconditionally (`mercy/questions.py:126`). `prepare` exports that bank directly (`mercy/cli.py:150`). | Question count can look like analysis depth even when the central explanation remains unfinished or the topic does not apply. | The guided host workflow now seeds ten project topics and presents one bounded task at a time. Legacy starter generation remains compatible; source investigation is still required. |
| High | `add` assigns supported status whenever a proof list is present (`mercy/questions.py:36`). Some generic answers attach broad technology or symbol references (`mercy/questions.py:73`, `mercy/questions.py:94`). `validate_questions` checks schema and citation bounds, not whether prose follows from source (`mercy/agent.py:89`). | A valid citation can be mistaken for semantic verification, a successful test or completed review. | UI calls the state source cited / static evidence, and explicitly separates evidence counts from accuracy and review completion. Semantic checking remains the host's responsibility. |
| Medium | The previous guide offered generic navigation steps; the map and question grid carried the answers. `mercy/assets/studio.html:58` now contains the replacement guide. | Readers had to discover where the explanation was and assemble it across unrelated views. | Added a project brief, chapter contents, full answer reader, sequential navigation and one-column viva reading. Same question data drives the brief, map and guide. |
| Medium | Scanner records symbols and framework hit locations (`mercy/scanner.py:197`, `mercy/scanner.py:216`), but the old atlas truncated symbols and stripped framework evidence. | Collected information disappeared before the reader could use it. | Atlas preserves scanner-bounded symbols/imports and exports framework citation metadata (`mercy/studio.py:155`, `mercy/studio.py:186`). Inspectors display symbols, routes, imports, incoming references and selected citation lines. |
| Medium | Warning display previously capped notes at six and follow-up checks lived inside individual answers. | Important omissions could remain invisible while a diagram looked complete. | All scanner notes and per-answer next checks are available in expandable Project Guide references. Evidence-level filters help isolate unverified answers. |
| Medium | Framework and signal matching covers every indexed code file (`mercy/scanner.py:210`); discovery does not distinguish product code, examples and tests (`mercy/scanner.py:63`). | A sample or test can contribute a technology clue that does not describe the primary product. | Technology matches are shown with their file/line locations. No production-stack claim is made. Scope-aware signal extraction remains future scanner work. |
| Medium | `_local_imports` handles a limited candidate set (`mercy/scanner.py:82`); Flow/Import Trails takes the first unseen edge (`mercy/assets/studio.html:163`). | Aliases, re-exports and package layouts may be missed; an import trail is not a function trace or complete traversal. | Existing static-import limits remain explicit. No new runtime or architectural-tier claims. |

## What the redesign changes

1. **Orient:** title and counts occupy less space; the first answer and its evidence appear before the map.
2. **Read:** Project Guide offers a table of contents and one complete explanation, with previous/next navigation.
3. **Inspect:** citations preserve their line numbers; file details expose the available metadata and both directions of resolved imports.
4. **Check:** every scanner note and recorded answer follow-up is accessible together; evidence counts explain their limits.
5. **Practise:** a single-column question list supports category/evidence filtering, source-path search and accessible answer toggles.
6. **Reference:** technology clues, coverage and glossary have deliberate homes instead of competing with the primary lesson.

The black-and-white teacher/notebook identity, default Mind Map, six destinations, embedded assets, evidence JSON edit/render loop and Markdown companions remain part of the design. No new dependencies or services are introduced.

## Strengths to preserve

- HTML payload escaping handles script-breakout delimiters before embedding (`mercy/studio.py:206`); labels are built with text nodes in the template (`mercy/assets/studio.html:103`).
- Review validates complete question patches, rejects changed source fingerprints and replaces evidence atomically (`mercy/agent.py:195`).
- Discovery excludes secret-prone filenames and symlinks; bounded context redacts sensitive-looking lines (`mercy/scanner.py:51`, `mercy/scanner.py:63`, `mercy/agent.py:16`). These controls reduce exposure; they are not a universal secret detector.
- The normal pipeline is local; the optional remote rewrite is a distinct explicit flag (`mercy/cli.py:154`, `mercy/llm.py:12`).
- `render` accepts edited answer JSON and validates references against its saved scan (`mercy/cli.py:120`). It is a snapshot rebuild, not a fresh scan or runtime check.

## Remaining limits and next priorities

1. Improve the host-reviewed answer bank before adding more default prompts. Cover actual purpose, entry command, key modules, one source-traced workflow, validation, errors, dependencies and limitations. Keep generic definitions in reference material.
2. Guided workflow now records submitted question digests separately from source-cited status. This is editable progress bookkeeping, not reviewer identity, independent review or proof that the prose is true.
3. Separate example/test signals from primary product signals if stack accuracy becomes a priority.
4. Large SVG graphs still need aggregation and performance work. Separate node rows prevent overlap, but hundreds of files can require substantial panning.
5. Palette refresh now reuses the safe source reader and skips missing, outside or symlinked styles (`mercy/studio.py:86`). Rendering without `--project` still rebuilds a saved snapshot rather than refreshing source evidence.
6. Actual desktop/mobile pixels, pointer gestures and screen-reader behavior remain unverified until a permitted browser preview is available. Local-file navigation was rejected by browser policy during this review; no workaround was attempted.

## Validation boundary

Regression checks were added for chapter navigation, complete answer/citation preservation, source search, evidence filters, reveal accessibility state, complete warning visibility, symbol inspection, empty banks, old atlas metadata and framework citations. See `tests/studio_ui.test.cjs` and `tests/test_studio.py`.

Syntax and static artifact inspection results are recorded in `docs/VALIDATION.md`. Existing HTML examples were refreshed from saved evidence by file operations without executing Mercy. Runtime checks and project tests have not run; repository instructions require explicit authorization for those actions.
