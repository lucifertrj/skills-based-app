# Audit: parseq Library README

**Document type**: Open-source library README (marketing + quick-start reference)
**Audit applicability**: Partial. A README is not a spec or design document, so a full pre-implementation audit does not cleanly apply. However, the README *is* the contract between the library and its users — it defines the public API surface, promises, and constraints that the implementation must satisfy. Auditing it before writing code is legitimate and useful: gaps here become mismatched expectations later.

---

## Findings

### 1. API contract is under-specified for edge cases
The `@command` decorator is the entire public API, yet its behavior under failure conditions is not documented. What happens when the user passes a wrong type? Does parseq print a message and exit, raise an exception, or defer to Python? This matters immediately at implementation time.

### 2. Type support list may create false promises
The Features section lists `Literal`, `Enum`, `list[T]`, and `Optional[T]` as supported. These are significantly harder to implement than `str`/`int`/`float`. Listing them without any caveats (e.g., nesting depth, mutual exclusions) sets a hard expectation. If `list[Enum]` or `Optional[list[T]]` is out of scope, the README should say so.

### 3. Multi-command / subcommand story is absent
The one-liner "if your function has type hints, you get a CLI for free" implies a single-function model. Real CLIs often need subcommands. Whether parseq supports multiple `@command`-decorated functions, a `main()` dispatcher, or intentionally excludes this is unstated — implementers will design the wrong architecture if they guess.

### 4. Keyword-only vs positional mapping needs a worked example
The feature bullet "Positional args ↔ positional parameters / Keyword-only args ↔ --flags" is stated but not demonstrated beyond the `greet` example. Edge cases (e.g., `*args`, default positional values, required flags) are not shown and could be interpreted differently by different implementers.

### 5. No versioning or stability signal
There is no mention of semantic versioning intent, stability guarantees, or whether the API is considered stable. For a v0.x library this is forgivable, but it should be explicit.

---

## Verdict: REVISE before implementation

The README is clean and readable, but it leaves enough API surface undefined that two engineers could implement meaningfully different behavior and both claim fidelity to this document. Revise the edge-case behavior and type-support scope before cutting code.

---

## Three Questions for the Author

1. **Error handling contract**: When argument parsing fails (wrong type, missing required positional), what is the intended user-facing behavior — `sys.exit(2)` with a message (argparse style), a raised `ParseqError`, or something else?

2. **Compound type depth**: Is `list[T]` support limited to flat lists of primitives, or does the implementation need to handle `list[Enum]`, `Optional[list[int]]`, and similar nested constructs?

3. **Multi-command support**: Is a single `@command` per entry point the intended model indefinitely, or is a subcommand/dispatch API planned? The answer changes the internal architecture substantially.
