# MERCY | galaxy-demo | Viva Preparation

> Evidence-first preparation. A source reference shows a code clue, not proof that a feature works in production.

## Repository scan

- Files read: 10
- Data-shaped files: 0
- Routes detected: 1
- Resolved local imports: 5
- Tech markers: FastAPI

## Module connections

- `infra/settings.py` -> `server/main.py` (import `server.main`)
- `intelligence/pipeline.py` -> `intelligence/embed.py` (import `intelligence.embed`)
- `server/main.py` -> `intelligence/pipeline.py` (import `intelligence.pipeline`)
- `server/main.py` -> `storage/db.py` (import `storage.db`)
- `ui/components/App.jsx` -> `ui/components/StatusBadge.jsx` (import `./StatusBadge`)

## Important verification gaps

- No direct training-loop evidence found; do not claim this model was trained here.
- No dataset files or loaders located in the inspected source.

## Start here

### Q01. What is this project?

**Short viva answer:** The repository is called galaxy-demo. The exact business goal must be confirmed from the owner or documentation; the code scan alone does not prove user outcomes.

**Explain simply:** First explain the problem it solves, then who uses it, then what happens when they click a button.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Write a one-sentence problem statement and demonstrate the main feature.

### Q02. What is your project tech stack?

**Short viva answer:** Found these technology signals: FastAPI. A detected import does not prove a service is configured or used in production.

**Explain simply:** A tech stack is your toolbox: what builds the screen, what handles requests, and where data lives.

**Evidence:** server/main.py:1

**Proof level:** supported

**Verify:** Verify versions and running services in package manifests and deployment.

### Q03. Show me where the application starts.

**Short viva answer:** Likely starting files: server/main.py. Confirm the start command before claiming any one is the actual entry point.

**Explain simply:** An entry point is the front door. It is the first file started when the app runs.

**Evidence:** server/main.py:1

**Proof level:** supported

**Verify:** Check README scripts or package.json and run the project.

### Q04. Show the frontend and backend directories.

**Short viva answer:** Files include: README.md, mercy-theme.json, infra/settings.py, intelligence/embed.py, intelligence/pipeline.py, server/main.py, storage/db.py, ui/style.css, ui/components/App.jsx. A folder name alone cannot prove which part runs on the server.

**Explain simply:** Frontend is what users see. Backend is what responds to requests and talks to data.

**Evidence:** README.md:1, mercy-theme.json:1, infra/settings.py:1

**Proof level:** supported

**Verify:** Trace one UI request to one server handler.

### Q05. Explain your project workflow from opening the app to getting a result.

**Short viva answer:** Observed 1 route declarations and 5 local module links. A full end-to-end workflow is not verified by static analysis alone.

**Explain simply:** Tell the story: user -> screen -> request -> server -> database/model -> answer -> screen.

**Evidence:** server/main.py:6

**Proof level:** supported

**Verify:** Run the app, click the main feature and watch its network requests.


## Architecture

### Q06. Show your software architecture.

**Short viva answer:** Likely technology components are FastAPI. Use the import map and actual route handlers to draw confirmed arrows.

**Explain simply:** Architecture is a map of the rooms in your application and the doors between them.

**Evidence:** server/main.py:1

**Proof level:** supported

**Verify:** Trace at least one complete user action and draw only confirmed connections.

### Q07. Which module calls which other module?

**Short viva answer:** Local references found: infra/settings.py -> server/main.py; intelligence/pipeline.py -> intelligence/embed.py; server/main.py -> intelligence/pipeline.py; server/main.py -> storage/db.py; ui/components/App.jsx -> ui/components/StatusBadge.jsx

**Explain simply:** An import means one file can use code from another. That is not always a runtime call.

**Evidence:** infra/settings.py:1, intelligence/pipeline.py:1, server/main.py:2

**Proof level:** supported

**Verify:** Follow the imported function in the actual call sites.

### Q08. What are your API endpoints?

**Short viva answer:** Found routes: /status in server/main.py

**Explain simply:** An endpoint is a door the frontend knocks on to ask the server for something.

**Evidence:** server/main.py:6

**Proof level:** supported

**Verify:** Inspect router registration and use a real HTTP request to verify these routes.

### Q09. What happens when the frontend sends a request?

**Short viva answer:** Found HTTP handlers in server/main.py

**Explain simply:** A request is like ordering food: the screen asks, the server prepares, then sends a response.

**Evidence:** server/main.py:6

**Proof level:** supported

**Verify:** Open browser DevTools Network and trace one request to the backend.

### Q10. What is the difference between frontend and backend?

**Short viva answer:** Frontend builds the screens that people use. Backend handles server-side logic, data and API requests. Your exact code split still requires tracing.

**Explain simply:** Frontend = shop counter; backend = kitchen.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Identify two files from each side, if both exist.

### Q11. Where are business rules written?

**Short viva answer:** Look for functions that validate inputs, calculate values, or decide outcomes. Static import names cannot prove which functions contain the core rules.

**Explain simply:** Business logic is the rulebook, not the paint on the screen.

**Evidence:** intelligence/embed.py:1, intelligence/pipeline.py:3, server/main.py:7

**Proof level:** supported

**Verify:** Follow one important function from input to return value.

### Q12. What breaks if a service is down?

**Short viva answer:** Failure handling and deployed dependencies are not confirmed by static scanning.

**Explain simply:** If the kitchen is closed, the shop should tell the customer instead of crashing.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Disconnect the API or database in a test environment and record the result.


## Data

### Q13. Where is your database?

**Short viva answer:** No database connection was proven in the inspected code.

**Explain simply:** A database is the app’s organized notebook. An SDK import is not the same as a running database.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Locate connection config, schema, migrations and deployment provider.

### Q14. Show your database tables or collections.

**Short viva answer:** The scanner does not execute migrations or query databases, so it cannot establish the live schema.

**Explain simply:** Tables are like named pages in a notebook; columns are the headings.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Open migrations/schema and compare with the actual database.

### Q15. How does data travel through your system?

**Short viva answer:** The scan located 1 routes, 0 data-shaped files and 5 module links. These are clues, not a verified complete data pipeline.

**Explain simply:** Follow one piece of data from where it enters until you see the result.

**Evidence:** server/main.py:6

**Proof level:** supported

**Verify:** Trace and document one real input all the way through.

### Q16. How do you validate user input?

**Short viva answer:** Input validation is not established by a basic repository scan.

**Explain simply:** Validation is checking a form before accepting it, like rejecting an impossible age.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Show the exact schema or condition and test invalid input.

### Q17. How do you handle errors and bad requests?

**Short viva answer:** Error handling must be checked in actual route handlers and through tests.

**Explain simply:** When something fails, the program should say what went wrong instead of dying.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Try missing fields, invalid IDs and unavailable services.

### Q18. How do you prevent SQL injection?

**Short viva answer:** The audit does not certify that queries are parameterized or safe.

**Explain simply:** Never glue untrusted user text into a database command.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Inspect query construction and verify parameterized queries or safe ORM calls.


## AI/ML

### Q19. Did you train the model yourself?

**Short viva answer:** I did not find direct model-training steps in the inspected code. Do not claim the model was trained here.

**Explain simply:** Calling an AI API is like using someone else’s already-trained calculator. Training means teaching a model with data.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Find actual training script, data split, trained weights and run logs if claiming training.

### Q20. Where did you get the dataset? Show it.

**Short viva answer:** No local dataset file was found in the inspected files. It might be remote, generated or absent; verify before answering.

**Explain simply:** A dataset is examples a model learns from or looks things up in. One CSV file does not automatically mean training.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Identify the precise dataset source, license, sample rows and where it is loaded.

### Q21. Where is the model saved?

**Short viva answer:** Static inspection did not verify a trained model checkpoint or the hosted model behind any API.

**Explain simply:** A model file is like a saved brain; an API can use a brain hosted on someone else’s computer.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Find a real model checkpoint, model name or provider configuration.

### Q22. What is an AI model?

**Short viva answer:** An AI model is a program whose behaviour is shaped by learned patterns or parameters, rather than only hard-coded rules.

**Explain simply:** Think of a model like a student who learned from many examples.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Ask the project owner and check README, deployment, or external services.

### Q23. Are you using an AI API or your own ML model?

**Short viva answer:** No clear AI API call was identified. This does not prove there is no model: look for wrappers and external services.

**Explain simply:** API = you send a question to someone else’s service. Local model = the model runs in your own system.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Check model initialization and where inference actually executes.

### Q24. What is inference?

**Short viva answer:** Inference means using an already-prepared model to produce a prediction or response.

**Explain simply:** Training is studying; inference is answering the exam.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Ask the project owner and check README, deployment, or external services.

### Q25. What is RAG? Does your project use it?

**Short viva answer:** RAG was not established from this repository scan. Do not claim RAG simply because an LLM is present.

**Explain simply:** RAG = look up relevant notes first, then ask an AI to answer using those notes.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Show a retrieval step AND where its results enter the model prompt.

### Q26. Explain a RAG pipeline step by step.

**Short viva answer:** A typical RAG flow is: load documents -> split text -> create embeddings -> store vectors -> retrieve useful chunks -> include chunks in a prompt -> generate an answer. Actual steps depend on the project.

**Explain simply:** It is an open-book test: find pages, read them, then answer. Do not call this your implemented flow until you prove each step.

**Evidence:** intelligence/embed.py:2

**Proof level:** supported

**Verify:** Locate the exact implementation of each stage or mark it not implemented.

### Q27. What are embeddings?

**Short viva answer:** Embedding-related code markers exist; check where vectors are generated and stored.

**Explain simply:** An embedding turns text into a list of numbers so similar meanings can be compared.

**Evidence:** intelligence/embed.py:2

**Proof level:** supported

**Verify:** Find the exact embedding model and vector dimension if used.

### Q28. What is a vector database? Do you use one?

**Short viva answer:** No vector store was proven by this scan.

**Explain simply:** A vector database is a special library shelf that finds meaning-similar notes.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Name the actual store, collection, persistence and retrieval call.

### Q29. What is chunking and why use it?

**Short viva answer:** No explicit document chunking step was confirmed.

**Explain simply:** Chunking means cutting a long book into smaller pages, so finding the right part is easier.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Show chunk size, overlap, and why these values were chosen.

### Q30. How do you reduce hallucinations in the AI answer?

**Short viva answer:** No reliability evaluation was verified. RAG and citations can help grounding but do not guarantee correct answers.

**Explain simply:** A hallucination is when AI confidently makes something up. Make it show the source.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Test a set of answerable and unanswerable questions and measure grounded correctness.

### Q31. How do you evaluate model accuracy?

**Short viva answer:** No evaluation metrics were located. Do not invent accuracy percentages.

**Explain simply:** Accuracy asks: out of many known-answer questions, how many answers were right?

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Provide a held-out test set, metric definition and reproducible result.

### Q32. What is overfitting?

**Short viva answer:** Overfitting happens when a model learns the training examples too specifically and performs worse on new examples.

**Explain simply:** Like memorizing exam answers but not understanding the subject.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Ask the project owner and check README, deployment, or external services.

### Q33. What is fine-tuning versus prompting?

**Short viva answer:** Prompting changes the instructions sent to a model. Fine-tuning updates model parameters through training. Neither is confirmed without evidence.

**Explain simply:** Prompting tells the student what to do; fine-tuning gives the student extra lessons.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Ask the project owner and check README, deployment, or external services.


## Security

### Q34. Where is authentication implemented?

**Short viva answer:** No clear authentication implementation was confirmed.

**Explain simply:** Authentication checks who you are. Authorization checks what you may access.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Show login, token/session validation and a protected endpoint.

### Q35. Where are secrets and API keys stored?

**Short viva answer:** No environment variable names detected in scanned source; secrets were not read.

**Explain simply:** Secrets are house keys. Do not put them in a public repository or a viva PDF.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Verify secrets are server-side and not checked into version control.

### Q36. Can one user read another user’s data?

**Short viva answer:** Object-level authorization cannot be proven without tracing identity checks at each data-access route.

**Explain simply:** Knowing the house address does not mean someone should get the key.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Test access to another user’s ID in a controlled test environment.

### Q37. What happens if an attacker sends malicious input?

**Short viva answer:** No penetration test was run by Mercy. Treat security as unverified until tested.

**Explain simply:** Bad input should be rejected or treated as plain text, not followed as instructions.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Review input boundaries and test with safe invalid inputs.


## Quality

### Q38. How many tests does this project have?

**Short viva answer:** Found 0 files with test-like names. This is not a test pass result or a coverage percentage.

**Explain simply:** Tests are practice questions for your software. Counting them does not tell you if it passed.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Run the project test command and save the result.

### Q39. What are the limitations of your project?

**Short viva answer:** Known verification gaps: No direct training-loop evidence found; do not claim this model was trained here.; No dataset files or loaders located in the inspected source.. There may be other runtime limitations not visible in code.

**Explain simply:** A limitation is something your current project cannot reliably do yet.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Write down three issues observed in real usage, not guesses.

### Q40. How do you handle performance or high traffic?

**Short viva answer:** No load or latency benchmark was run. Architecture alone does not prove scaling ability.

**Explain simply:** Can the kitchen handle 100 orders at once? Measure instead of guessing.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Run a small controlled load test and record latency, error rate and resource use.


## Deployment

### Q41. Where is the project deployed?

**Short viva answer:** No deployed service was confirmed.

**Explain simply:** Deployment means putting the app on a computer/server where others can open it.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Show the real deployed URL, hosting dashboard and production start command.

### Q42. How does a new change reach production?

**Short viva answer:** No confirmed deployment pipeline was executed. Check CI configuration and actual production settings.

**Explain simply:** A deployment pipeline is the delivery route from your laptop to a live website.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Walk through an actual commit, build, test and deploy log.

### Q43. What would you improve next?

**Short viva answer:** Prioritize measured limitations, missing tests and unclear architecture before adding unnecessary features.

**Explain simply:** Fix broken doors before building another floor.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Pick a real observed limitation and explain how you would verify the fix.


## Defense

### Q44. Which part did you personally implement?

**Short viva answer:** Personal contribution cannot be established from repository code or Git history alone.

**Explain simply:** Say what you wrote, what a tool generated, and what you tested. Do not claim someone else’s work.

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Select two pieces of code you can explain line by line.

### Q45. If you remove the LLM, what still works?

**Short viva answer:** This requires a runtime dependency test; any detected AI SDK only gives a clue.

**Explain simply:** Pretend the AI service is offline. What parts of the app still work?

**Evidence:** No repository proof located

**Proof level:** not_verified

**Verify:** Disable external AI access in a local test and observe which features fail.

### Q46. Can you change one feature now and show exactly where?

**Short viva answer:** Use the dependency map to locate the responsible function, then explain how it is called and tested.

**Explain simply:** Showing a real small change proves you understand the project better than memorizing a speech.

**Evidence:** intelligence/embed.py:1, intelligence/pipeline.py:3, server/main.py:7

**Proof level:** supported

**Verify:** Pick a small input/label/validation rule and practice modifying it safely.


## Code-specific follow-ups

### Q47. Where is endpoint /status implemented, and what does it do?

**Short viva answer:** /status is declared in server/main.py:6; the likely handler is status. Its full behavior still requires reading the function body.

**Explain simply:** An endpoint is a door. Find the person standing behind that door and ask what happens next.

**Evidence:** server/main.py:6, server/main.py:7

**Proof level:** supported

**Verify:** Follow calls inside the handler and verify the real response.

### Q48. Why does infra/settings.py import server/main.py?

**Short viva answer:** infra/settings.py:1 imports server.main, which resolves to server/main.py. This proves a reference, not that every exported function is called.

**Explain simply:** One file borrows a tool from another file. Point at the borrowing line and find where the tool is actually used.

**Evidence:** infra/settings.py:1

**Proof level:** supported

**Verify:** Find the exact call site and show the input and output.

### Q49. Why does intelligence/pipeline.py import intelligence/embed.py?

**Short viva answer:** intelligence/pipeline.py:1 imports intelligence.embed, which resolves to intelligence/embed.py. This proves a reference, not that every exported function is called.

**Explain simply:** One file borrows a tool from another file. Point at the borrowing line and find where the tool is actually used.

**Evidence:** intelligence/pipeline.py:1

**Proof level:** supported

**Verify:** Find the exact call site and show the input and output.

### Q50. Why does server/main.py import intelligence/pipeline.py?

**Short viva answer:** server/main.py:2 imports intelligence.pipeline, which resolves to intelligence/pipeline.py. This proves a reference, not that every exported function is called.

**Explain simply:** One file borrows a tool from another file. Point at the borrowing line and find where the tool is actually used.

**Evidence:** server/main.py:2

**Proof level:** supported

**Verify:** Find the exact call site and show the input and output.

### Q51. Why does server/main.py import storage/db.py?

**Short viva answer:** server/main.py:3 imports storage.db, which resolves to storage/db.py. This proves a reference, not that every exported function is called.

**Explain simply:** One file borrows a tool from another file. Point at the borrowing line and find where the tool is actually used.

**Evidence:** server/main.py:3

**Proof level:** supported

**Verify:** Find the exact call site and show the input and output.

### Q52. Why does ui/components/App.jsx import ui/components/StatusBadge.jsx?

**Short viva answer:** ui/components/App.jsx:1 imports ./StatusBadge, which resolves to ui/components/StatusBadge.jsx. This proves a reference, not that every exported function is called.

**Explain simply:** One file borrows a tool from another file. Point at the borrowing line and find where the tool is actually used.

**Evidence:** ui/components/App.jsx:1

**Proof level:** supported

**Verify:** Find the exact call site and show the input and output.
