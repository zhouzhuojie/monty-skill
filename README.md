# monty-skill

Run Python code in a secure sandbox using [pydantic-monty](https://github.com/pydantic/monty).

## Quick Start

```bash
uv run https://raw.githubusercontent.com/zhouzhuojie/monty-skill/main/monty.py "print(2 + 2)"
```

## Options

| Flag | Description |
|------|-------------|
| `-f FILE` | External functions file |
| `-t SEC` | Timeout in seconds |

## External Functions

Create `functions.py` with async functions:

```python
async def greet(name: str) -> str:
    return f"Hello, {name}!"
```

```bash
curl -sL https://raw.githubusercontent.com/zhouzhuojie/monty-skill/main/functions.py > functions.py
uv run https://raw.githubusercontent.com/zhouzhuojie/monty-skill/main/monty.py "print(await greet('World'))" -f functions.py
```

## Install for AI Agents

```bash
npx skills add zhouzhuojie/monty-skill
```

## Development

```bash
git clone https://github.com/zhouzhuojie/monty-skill.git
cd monty-skill
uv run pytest test_monty.py -v
```

See `test_monty.py` for examples.

MIT
