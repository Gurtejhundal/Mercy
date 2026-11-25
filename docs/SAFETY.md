# Mercy Studio 0.2.0 — Safety, Privacy, and Honest Graphs

## Threat model

Untrusted repositories can contain malicious source text, fake architecture claims, prompt-injection comments, private paths, tokens, API keys and secrets. A standalone HTML report can leak metadata if shared carelessly, or execute injected script if generated unsafely.

## Read-time protections

- `scan_project` reads regular files only, within an explicit repository directory; it does not follow symlinks.
- Standard dependency/build/cache directories and secret-prone filenames are excluded; `.env`, `.pem`, `.key`, `.db`, notebooks and several others are excluded.
- Global file-count/read-byte limits apply. Scanner may skip files; never claim full coverage.
- No execution, imports, training, tests, network fetches or database connections to the target project.
- Source excerpts with credential-like patterns are redacted.
- Some sensitive material could still appear in non-standard filenames, route names, symbols or framework names. **Review the report before sharing.**

## Native-agent tools

`context` operates on the scanner's indexed source paths only, rejects traversal/symlink paths, caps excerpts and redacts sensitive-looking lines. Returned repository text is untrusted data. Redaction is conservative pattern matching, not a guarantee that arbitrary source is free of private data. The selected Codex/Claude host receives the context under its own privacy settings.

`review` accepts only a `questions` patch, validates IDs, proof labels and citation bounds against the scan and current files, and rejects source inventory or fingerprint changes. It cannot rewrite scan metadata. The evidence file is replaced atomically only after validation. Prepare/render also stage evidence JSON beside its destination and replace it atomically; a failed write preserves the prior evidence file. Other report companions are separate writes. Hashes do not prove an answer's semantics; the host must inspect and reason about each claim.

## HTML output protections

- No remote CSS, JavaScript, fonts, CDN, APIs, workers or network calls in the default generated Studio.
- No persistent browser storage. Answer reveal/filter/session state is ephemeral.
- The embedded report payload is placed into an `application/json` script tag with HTML-parser-sensitive characters safely escaped.
- The viewer uses `textContent`, `createElement` and `createElementNS`; it does not insert scanner-derived strings as raw HTML or eval source strings.
- Project colors are selected from validated six-digit hex values only; arbitrary CSS declarations from the repository are **not** inserted into the report.
- Browser CSP/sandbox are not presently enforced by the output; the important defensive properties are inert JSON and safe DOM construction. A future release should consider a strict CSP while preserving single-file usage.

## Honest topology contract

1. Node label = scanned source path (or data-file candidate).
2. File-role classification = **heuristic**, not a verified frontend/backend/AI boundary.
3. Edge = scanner-resolved local **import**, with source file and line. A is not claimed to call B at runtime.
4. Route = route **declaration** in code, not proof of a mounted endpoint or successful request.
5. Import Trails = a *dependency trail*, not a real user-click or data-flow execution trace.
6. A model import, `fit()` marker, CSV file, retrieval-related term or deployment manifest cannot prove the feature works.
7. If code evidence is absent, explain that the feature was *not established*, rather than saying it definitely does not exist.

## Permissions and agent integrations

- Skill installation changes only selected local skill file paths unless optional `--hooks` is explicitly requested.
- Claude `SessionStart` hook writes a short **read-only reminder**; it does not scan or run code. The host/user must approve it.
- Never ask to skip permission prompts or bypass tools.
- `--ai` (OpenAI API-assisted rewriting) requires explicit user permission. Its current metadata-only design does not equal zero privacy risk; do not invoke automatically.

## Sharing checklist

1. Review paths, function names and route names for customer/personal data.
2. Check whether model/training, RAG and data claims are explicitly verified or still unknown.
3. Confirm every edge is based on actual scanned imports; do not embellish diagrams with invented connections.
4. Confirm HTML opens offline and question cards do not produce any network requests.
5. Do not publish proprietary or campus/client material without authorization.
