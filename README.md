# monty-skill

Run Python code in a secure sandbox using [pydantic-monty](https://github.com/pydantic/monty).

## How It Works

monty-skill executes Python code in an isolated environment where:
- No filesystem access
- No network access
- No environment variable access

External functions (defined in `functions.py`) can be called from sandboxed code to enable controlled I/O, network requests, or other operations.

## Usage

```bash
# Run directly (requires chmod +x)
./monty.py "print(2 + 2)"

# Or via uv
uv run monty.py "print(2 + 2)"

# With external functions
./monty.py "print(await greet('World'))" -f functions.py
```

## Options

| Flag | Description |
|------|-------------|
| `-f FILE` | External functions file |
| `-t SEC` | Timeout (default: 30) |

## External Functions

Define async functions in `functions.py`:

```python
async def fetch(url: str) -> dict:
    return {"data": "example"}

async def greet(name: str) -> str:
    return f"Hello, {name}!"
```

## Testing

Tests are in `test_monty.py`:

```bash
uv run pytest test_monty.py -v
```

See `test_monty.py` for more examples of supported Python features.

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv)
- pydantic-monty

MIT
