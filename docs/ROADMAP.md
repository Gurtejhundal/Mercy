# Mercy — native agent roadmap

## Working foundation

- Codex/Claude skills for focused codebase investigation, reviewed study notebooks and a one-question-at-a-time mock viva.
- Bounded local scan and redacted source context with exact line numbers.
- Review patches for replacing or adding project-specific questions; shared proof validation, source inventory/fingerprint checks and atomic writes.
- Offline mind map, import graph, reference trails, file browser and Q&A; Markdown and JSON companions.
- No separate model service or provider key for the native agent workflow. The host's model, privacy settings and permissions apply.

## Next improvements

1. Benchmark host reasoning against known codebases: misleading README claims, incomplete RAG, imported-but-unused libraries and failure paths. Current tool tests do not measure AI reasoning quality.
2. Refresh source snapshots while retaining only reviewed answers whose evidence is still current, with a reviewable comparison.
3. Add language/framework-specific source tracing that distinguishes import references, function calls and registered routes. Runtime verification stays separately authorized.
4. Improve large-map navigation and file filtering, then verify desktop/mobile layout and screen-reader behavior in a real browser.
5. Refine viva coaching from observed learner answers; progress persistence remains an explicit user choice.

## Boundaries

Mercy is a codebase understanding and viva coach. Application editing, command execution against the target project, model training, deployment and external publishing require separate requests. A citation is a source location, not proof that every sentence an AI writes is true.
