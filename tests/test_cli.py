import json
import os
import tempfile
from unittest.mock import patch

from click.testing import CliRunner

from kerf.cli import cli
from kerf.scaffold import scaffold_project


def _make_project():
    """Create a temp kerf project and return the path."""
    d = tempfile.mkdtemp()
    scaffold_project(d)
    return d


class TestBatchMode:
    def test_processes_jsonl(self):
        project_dir = _make_project()
        # Use a tool-chain-only workflow (clean) — no LLM needed
        jsonl = '{"input": "  hello   world  "}\n{"input": "  foo   bar  "}\n'
        runner = CliRunner()
        with patch("kerf.cli.find_project_root", return_value=project_dir):
            result = runner.invoke(cli, ["run", "clean", "--batch"], input=jsonl)
        assert result.exit_code == 0
        lines = [l for l in result.output.strip().split("\n") if l]
        assert len(lines) == 2
        for line in lines:
            parsed = json.loads(line)
            assert "output" in parsed

    def test_skips_empty_lines(self):
        project_dir = _make_project()
        jsonl = '{"input": "hello"}\n\n\n{"input": "world"}\n'
        runner = CliRunner()
        with patch("kerf.cli.find_project_root", return_value=project_dir):
            result = runner.invoke(cli, ["run", "clean", "--batch"], input=jsonl)
        lines = [l for l in result.output.strip().split("\n") if l]
        assert len(lines) == 2

    def test_invalid_json_produces_error(self):
        project_dir = _make_project()
        jsonl = "not json\n"
        runner = CliRunner()
        with patch("kerf.cli.find_project_root", return_value=project_dir):
            result = runner.invoke(cli, ["run", "clean", "--batch"], input=jsonl)
        parsed = json.loads(result.output.strip())
        assert parsed["error"] == "invalid JSON"
        assert parsed["line"] == 1

    def test_missing_input_field(self):
        project_dir = _make_project()
        jsonl = '{"text": "no input key"}\n'
        runner = CliRunner()
        with patch("kerf.cli.find_project_root", return_value=project_dir):
            result = runner.invoke(cli, ["run", "clean", "--batch"], input=jsonl)
        parsed = json.loads(result.output.strip())
        assert "missing 'input' field" in parsed["error"]

    def test_workflow_not_found(self):
        project_dir = _make_project()
        jsonl = '{"input": "hello"}\n'
        runner = CliRunner()
        with patch("kerf.cli.find_project_root", return_value=project_dir):
            result = runner.invoke(cli, ["run", "nonexistent", "--batch"], input=jsonl)
        parsed = json.loads(result.output.strip())
        assert "error" in parsed
