# Questions and Concept Teaching Strategy — Mercy Studio

## Why HTML changes the teaching approach

In the PDF-only version, learners could memorize canned answers without understanding where they came from. The interactive version links **question → simple answer → concept → cited file → visual location in the project**. Follow-up learning is possible without switching documents.

## Q&A content contract

Keep each item in `mercy-evidence.json` using the existing schema:

- `id`, `category`, `difficulty`, `question`
- `answer`: 1–3 short, accurate sentences, ideally a response that could be spoken aloud in a viva.
- `explain_like_im_10`: a plain-language definition or real-world analogy, not an invented project claim.
- `evidence`: precise, existing `path:line` references, if available.
- `status`: supported code clue vs not verified (a citation never proves runtime deployment or correctness).
- `verify_next`: one action to confirm missing claims.

Question categories are generated from current scanner evidence: Start here, Architecture, Data, AI/ML, Security, Quality, Deployment, and so on. **Do not display a subject in the mind map as a confirmed implemented feature simply because its questions exist.** User-supplied PYQs should be included but not represented as university-authenticated.

## The most important evaluator attacks to prepare for

1. “Did you really train the model? Show your training script, checkpoints and logs.”
2. “Where did the dataset come from? Can you show it and explain its license?”
3. “You say RAG. Which function retrieves data, and where is it inserted into the model prompt?”
4. “Show the exact backend API that handles this button.”
5. “Show a real database schema and one query.”
6. “Where does authentication happen, and can you demonstrate a protected route?”
7. “What module imports this component? Does it actually run?”
8. “What tests passed? Show the command and result.”
9. “Where is the app deployed? Show the running service, not a README claim.”
10. “What fails when the database or model endpoint is unavailable?”

## Question Lab behaviors

- Filter by category and search text.
- Show/hide all answers or one card to practice memory recall.
- Click `file:line` source text to locate the file inside Mercy's map.
- Mark uncertainty clearly with “Not verified”.
- Teach with first-principles definitions, not dense engineering jargon.
- Encourage a spoken mock viva one question at a time when invoked in Codex or Claude.

## Agent refinement loop

After generating default content, the coding agent may inspect critical code paths **within the user's approved scope**, verify citations, write a complete question patch, run `mercy review --project . --input mercy-output/mercy-evidence.json --review mercy-output/review.json`, then `mercy render --input mercy-output/mercy-evidence.json` to refresh the HTML. It must not synthesize fake evidence or add a claim merely to make the graphic look full.
