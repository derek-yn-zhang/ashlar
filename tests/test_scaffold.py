import json
import os
import tempfile

import pytest

from kerf.scaffold import scaffold_mcp, scaffold_project, scaffold_tool, scaffold_workflow


class TestScaffoldProject:
    def test_creates_structure(self):
        with tempfile.TemporaryDirectory() as d:
            scaffold_project(d)
            assert os.path.exists(os.path.join(d, ".kerf"))
            assert os.path.isdir(os.path.join(d, "workflows"))
            assert os.path.isdir(os.path.join(d, "tools"))
            assert os.path.isdir(os.path.join(d, "schemas"))
            assert os.path.isdir(os.path.join(d, "logs"))
            assert os.path.exists(os.path.join(d, "kerf.toml"))

    def test_creates_example_workflows(self):
        with tempfile.TemporaryDirectory() as d:
            scaffold_project(d)
            for name in ["summarize", "classify", "extract", "clean"]:
                wf_path = os.path.join(d, "workflows", f"{name}.json")
                assert os.path.exists(wf_path)
                with open(wf_path) as f:
                    json.load(f)  # valid JSON

    def test_no_tool_file_scaffolded(self):
        """Builtins provide normalize_text; no need to scaffold a tool file."""
        with tempfile.TemporaryDirectory() as d:
            scaffold_project(d)
            tool_files = [
                f for f in os.listdir(os.path.join(d, "tools"))
                if f.endswith(".py") and not f.startswith("_")
            ]
            assert tool_files == []

    def test_double_init_raises(self):
        with tempfile.TemporaryDirectory() as d:
            scaffold_project(d)
            with pytest.raises(FileExistsError):
                scaffold_project(d)


class TestScaffoldWorkflow:
    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "workflows"))
            scaffold_workflow("test_wf", d)
            path = os.path.join(d, "workflows", "test_wf.json")
            assert os.path.exists(path)
            with open(path) as f:
                wf = json.load(f)
            assert "task_type" in wf

    def test_duplicate_raises(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "workflows"))
            scaffold_workflow("test_wf", d)
            with pytest.raises(FileExistsError):
                scaffold_workflow("test_wf", d)


class TestScaffoldTool:
    def test_creates_valid_python(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "tools"))
            scaffold_tool("my_tool", d)
            path = os.path.join(d, "tools", "my_tool.py")
            assert os.path.exists(path)
            with open(path) as f:
                content = f.read()
            assert "def my_tool(input_data, params)" in content
            assert 'register_tool("my_tool"' in content

    def test_hyphenated_name(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "tools"))
            scaffold_tool("strip-html", d)
            path = os.path.join(d, "tools", "strip-html.py")
            with open(path) as f:
                content = f.read()
            # Function name uses underscores
            assert "def strip_html(input_data, params)" in content
            # Registration uses original hyphenated name
            assert 'register_tool("strip-html"' in content

    def test_duplicate_raises(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "tools"))
            scaffold_tool("my_tool", d)
            with pytest.raises(FileExistsError):
                scaffold_tool("my_tool", d)


class TestScaffoldMcp:
    def test_creates_config(self):
        with tempfile.TemporaryDirectory() as d:
            scaffold_mcp("test_server", d)
            path = os.path.join(d, "mcp.json")
            assert os.path.exists(path)
            with open(path) as f:
                config = json.load(f)
            assert "test_server" in config["mcpServers"]

    def test_appends_to_existing(self):
        with tempfile.TemporaryDirectory() as d:
            scaffold_mcp("server1", d)
            scaffold_mcp("server2", d)
            with open(os.path.join(d, "mcp.json")) as f:
                config = json.load(f)
            assert "server1" in config["mcpServers"]
            assert "server2" in config["mcpServers"]

    def test_duplicate_raises(self):
        with tempfile.TemporaryDirectory() as d:
            scaffold_mcp("server1", d)
            with pytest.raises(FileExistsError):
                scaffold_mcp("server1", d)
