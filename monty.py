#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pydantic-monty"]
# ///
"""monty - Run Python code in a secure sandbox.

Usage:
    monty "code here"                        # Basic usage
    monty "code" -f functions.py             # With custom functions
    monty "code" -d requirements.txt         # With extra dependencies

To extend dependencies, add to functions.py:
    # /// monty-deps: cryptography, requests

Or use a requirements.txt file alongside monty.py
"""

import argparse
import asyncio
import re
import subprocess
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
    parser = argparse.ArgumentParser(
        prog="monty",
        description="Run Python code in a secure sandbox.",
        epilog="""
Examples:
    monty "print('hello')"
    monty "result = fetch('https://api.example.com')" -f my_functions.py
    monty "encrypt('secret')" -d requirements.txt

To add dependencies, add a comment to your functions.py:
    # /// monty-deps: cryptography, requests
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("code", help="Python code to execute")
    parser.add_argument("-f", "--functions", default="functions.py", help="External functions file")
    parser.add_argument("-d", "--deps", help="Requirements file for extra dependencies")
    parser.add_argument("-t", "--timeout", type=int, default=30, help="Timeout in seconds")
    return parser.parse_args()


def find_deps_from_functions(functions_file: str) -> list[str]:
    """Extract dependencies from special comment in functions.py."""
    path = Path(functions_file)
    if not path.exists():
        return []
    
    deps = []
    pattern = re.compile(r"#\s*///\s*monty-deps:\s*(.+)")
    
    for line in path.read_text().splitlines():
        match = pattern.match(line)
        if match:
            deps_str = match.group(1).strip()
            deps = [d.strip() for d in deps_str.split(",") if d.strip()]
            break
    
    return deps


def parse_requirements_file(req_file: str) -> list[str]:
    """Parse requirements.txt file."""
    path = Path(req_file)
    if not path.exists():
        return []
    
    deps = []
    for line in path.read_text().splitlines():
        line = line.strip()
        # Skip comments, empty lines, and editable installs
        if line and not line.startswith("#") and not line.startswith("-e"):
            # Remove version specifiers for --with
            pkg = line.split("==")[0].split(">=")[0].split("<=")[0].split(">")[0].split("<")[0]
            deps.append(pkg.strip())
    
    return deps


def check_and_rerun_with_deps():
    """Check if additional deps are needed and rerun with them."""
    args = sys.argv[1:]
    
    # Check for --deps flag
    deps_file = None
    filtered_args = []
    for i, arg in enumerate(args):
        if arg in ("-d", "--deps") and i + 1 < len(args):
            deps_file = args[i + 1]
            # Remove -d/--deps and its value from args
        elif arg in ("-d", "--deps"):
            continue
        else:
            filtered_args.append(arg)
    
    if deps_file:
        deps = parse_requirements_file(deps_file)
        if deps:
            # Rerun with --with flags
            with_flags = " ".join(f"--with {d}" for d in deps)
            cmd = f"uv run {with_flags} {__file__} {' '.join(filtered_args)}"
            sys.exit(subprocess.run(cmd, shell=True).returncode)
    
    # Check functions.py for deps comment
    functions_file = "functions.py"
    for i, arg in enumerate(args):
        if arg in ("-f", "--functions") and i + 1 < len(args):
            functions_file = args[i + 1]
            break
    
    deps = find_deps_from_functions(functions_file)
    if deps:
        with_flags = " ".join(f"--with {d}" for d in deps)
        cmd = f"uv run {with_flags} {__file__} {' '.join(filtered_args)}"
        sys.exit(subprocess.run(cmd, shell=True).returncode)


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
    check_and_rerun_with_deps()  # Handle deps before running
    
    args = parse_args()
    try:
        output = asyncio.run(run_monty(args.code, args.functions))
        print(output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
