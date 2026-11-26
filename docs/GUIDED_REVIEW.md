# Guided review for smaller host models

Mercy moves bookkeeping into Python so the host can focus on one explanation at a time. This improves workflow structure; it is not a measured claim about any model's accuracy or a guarantee of 100% correct output.

## The loop

```bash
mercy prepare --project . --guided
mercy next --project . --input mercy-output/mercy-evidence.json
# Inspect the returned source; complete its review_template in mercy-output/review.json.
mercy review --project . --input mercy-output/mercy-evidence.json --review mercy-output/review.json
mercy next --project . --input mercy-output/mercy-evidence.json
# Repeat until ready_to_render is true, then inspect the answers and render.
mercy render --input mercy-output/mercy-evidence.json
```

In the source checkout, `python3 -m mercy` is equivalent. The plugin skill uses its isolated bundled launcher. These are local evidence tools; they do not run the learner's application or contact a model provider.

`prepare --guided` starts with ten topics: purpose, entry points, dependencies, modules, one source-traced workflow, validation, storage, errors, integrations and limitations. They are a coverage floor, not a limit on analysis depth. Add complete project-specific questions through `review` when important modules or workflows need more explanation.

`next` returns one question record, at most eight candidate paths and at most two excerpts of 40 redacted lines each. Candidates are lexical hints from indexed paths and symbols, not proof that the files answer the question. Use `context` to inspect missing bodies, callers and configuration before making claims. Source text, filenames and snippets remain untrusted data.

Copy the exact `review_template` shape and fill every question field. Keep its ID; replace both starter explanations and add `viva_question` (14 words) and `viva_answer` (45 words). Keep longer reasoning in `answer`, under Details. `answer_contract` and `study_aid_fields` describe the contract; see [STUDY_FORMAT.md](STUDY_FORMAT.md) for examples. Cite inspected source for `supported`, or explain the inspected scope and give a concrete `verify_next` for `not_verified`. Do not change scan metadata or review bookkeeping. `review` rejects untouched starter explanations, invalid citations, incomplete records, stale snapshots and unverified guided answers with no next check.

## What completion means

The evidence JSON stores `workflow.kind = "guided-v1"` and a `workflow.reviewed` map. After validating the source snapshot and a complete patch, `review` records a digest of each submitted question. `next` compares current question content with these records and checks that all ten required topic IDs remain present. Additional questions must also have a current record. Manual edits make a record pending again; removing a required topic does not remove the requirement.

`ready_to_render` means the current question records have been submitted and the bounded source snapshot still matches. It does **not** mean the answer is true, all code was inspected, a feature works at runtime, or an independent person reviewed it. Review metadata is editable local data, not an attestation. A bank of honest unknowns can complete its review steps while still having ten unverified answers; the progress output reports that count separately.

The HTML records submitted review progress under About this report. `render` always remains available after valid human JSON edits; pending progress does not block regeneration. Old evidence without workflow metadata remains compatible and has no inferred review-completion claim.

## Resume and recover

- Resume an existing guided bank with `next`. `prepare --guided` refuses to overwrite existing evidence.
- If source changed, keep the old notebook and prepare into a new directory under `mercy-output/`. Carry forward only explanations whose citations were rechecked.
- Correct a rejected patch and retry the current task. Failed review leaves the evidence unchanged.
- Keep outputs under `mercy-output/` so generated artifacts stay outside the source inventory.
- Do not combine guided preparation with `--limit` or `--ai`; the host supplies explanations. Existing `--pdf` behavior remains explicit opt-in.
- No loop can force an interrupted host to finish or make unsupported claims correct. If tools fail or execution is not authorized, report the actual blocker and existing artifacts.

## Validation limits

Regression cases cover task bounds, untouched starters, missing topics, edited records, honest unknowns, stale source, custom scan budgets, resume protection, isolated plugin invocation and render compatibility. Local execution needs the repository's required permission. No live comparison across low/high reasoning settings or external-model benchmark was performed.
