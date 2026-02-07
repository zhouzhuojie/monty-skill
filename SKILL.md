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

Define safe functions in `functions.py` for use in sandboxed code:

```python
import random

def random_numbers(count: int) -> list:
    """Generate n random numbers between 0 and 1."""
    return [random.random() for _ in range(count)]

async def fetch(url: str) -> dict:
    return {"data": "example"}
```

### Creating Custom Functions

If a feature isn't available in the built-ins, you can add your own safe functions to `functions.py`. Monty will automatically detect and load functions that are called in your code.

**Example: Generating random numbers**

```python
# functions.py
import random

def random_numbers(count: int) -> list:
    """Generate n random numbers between 0 and 1."""
    return [random.random() for _ in range(count)]

def random_int(min_val: int, max_val: int, count: int) -> list:
    """Generate n random integers between min and max (inclusive)."""
    return [random.randint(min_val, max_val) for _ in range(count)]
```

Then use in monty:
```bash
uv run monty.py "result = random_numbers(1000); print(f'Mean: {sum(result)/len(result):.4f}')"
```

## Install for Agents

```bash
npx skills add zhouzhuojie/monty-skill
```

Or manually:

```bash
git clone https://github.com/zhouzhuojie/monty-skill.git
cp -r monty-skill ~/.claude/skills/  # Claude
cp -r monty-skill ~/.pi/agent/skills/  # Pi
```

## Supported Python

- Built-ins: `print`, `len`, `str`, `int`, `list`, `dict`, `range`
- Control flow, functions, async/await, type hints

## Not Supported

- Third-party libraries (pandas, requests)
- Classes, match statements
- Direct filesystem/network access

## Examples

See `test_monty.py` for comprehensive examples.
