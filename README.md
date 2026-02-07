# monty

Run Python in a secure sandbox with [pydantic-monty](https://github.com/pydantic/monty).

```bash
uv run monty.py "print(2 + 2)"
uv run monty.py "print(await greet('World'))" -f functions.py
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

## Requirements

Python 3.10+, [uv](https://github.com/astral-sh/uv)

MIT
