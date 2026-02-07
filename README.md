# monty-skill

Run Python code in a secure sandbox using [pydantic-monty](https://github.com/pydantic/monty).

## Quick Start

```bash
# Run directly from GitHub (uv caches automatically)
uv run https://raw.githubusercontent.com/zhouzhuojie/monty-skill/main/monty.py "print(2 + 2)"
```

## For AI Agents

Copy to your agent's skills directory:

```bash
# For Claude
cp -r monty-skill ~/.claude/skills/

# For Pi
cp -r monty-skill ~/.pi/agent/skills/
```

## How It Works

monty-skill executes Python code in an isolated environment where:
- No filesystem access
- No network access
- No environment variable access

External functions (defined in `functions.py`) can be called from sandboxed code to enable controlled I/O, network requests, or other operations.

## Usage

```bash
# Run directly
uv run https://raw.githubusercontent.com/zhouzhuojie/monty-skill/main/monty.py "print(2 + 2)"

# With external functions (download functions.py first)
curl -sL https://raw.githubusercontent.com/zhouzhuojie/monty-skill/main/functions.py > functions.py
uv run https://raw.githubusercontent.com/zhouzhuojie/monty-skill/main/monty.py "print(await greet('World'))" -f functions.py
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

```bash
# Clone for local development
git clone https://github.com/zhouzhuojie/monty-skill.git
cd monty-skill
uv run pytest test_monty.py -v
```

See `test_monty.py` for comprehensive examples.

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv)
- pydantic-monty

MIT
