# parseq

> A tiny, zero-dependency argument parser for Python 3.10+.

[![PyPI](https://img.shields.io/pypi/v/parseq)](https://pypi.org/project/parseq/) [![CI](https://img.shields.io/github/actions/workflow/status/example/parseq/ci.yml)](https://github.com/example/parseq/actions) [![License: MIT](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

parseq is an argument parser that reads like a type-annotated function signature. It's useful when you want argparse's power without argparse's API.

```python
from parseq import command

@command
def greet(name: str, count: int = 1, *, loud: bool = False) -> None:
    """Greet someone count times."""
    message = f"Hello, {name}!"
    if loud:
        message = message.upper()
    for _ in range(count):
        print(message)

if __name__ == "__main__":
    greet()
```

Then:

```
$ python greet.py Alice --count 3 --loud
HELLO, ALICE!
HELLO, ALICE!
HELLO, ALICE!
```

## Install

```
pip install parseq
```

Requires Python 3.10+. No runtime dependencies.

## Why parseq?

argparse is powerful but verbose. Typer and click are great but bring dependencies and their own opinions. parseq tries to do one thing: if your function has type hints, you get a CLI for free.

## Features

- Single decorator: `@command`.
- Type-driven coercion: `str`, `int`, `float`, `bool`, `Path`, `Literal`, `Enum`, `list[T]`, `Optional[T]`.
- Positional args ↔ positional parameters.
- Keyword-only args ↔ `--flags`.
- Docstrings become `--help` text.
- Zero dependencies.

## Docs

See [docs/guide.md](docs/guide.md). Contributing: see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT.
