# External functions for monty sandbox
from typing import Any


async def fetch(url: str) -> dict[str, Any]:
    """Fetch data from a URL."""
    import urllib.request

    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = r.read().decode("utf-8")[:1000]
            return {"status": "ok", "url": url, "data": data}
    except Exception as e:
        return {"status": "error", "url": url, "error": str(e)}


async def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"


async def calculate(a: int, b: int, op: str) -> int:
    """Perform a calculation."""
    ops = {
        "add": lambda x, y: x + y,
        "sub": lambda x, y: x - y,
        "mul": lambda x, y: x * y,
        "div": lambda x, y: x / y if y else 0,
    }
    return ops.get(op, lambda x, y: 0)(a, b)


async def timestamp() -> dict[str, Any]:
    """Get current timestamp."""
    import datetime

    now = datetime.datetime.now()
    return {"iso": now.isoformat(), "ts": now.timestamp()}


async def capitalize(text: str) -> str:
    """Capitalize a string."""
    return text.capitalize()


async def reverse(text: str) -> str:
    """Reverse a string."""
    return text[::-1]


async def json_dumps(data: dict[str, Any]) -> str:
    """Convert dict to JSON string."""
    import json

    return json.dumps(data)


async def json_loads(text: str) -> dict[str, Any]:
    """Parse JSON string."""
    import json

    return json.loads(text)


# Custom functions for testing custom external functions feature
import random


def random_numbers(count: int) -> list:
    """Generate n random numbers between 0 and 1."""
    return [random.random() for _ in range(count)]


def random_int(min_val: int, max_val: int, count: int) -> list:
    """Generate n random integers between min and max (inclusive)."""
    return [random.randint(min_val, max_val) for _ in range(count)]
