# monty

Run Python in a secure sandbox with [pydantic-monty](https://github.com/pydantic/monty).

```bash
uv run monty "print(2 + 2)"
uv run monty "print(sum(range(1, 6)))"
uv run monty "print(await greet('World'))" -f functions.py
```

## Options

| Flag | Description |
|------|-------------|
| `-f FILE` | Functions file |
| `-t SEC` | Timeout (default: 30) |

## Functions

```python
async def fetch(url: str) -> dict:
    return {"data": "example"}
```

## Supported

- Built-ins, `sys`, `typing`, `asyncio`, `json`
- Control flow, functions, async/await, type hints

## Not Supported

- Classes, third-party libs, filesystem/network

## Requirements

Python 3.10+, [uv](https://github.com/astral-sh/uv)

MIT
