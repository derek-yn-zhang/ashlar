import json
import os
from importlib import resources


def _read_template(filename: str) -> str:
    return resources.files("kerf.scaffold").joinpath(filename).read_text()


def scaffold_project(target_dir: str):
    """Create the full kerf project structure in target_dir."""
    # Marker file
    marker = os.path.join(target_dir, ".kerf")
    if os.path.exists(marker):
        raise FileExistsError("Kerf project already initialized here.")
    with open(marker, "w") as f:
        f.write("")

    # Directories
    for dirname in ["workflows", "schemas", "tools", "logs"]:
        dirpath = os.path.join(target_dir, dirname)
        os.makedirs(dirpath, exist_ok=True)

    # Example workflows
    for src, dst in [
        ("example_workflow.json", "summarize.json"),
        ("example_classify.json", "classify.json"),
        ("example_extract.json", "extract.json"),
        ("example_clean.json", "clean.json"),
    ]:
        wf_content = _read_template(src)
        with open(os.path.join(target_dir, "workflows", dst), "w") as f:
            f.write(wf_content)

    # .gitkeep files
    for dirname in ["schemas", "logs"]:
        with open(os.path.join(target_dir, dirname, ".gitkeep"), "w") as f:
            f.write("")

    # Optional config
    config_path = os.path.join(target_dir, "kerf.toml")
    with open(config_path, "w") as f:
        f.write(
            "# Kerf project configuration\n"
            "\n"
            "# [server]\n"
            '# host = "0.0.0.0"\n'
            "# port = 8000\n"
            "\n"
            "# [defaults]\n"
            '# fallback = "retry"\n'
        )


def scaffold_workflow(name: str, project_dir: str):
    """Create a new workflow JSON from template."""
    wf_dir = os.path.join(project_dir, "workflows")
    os.makedirs(wf_dir, exist_ok=True)

    wf_path = os.path.join(wf_dir, f"{name}.json")
    if os.path.exists(wf_path):
        raise FileExistsError(f"Workflow '{name}' already exists.")

    content = _read_template("workflow_template.json")
    with open(wf_path, "w") as f:
        f.write(content)


def scaffold_tool(name: str, project_dir: str):
    """Create a new tool Python file from template."""
    tools_dir = os.path.join(project_dir, "tools")
    os.makedirs(tools_dir, exist_ok=True)

    tool_path = os.path.join(tools_dir, f"{name}.py")
    if os.path.exists(tool_path):
        raise FileExistsError(f"Tool '{name}' already exists.")

    # Hyphens are valid in tool names but not in Python identifiers
    func_name = name.replace("-", "_")

    content = _read_template("tool_template.py")
    content = content.replace("TOOL_NAME", name)
    content = content.replace("tool_name", func_name)
    with open(tool_path, "w") as f:
        f.write(content)


def scaffold_mcp(name: str, project_dir: str):
    """Add an MCP server configuration entry."""
    mcp_path = os.path.join(project_dir, "mcp.json")

    if os.path.exists(mcp_path):
        with open(mcp_path, "r") as f:
            config = json.load(f)
    else:
        config = {"mcpServers": {}}

    servers = config.setdefault("mcpServers", {})
    if name in servers:
        raise FileExistsError(f"MCP server '{name}' already configured.")

    template = json.loads(_read_template("mcp_config_template.json"))
    servers[name] = template

    with open(mcp_path, "w") as f:
        json.dump(config, f, indent=2)
