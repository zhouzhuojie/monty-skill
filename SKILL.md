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

> **Note:** Since `uv run` downloads `monty.py` from the remote repo, the local `functions.py` does **not** exist by default. If you need external functions, create a `functions.py` file and pass it with `-f`.

## Options

| Flag | Description |
|------|-------------|
| `-f FILE` | Path to external functions file (default: `functions.py`) |
| `-d FILE` | Requirements file for extra dependencies |
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
uv run https://raw.githubusercontent.com/zhouzhuojie/monty-skill/main/monty.py "result = random_numbers(1000); print(f'Mean: {sum(result)/len(result):.4f}')" -f functions.py
```

## Adding Extra Dependencies

If your external functions require additional packages (e.g., cryptography, requests), you have two options:

### Option 1: Use `-d` flag with a requirements file

```bash
# Create requirements.txt
echo "cryptography" > requirements.txt

# Run with extra dependencies
uv run https://raw.githubusercontent.com/zhouzhuojie/monty-skill/main/monty.py "encrypt('secret')" -f functions.py -d requirements.txt
```

### Option 2: Add a comment in functions.py

Add a special comment to your `functions.py`:

```python
# /// monty-deps: cryptography, requests

import cryptography
import requests
...
```

Monty will automatically detect this and install the dependencies when the functions file is loaded.

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
