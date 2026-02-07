---
name: monty
description: Execute Python code in a secure sandbox using pydantic-monty. Use when running LLM-generated code that should be isolated from filesystem/network access.
---

# monty

Execute Python code safely without filesystem/network access.

## Run

```bash
uv run https://raw.githubusercontent.com/zhouzhuojie/monty-skill/main/monty.py "code here"
```

## Options

| Flag | Description |
|------|-------------|
| `-f FILE` | External functions file |
| `-t SEC` | Timeout in seconds |

## External Functions

Define in `functions.py`:

```python
async def fetch(url: str) -> dict:
    return {"data": "example"}
```

## Supported Python

- Built-ins: `print`, `len`, `str`, `int`, `list`, `dict`, `range`
- Control flow, functions, async/await, type hints

## Not Supported

- Third-party libraries (pandas, requests)
- Classes, match statements
- Direct filesystem/network access

## Examples

See `test_monty.py` for comprehensive examples including arithmetic, comprehensions, lambdas, type hints, and error handling.
