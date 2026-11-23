# Mercy architecture clues: mini-rag

> **Caution:** imports are dependency clues, not verified runtime data flow.

## Local module imports

```mermaid
flowchart LR
    N0["app.py"]
    N1["rag.py"]
    N0 --> N1
```

## Detected routes

| Endpoint | Source |
|---|---|
| `/health` | `app.py:5` |
| `/ask` | `app.py:9` |

## Technology hints

| Tech | Evidence |
|---|---|
| FastAPI | app.py:1, app.py:3 |
| OpenAI SDK | rag.py:1, rag.py:3 |

## Dataset and model provenance

- No local dataset file confirmed.
- Training steps found: 0 (code markers; not proof of a completed run).
- AI API markers found: 1.
- Retrieval markers found: 0 (not a complete RAG proof).

## What to trace manually

1. One user action and the actual frontend call.
2. The exact API handler and its input/output schema.
3. The database query or model call, if any.
4. What happens on failure and how errors reach the user.
5. Training evidence: data provenance, experiment logs, model weights, and evaluation metrics (if the project trains a model).
