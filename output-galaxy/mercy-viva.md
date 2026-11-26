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

### GUIDE_PURPOSE. What does this project do?

Galaxy Demo is a tiny teaching example for Mercy. It shows source files and imports; it has no connected website-to-server flow, real database or trained model.

<details>
<summary>Details</summary>

Galaxy Demo is a tiny teaching example for Mercy. It shows source files and imports; it has no connected website-to-server flow, real database or trained model.

**Source:** README.md:3

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>

### GUIDE_ENTRY. How do you start it?

The backend application is defined in server/main.py. This sample has no startup script; a runnable setup still needs to be supplied.

<details>
<summary>Details</summary>

The backend application is defined in server/main.py. This sample has no startup script; a runnable setup still needs to be supplied.

**Source:** server/main.py:1

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>


## Architecture

### GUIDE_DEPENDENCIES. Which tools does it use?

The backend uses FastAPI. The interface uses JSX components. The intelligence and storage helpers are simple Python placeholders.

<details>
<summary>Details</summary>

The backend uses FastAPI. The interface uses JSX components. The intelligence and storage helpers are simple Python placeholders.

**Source:** server/main.py:1, ui/components/App.jsx:1, intelligence/embed.py:1

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>

### GUIDE_MODULES. What are its main components?

There are website components, an API, a placeholder intelligence helper, a storage placeholder and infrastructure settings. The website does not call the API.

<details>
<summary>Details</summary>

There are website components, an API, a placeholder intelligence helper, a storage placeholder and infrastructure settings. The website does not call the API.

**Source:** ui/components/App.jsx:1, server/main.py:1, infra/settings.py:1

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>

- **Website:** Displays a heading and demo badge. (ui/components/App.jsx:1)
- **API:** Returns the status JSON. (server/main.py:6)
- **Demo intelligence:** Returns a placeholder vector, not a model prediction. (intelligence/pipeline.py:3)
- **Storage placeholder:** Returns zero without a database. (storage/db.py:1)
- **Settings:** Imports the API application and marks the example as a demo. (infra/settings.py:1)
- **ui/:** Website components and styles. (ui/components/App.jsx:1)
- **ui/components/:** Small reusable parts of the website. (ui/components/StatusBadge.jsx:1)
- **server/:** The status API. (server/main.py:1)
- **storage/:** A placeholder for data access. (storage/db.py:1)
- **intelligence/:** Educational answer and vector helpers. (intelligence/pipeline.py:1)
- **infra/:** Demo application settings. (infra/settings.py:1)
### GUIDE_WORKFLOW. How does a user get a result?

Request /status from the API. It reads a placeholder count, calls the demo answer helper and returns both in JSON. The website is a separate display-only component.

<details>
<summary>Details</summary>

Request /status from the API. It reads a placeholder count, calls the demo answer helper and returns both in JSON. The website is a separate display-only component.

**Source:** server/main.py:6, ui/components/App.jsx:2

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>

#### Demo

1. **Request /status from the running sample API.** The handler returns a count and a demo answer object. (server/main.py:6)

2. **Inspect the returned values.** The count is zero. The vector represents the length of “hello”, not a real embedding. (storage/db.py:2, intelligence/embed.py:2, server/main.py:8)

3. **Inspect the website component.** It displays a demo badge. It does not request /status. (ui/components/App.jsx:2)

#### User flow (source trace)

- Open an API client → Request /status — server/main.py:6
- Request /status → Read count and demo answer — server/main.py:6
- Read count and demo answer → Finish — server/main.py:6

## Data

### GUIDE_VALIDATION. How are inputs checked?

The status handler accepts no user fields. It sends the fixed text “hello” to the demo helper, so this route does not demonstrate form validation.

<details>
<summary>Details</summary>

The status handler accepts no user fields. It sends the fixed text “hello” to the demo helper, so this route does not demonstrate form validation.

**Source:** server/main.py:7

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>

### GUIDE_STORAGE. Where is the data stored?

The storage helper returns zero. It does not connect to a database or save records.

<details>
<summary>Details</summary>

The storage helper returns zero. It does not connect to a database or save records.

**Source:** storage/db.py:1

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>


## Quality

### GUIDE_ERRORS. What happens if something fails?

The inspected status handler has no custom error recovery. This example does not show retries or a user-facing error screen.

<details>
<summary>Details</summary>

The inspected status handler has no custom error recovery. This example does not show retries or a user-facing error screen.

**Source:** server/main.py:6

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>


## Architecture

### GUIDE_INTEGRATIONS. Which outside services does it use?

The inspected request path calls local Python helpers. It does not call an AI provider or another remote service.

<details>
<summary>Details</summary>

The inspected request path calls local Python helpers. It does not call an AI provider or another remote service.

**Source:** server/main.py:7, intelligence/pipeline.py:3

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>


## Quality

### GUIDE_LIMITS. What are its limitations?

The embedding is just the text length, the stored count is always zero, and the interface is not connected to the API. This is a source example, not a complete application.

<details>
<summary>Details</summary>

The embedding is just the text length, the stored count is always zero, and the interface is not connected to the API. This is a source example, not a complete application.

**Source:** intelligence/embed.py:2, storage/db.py:2, README.md:3

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>
