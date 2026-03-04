<p align="center">
  <strong>Kerf</strong><br>
  Declarative workflow engine for Claude CLI
</p>

<p align="center">
  <a href="https://pypi.org/project/kerf/"><img src="https://img.shields.io/pypi/v/kerf" alt="PyPI"></a>
  <a href="https://pypi.org/project/kerf/"><img src="https://img.shields.io/pypi/pyversions/kerf" alt="Python"></a>
  <a href="https://github.com/derek-yn-zhang/kerf/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/kerf" alt="License"></a>
</p>

---

Kerf runs deterministic tools first, calls the LLM only when you need reasoning, and logs every result. Workflows are configured as JSON, custom tools are Python.

- **Deterministic-first:** preprocessing runs without the LLM until you actually need it
- **JSON workflows:** define tool chains, prompt templates, and fallback policies as config
- **Per-workflow fallback:** `retry` the LLM, degrade to `deterministic` output, or `flag` for review
- **Full execution logging:** every run gets a UUID-stamped log you can audit and learn from
- **Auto-discovered tools:** drop a Python file in `tools/`, it gets picked up

## Install

```bash
uv tool install kerf
```

Requires Python 3.10+ and Claude CLI (`claude login`).

## Quick Start

```bash
kerf init
```

```
Kerf project initialized.
```

```bash
kerf run summarize "Kerf is a workflow engine that wraps Claude CLI..."
```

```json
{
  "summary": "Kerf is a declarative workflow engine that wraps Claude CLI for structured, deterministic text processing."
}
```

A workflow is a JSON file in `workflows/`:

```json
{
  "task_type": "summarization",
  "tool_chain": [{ "tool": "normalize_text", "condition": "always_true" }],
  "fallback": "retry"
}
```

`tool_chain` runs deterministic preprocessing. `task_type` sends the result to Claude. `fallback` controls what happens when the LLM fails.

Custom tools go in `tools/` as Python files with a `register(manager)` function:

```python
# tools/uppercase.py
def uppercase(input_data, params):
    return input_data.upper()

def register(manager):
    manager.register_tool("uppercase", uppercase)
```

