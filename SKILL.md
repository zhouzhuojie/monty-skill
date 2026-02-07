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
# Simple calculation
uv run monty "print(2 + 2)"

# Multi-line code
uv run monty "
total = sum(range(1, 6))
print(f'Sum: {total}')
"

# With external functions
uv run monty "print(await greet('World'))" -f functions.py

# Custom timeout (seconds)
uv run monty "time.sleep(1)" -t 5
```

## Options

| Flag | Description |
|------|-------------|
| `-f, --functions FILE` | External functions file |
| `-t, --timeout SECONDS` | Timeout (default: 30) |

## External Functions

Define async functions in `functions.py` for sandboxed code to call:

```python
async def fetch(url: str) -> dict:
    # Your implementation here
    return {"data": "example"}

async def greet(name: str) -> str:
    return f"Hello, {name}!"
```

## Supported Python

- Built-ins: `print`, `len`, `str`, `int`, `list`, `dict`, `range`, etc.
- Stdlib: `sys`, `typing`, `asyncio`, `dataclasses`, `json`
- Control flow: `if`, `for`, `while`, functions, async/await
- Type hints, comprehensions, lambdas

## Not Supported

- Classes (coming soon)
- Match statements (coming soon)
- Third-party libraries
- Direct filesystem/network access
