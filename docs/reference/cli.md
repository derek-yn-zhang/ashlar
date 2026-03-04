# CLI Commands

## `kerf init`

Scaffold a new project in the current directory.

```bash
kerf init
```

Creates `.kerf`, `workflows/`, `schemas/`, `tools/`, `logs/`, and `kerf.toml`. Fails if `.kerf` already exists.

## `kerf run`

Execute a workflow.

```bash
kerf run <workflow> [input] [--debug] [--batch]
```

| Argument / Option | Description |
|---|---|
| `workflow` | Workflow name (matches `workflows/<name>.json`) |
| `input` | Input text (optional — reads stdin if omitted) |
| `--debug` | Show debug output: tool chain execution, prompts, LLM responses |
| `--batch` | Process JSONL input from stdin (one JSON object per line) |

```bash
# argument
kerf run summarize "some text"
```

```bash
# stdin
cat file.txt | kerf run summarize
```

```bash
# debug mode
kerf run --debug summarize "some text"
```

```bash
# batch mode — one JSON result per line
echo '{"input": "text one"}
{"input": "text two"}' | kerf run summarize --batch
```

Prints JSON result to stdout. With `--debug`, also prints the full execution trace to stderr. With `--batch`, each input line produces one output line (JSONL).

Set `KERF_DEBUG=1` to always show tracebacks on errors.

## `kerf serve`

Start the API server.

```bash
kerf serve [--host HOST] [--port PORT]
```

| Option | Default | Description |
|---|---|---|
| `--host` | `0.0.0.0` | Server host |
| `--port` | `8000` | Server port |

## `kerf add`

Scaffold new resources.

```bash
kerf add workflow <name>    # creates workflows/<name>.json
kerf add tool <name>        # creates tools/<name>.py
kerf add mcp <name>         # adds MCP server entry to mcp.json
```

Fails if the resource already exists. `kerf add mcp` creates or appends to `mcp.json` in Claude CLI's native config format.

## `kerf list`

Show available workflows and tools in the current project.

```bash
kerf list
```

## `kerf logs`

View recent execution logs.

```bash
kerf logs [--last N] [--workflow NAME]
```

| Option | Default | Description |
|---|---|---|
| `--last` | `10` | Number of recent logs to show |
| `--workflow` | — | Filter by workflow name |
