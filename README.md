# monty-skill

Run Python code safely in a secure sandbox using [pydantic-monty](https://github.com/pydantic/monty).

A skill for AI coding agents to execute LLM-generated Python code without filesystem, network, or environment access risks.

## What It Does

- Executes Python code in a **secure, isolated** environment
- Blocks filesystem, network, and environment access by default
- Supports **external functions** you define for controlled I/O
- Starts in **microseconds** (~1ms, vs ~200ms for Docker)
- Works with any AI agent that supports bash scripts

## Quick Start

```bash
# Clone and setup
git clone https://github.com/zhouzhuojie/monty-skill.git
cd monty-skill

# Install dependencies
uv venv
source .venv/bin/activate
uv add pydantic-monty

# Run a simple calculation
./monty "result = 2 + 2; print(f'2 + 2 = {result}')"

# Execute multi-line code
./monty "
total = 0
for i in range(1, 6):
    total += i
print(f'Sum of 1-5: {total}')
"
```

## Usage

```bash
./monty "python_code" [OPTIONS]
```

### Options

| Option | Description |
|--------|-------------|
| `-h, --help` | Show help |
| `-f, --functions-file` | Path to external functions (default: `./functions.py`) |
| `-t, --timeout` | Timeout in seconds (default: 30) |

## External Functions

Define async functions in `functions.py` for sandboxed code to access external resources:

```python
from typing import Any

async def fetch(url: str) -> dict[str, Any]:
    """Fetch data from a URL."""
    # Your implementation here - sandbox can't access network directly
    return {"status": "ok", "data": "example"}

async def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"
```

Then call them from sandboxed code:

```bash
./monty "print(await greet('World'))"
```

## Supported Python Features

### Built-in Functions
- `print()`, `len()`, `str()`, `int()`, `float()`, `bool()`
- `list()`, `dict()`, `set()`, `tuple()`
- `range()`, `enumerate()`, `zip()`, `map()`, `filter()`
- `sorted()`, `reversed()`
- `type()`, `isinstance()`, `hasattr()`, `getattr()`

### Standard Library
- `sys`, `typing`, `asyncio`, `dataclasses`, `json`

### Language Features
- Variable assignments
- Functions (no classes yet)
- Control flow (`if`, `for`, `while`)
- `async`/`await`
- Type hints
- List/dict comprehensions
- Lambdas

### Not Supported
- Third-party libraries (pandas, requests, numpy, etc.)
- Classes (coming soon)
- Match statements (coming soon)
- Direct filesystem/network access

## Examples

### Data Processing
```bash
./monty "
data = [1, 2, 3, 4, 5]
squared = [x ** 2 for x in data]
print(f'Sum: {sum(squared)}')
"
```

### Type Hints
```bash
./monty "
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

print(f'Fib(10) = {fib(10)}')
"
```

### External Functions
```bash
./monty "
result = await fetch('https://example.com')
print(f'Data: {len(str(result))} bytes')
" -f functions.py
```

## Integration with AI Agents

### Claude (Anthropic)

Add to your agent configuration:
```yaml
skills:
  monty:
    command: ./monty
    description: Run Python code in secure sandbox
```

### OpenAI GPT

```python
assistant = OpenAIAssistant(...)
assistant.register_tool_function(
    name="monty",
    description="Execute Python code safely in sandbox",
    parameters={
        "type": "object",
        "properties": {
            "code": {"type": "string", "description": "Python code to execute"}
        },
        "required": ["code"]
    }
)
```

### Smith (OpenAI)

```typescript
import { Tool } from "openai/agents"

const monty: Tool = {
    name: "monty",
    description: "Execute Python code in secure sandbox",
    parameters: {
        type: "object",
        properties: {
            code: { type: "string", description: "Python code to execute" }
        },
        required: ["code"]
    },
    execute: async ({ code }) => {
        const result = await execSync(`./monty "${code.replace(/"/g, '\\"')}"`)
        return result.toString()
    }
}
```

### Pi Agent

Copy to `~/Documents/pi/skills/`:
```bash
cp -r ~/Dev/monty-skill ~/.pi/agent/skills/monty-skill
```

## Why Not Docker/Pyodide?

| Feature | Monty | Docker | Pyodide |
|---------|-------|--------|---------|
| Startup | <1ms | ~200ms | ~2800ms |
| Security | Strict | Good | Poor |
| Full stdlib | No | Yes | Yes |
| Third-party | No | Yes | Yes |
| Setup | Easy | Medium | Medium |

Monty is designed specifically for running LLM-generated code. It's not a general-purpose Python runtime.

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) or pip
- pydantic-monty

## License

MIT
