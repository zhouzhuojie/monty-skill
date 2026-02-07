#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pydantic-monty"]
# ///
"""monty - Run Python code in a secure sandbox."""

import argparse
import asyncio
import re
import sys
from pathlib import Path

try:
    import pydantic_monty
except ImportError:
    print("Error: pydantic-monty not installed")
    print("Install: uv add pydantic-monty")
    sys.exit(1)


BUILTINS = {
    'print', 'len', 'str', 'int', 'float', 'bool', 'list', 'dict', 'set',
    'tuple', 'range', 'enumerate', 'zip', 'map', 'filter', 'sorted',
    'reversed', 'type', 'isinstance', 'hasattr', 'getattr', 'setattr',
    'delattr', 'break', 'continue', 'pass', 'return', 'yield', 'raise',
    'try', 'except', 'finally', 'async', 'await', 'if', 'else', 'elif',
    'for', 'while', 'def', 'class', 'import', 'from', 'as', 'assert',
    'del', 'global', 'nonlocal', 'lambda', 'or', 'and', 'not', 'in',
    'True', 'False', 'None', 'self', 'super', '__import__',
}


def parse_args():
    parser = argparse.ArgumentParser(prog="monty", description="Run Python code in a secure sandbox.")
    parser.add_argument("code", help="Python code to execute")
    parser.add_argument("-f", "--functions", default="functions.py", help="External functions file")
    parser.add_argument("-t", "--timeout", type=int, default=30, help="Timeout in seconds")
    return parser.parse_args()


def load_external_functions(functions_file: str) -> tuple[dict, str]:
    func_code = ""
    external_funcs = {}
    path = Path(functions_file)
    if path.exists():
        func_code = path.read_text()
    if func_code:
        namespace = {}
        exec(compile(func_code, "<functions>", "exec"), namespace)
        for name, obj in namespace.items():
            if callable(obj) and not name.startswith("_"):
                external_funcs[name] = obj
    return external_funcs, func_code


def find_function_calls(code: str) -> set:
    calls = set()
    for match in re.finditer(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", code):
        fn_name = match.group(1)
        if fn_name not in BUILTINS:
            calls.add(fn_name)
    return calls


async def run_monty(code: str, functions_file: str) -> str:
    external_funcs, func_code = load_external_functions(functions_file)
    used_funcs = find_function_calls(code)
    filtered_funcs = {k: v for k, v in external_funcs.items() if k in used_funcs}

    m = pydantic_monty.Monty(
        code, inputs=[], external_functions=list(filtered_funcs.keys()),
        script_name="sandbox.py", type_check=False, type_check_stubs=func_code,
    )

    if filtered_funcs:
        result = await pydantic_monty.run_monty_async(m, external_functions=filtered_funcs)
    else:
        result = await pydantic_monty.run_monty_async(m)

    if result and hasattr(result, "output"):
        return result.output
    return ""


def main():
    args = parse_args()
    try:
        output = asyncio.run(run_monty(args.code, args.functions))
        print(output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
