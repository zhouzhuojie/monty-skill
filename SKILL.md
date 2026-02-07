---
name: monty
description: Execute Python code in a secure sandbox using pydantic-monty. Use when running LLM-generated Python code that should be isolated from filesystem, network, and environment access.
---

# Monty Sandbox

Execute Python code safely without filesystem/network access.

## When to Use

- Running LLM-generated Python code
- Data processing, calculations, transformations
- Testing code snippets before production use

## When Not to Use

- Code requiring third-party libraries (pandas, requests)
- Code needing filesystem/network access
- Complex class definitions

## Usage

```bash
uv run monty.py "print(2 + 2)"
uv run monty.py "sum([x ** 2 for x in range(1, 6)])"
uv run monty.py "print(await greet('World'))" -f functions.py
```

## Options

| Flag | Description |
|------|-------------|
| `-f, --functions FILE` | External functions file |
| `-t, --timeout SECONDS` | Timeout (default: 30) |

## External Functions

Define async functions in `functions.py`:

```python
async def fetch(url: str) -> dict:
    return {"data": "example"}

async def greet(name: str) -> str:
    return f"Hello, {name}!"
```

## Supported Python

- Built-ins: `print`, `len`, `str`, `int`, `list`, `dict`, `range`
- Control flow, functions, async/await, type hints

## Not Supported

- Classes, match statements
- Third-party libraries
- Direct filesystem/network access
