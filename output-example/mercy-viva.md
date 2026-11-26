# MERCY | mini-rag | Viva Preparation

> Evidence-first preparation. A source reference shows a code clue, not proof that a feature works in production.

## Repository scan

- Files read: 4
- Data-shaped files: 0
- Routes detected: 2
- Resolved local imports: 1
- Tech markers: FastAPI, OpenAI SDK

## Module connections

- `app.py` -> `rag.py` (import `rag`)

## Important verification gaps

- No direct training-loop evidence found; do not claim this model was trained here.
- No dataset files or loaders located in the inspected source.

## Start here

### GUIDE_PURPOSE. What does this project do?

This small API sends a question to an OpenAI model and returns its answer. Despite the folder name, it does not implement document retrieval or RAG.

<details>
<summary>Details</summary>

This small API sends a question to an OpenAI model and returns its answer. Despite the folder name, it does not implement document retrieval or RAG.

**Source:** README.md:3, rag.py:5

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>

### GUIDE_ENTRY. How do you start it?

app.py creates the FastAPI application and defines the routes. No startup command or dependency manifest is supplied in this tiny sample.

<details>
<summary>Details</summary>

app.py creates the FastAPI application and defines the routes. No startup command or dependency manifest is supplied in this tiny sample.

**Source:** app.py:1, app.py:3

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>


## Architecture

### GUIDE_DEPENDENCIES. Which tools does it use?

FastAPI defines the API. The OpenAI Python client sends the model request. Their installed versions and credentials still need checking.

<details>
<summary>Details</summary>

FastAPI defines the API. The OpenAI Python client sends the model request. Their installed versions and credentials still need checking.

**Source:** app.py:1, rag.py:1

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>

#### Backend: Python + FastAPI

app.py defines the health endpoint and accepts questions at /ask. No frontend information is reviewed in this tiny API example.

Locations: app.py

Source: app.py:9

- [FastAPI documentation](https://fastapi.tiangolo.com/)
#### Model: Configured OpenAI model

The helper names gpt-4.1-mini and sends it a question. Credentials, availability and response quality remain unverified.

From: An external OpenAI API call, not locally trained weights or a retrieval pipeline.

Locations: rag.py

Source: rag.py:7

- [OpenAI Python client](https://github.com/openai/openai-python)
### GUIDE_MODULES. What are its main components?

The API handles requests in app.py. The model helper in rag.py sends the question to OpenAI and extracts the returned text.

<details>
<summary>Details</summary>

The API handles requests in app.py. The model helper in rag.py sends the question to OpenAI and extracts the returned text.

**Source:** app.py:9, rag.py:5

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>


<details>
<summary>File explanations</summary>

- **README.md:** Introduces the sample and explains that its name does not establish RAG. (README.md:1)
- **app.py:** Defines the health endpoint and passes questions to the model helper. (app.py:1)
- **rag.py:** Sends the question directly to the OpenAI chat API and extracts the returned text. (rag.py:1)

</details>

- **Question API:** Accepts questions and returns JSON. (app.py:9)
- **Model helper:** Sends a prompt to OpenAI and extracts the answer. (rag.py:5)
### GUIDE_WORKFLOW. How does a user get a result?

Submit a question to /ask. The handler passes it to the model helper and returns the response as JSON.

<details>
<summary>Details</summary>

Submit a question to /ask. The handler passes it to the model helper and returns the response as JSON.

**Source:** app.py:9, rag.py:7

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>

#### Demo

1. **Request /health from the running sample API.** The handler returns a JSON status of “ok”. (app.py:5)

2. **Submit POST /ask?question=What%20is%20Python.** With a working provider setup, the handler sends the question to the model and returns answer text. (app.py:9, rag.py:7)

3. **Explain why this is not RAG.** The helper sends the question directly to the model. It does not retrieve project documents. (rag.py:5, README.md:3)

#### User flow (source trace)

- Prepare a question → Submit to /ask — app.py:9
- Submit to /ask → Read the returned answer — app.py:9
- Read the returned answer → Finish — app.py:9

## Data

### GUIDE_VALIDATION. How are inputs checked?

The question parameter is declared as text. These handlers do not show extra checks such as minimum length or content rules.

<details>
<summary>Details</summary>

The question parameter is declared as text. These handlers do not show extra checks such as minimum length or content rules.

**Source:** app.py:10

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>

### GUIDE_STORAGE. Where is the data stored?

The inspected request path sends the question to the provider and returns the response. It does not save the conversation or read a document store.

<details>
<summary>Details</summary>

The inspected request path sends the question to the provider and returns the response. It does not save the conversation or read a document store.

**Source:** rag.py:5, README.md:3

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>


## Quality

### GUIDE_ERRORS. What happens if something fails?

There is no custom exception handling around the model call in these two files. Provider failure behavior needs a separate runtime check.

<details>
<summary>Details</summary>

There is no custom exception handling around the model call in these two files. Provider failure behavior needs a separate runtime check.

**Source:** rag.py:7, app.py:11

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>


## Architecture

### GUIDE_INTEGRATIONS. Which outside services does it use?

The helper calls OpenAI chat completions with the configured model name. A source call does not prove credentials, network access or model availability.

<details>
<summary>Details</summary>

The helper calls OpenAI chat completions with the configured model name. A source call does not prove credentials, network access or model availability.

**Source:** rag.py:7

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>


## Quality

### GUIDE_LIMITS. What are its limitations?

This sample has no retrieval, embedding store, training pipeline or accuracy measurement. It also lacks custom error handling and a complete runnable setup.

<details>
<summary>Details</summary>

This sample has no retrieval, embedding store, training pipeline or accuracy measurement. It also lacks custom error handling and a complete runnable setup.

**Source:** README.md:3, rag.py:5

**Evidence level:** supported (source analysis; execution not verified)

**Check:** Source walkthrough only. Run the sample separately with explicit authorization to check runtime behavior.

</details>
