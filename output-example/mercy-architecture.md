# Architecture: mini-rag

> Source analysis. Arrows aggregate resolved imports, not runtime calls.

```mermaid
flowchart LR
    N0["Question API"]
    N1["Model helper"]
    N0 --> N1
```

## Question API

Accepts questions and returns JSON.

Source: app.py:9

## Model helper

Sends a prompt to OpenAI and extracts the answer.

Source: rag.py:5

- `app.py:2` imports `rag.py`
