# monty-skill

Run Python code in a secure sandbox using [pydantic-monty](https://github.com/pydantic/monty).

## Quick Start

```bash
uv run https://raw.githubusercontent.com/zhouzhuojie/monty-skill/main/monty.py "print(2 + 2)"
```

> **Note:** Since `uv run` downloads `monty.py` from the remote repo, the local `functions.py` does **not** exist by default. If you need external functions, create a `functions.py` file and pass it with `-f`.

## Options

| Flag | Description |
|------|-------------|
| `-f FILE` | Path to external functions file |
| `-d FILE` | Requirements file for extra dependencies |
| `-t SEC` | Timeout in seconds |

## External Functions

Create `functions.py` with your custom async or sync functions:

```python
async def greet(name: str) -> str:
    return f"Hello, {name}!"
```

Then use with `-f` flag pointing to your local file:

```bash
uv run https://raw.githubusercontent.com/zhouzhuojie/monty-skill/main/monty.py "print(await greet('World'))" -f functions.py
```

You can download the default `functions.py` for reference:

```bash
curl -sL https://raw.githubusercontent.com/zhouzhuojie/monty-skill/main/functions.py > functions.py
```

## Adding Extra Dependencies

If your external functions require additional packages (e.g., cryptography, requests), you have three options:

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

Monty will automatically detect this and install the dependencies.

### Option 3: Use `--with` directly (advanced)

```bash
uv run --with cryptography --with requests https://raw.githubusercontent.com/zhouzhuojie/monty-skill/main/monty.py "encrypt('secret')" -f functions.py
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
