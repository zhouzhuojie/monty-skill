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

If your external functions need packages like `cryptography` or `requests`, use `uv run --with`:

```bash
uv run --with cryptography --with requests https://raw.githubusercontent.com/zhouzhuojie/monty-skill/main/monty.py "encrypt('secret')" -f functions.py
```

> **Note:** The `--with` packages are only available to your external functions running on the host. The sandboxed code (LLM-generated) still cannot access these packages directly - it must call through your external functions. This maintains the security guarantee.

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
