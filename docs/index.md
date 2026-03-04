# Kerf

Declarative workflow engine for Claude CLI. Deterministic tools run first, the LLM handles reasoning when needed, everything gets logged.

```bash
uv tool install kerf
kerf init && kerf run summarize "Your text here..."
```

## Get Started

- [Installation](getting-started/installation.md): install Kerf and prerequisites
- [Quickstart](getting-started/quickstart.md): scaffold a project, run a workflow, see the output
- [Project Structure](getting-started/project-structure.md): what `kerf init` creates and why

## Guides

- [Writing Workflows](guides/workflows.md): define pipelines as JSON config
- [Writing Tools](guides/tools.md): add deterministic preprocessing steps
- [Using the API Server](guides/server.md): run workflows over HTTP
- [Using MCP Servers](guides/mcp.md): give the LLM access to external data
- [Reading Logs](guides/logs.md): audit execution results and extract patterns

## Concepts

- [How the Engine Works](concepts/engine.md): pipeline execution, tool resolution, fallback handling
- [Fallback Policies](concepts/fallback-policies.md): retry, deterministic, flag
- [Design Decisions](concepts/design-decisions.md): why subprocess, why sync, why named conditions

## Reference

- [CLI Commands](reference/cli.md): every command, flag, and option
- [Workflow Format](reference/workflow-format.md): JSON schema for workflow files
- [Tool API](reference/tool-api.md): function signatures, conditions, registration
- [Built-ins](reference/builtins.md): tools and conditions that ship with Kerf
- [Configuration](reference/configuration.md): `kerf.toml` and project settings
- [Server API](reference/server-api.md): HTTP endpoints
