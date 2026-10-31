import contextlib
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("factory", Path(__file__).resolve().parents[1] / "tools/factory.py")
factory = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(factory)


class FactoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(factory.ROOT / "templates", self.root / "templates")

    def init(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return factory.init_project(self.root, "example", "web")

    def manifest(self, path, checks):
        (path / "factory.project.json").write_text(json.dumps({
            "version": 1, "kind": "web", "checks": checks}), encoding="utf-8")

    def run_verify(self, only=None):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = factory.verify(self.root, "example", only)
        return code, output.getvalue()

    def test_init_all_kinds_and_no_overwrite(self):
        for kind in factory.KINDS:
            path = factory.init_project(self.root, f"example-{kind}", kind)
            data = json.loads((path / "factory.project.json").read_text())
            self.assertEqual(data["kind"], kind)
            self.assertEqual(set(data["checks"]), set(factory.GATES))
            self.assertTrue((path / "docs/VERIFICATION.md").is_file())
            with self.assertRaises(ValueError):
                factory.init_project(self.root, f"example-{kind}", kind)

    def test_reject_bad_project_paths(self):
        for slug in ("../escape", "a/b", "C:\\escape", "", "UPPER", "a b"):
            with self.assertRaises(ValueError):
                factory.project_path(self.root, slug)

    def test_unconfigured_checks_are_not_passes(self):
        self.init()
        code, output = self.run_verify()
        self.assertEqual(code, 2)
        self.assertEqual(output.count("NOT RUN"), len(factory.GATES))
        self.assertNotIn("PASS", output)

    def test_execute_real_commands_in_project_cwd(self):
        path = self.init()
        checks = {key: {"argv": [sys.executable, "-c", "from pathlib import Path; assert Path('AGENTS.md').is_file()"]}
                  for key in factory.GATES}
        self.manifest(path, checks)
        code, output = self.run_verify()
        self.assertEqual(code, 0)
        self.assertEqual(output.count("PASS"), len(factory.GATES))

    def test_fail_stops_later_checks(self):
        path = self.init()
        checks = dict.fromkeys(factory.GATES)
        checks["lint"] = {"argv": [sys.executable, "-c", "raise SystemExit(7)"]}
        checks["test"] = {"argv": [sys.executable, "-c", "from pathlib import Path; Path('unexpected').touch()"]}
        self.manifest(path, checks)
        code, output = self.run_verify()
        self.assertEqual(code, 1)
        self.assertIn("exit 7", output)
        self.assertFalse((path / "unexpected").exists())

    def test_missing_tool_is_blocked(self):
        path = self.init()
        checks = dict.fromkeys(factory.GATES)
        checks["lint"] = {"argv": ["factory-test-command-does-not-exist-09234"]}
        self.manifest(path, checks)
        code, output = self.run_verify()
        self.assertEqual(code, 2)
        self.assertIn("BLOCKED", output)

    def test_timeout_is_blocked(self):
        path = self.init()
        checks = dict.fromkeys(factory.GATES)
        checks["lint"] = {"argv": [sys.executable, "-c", "import time; time.sleep(10)"],
                          "timeout_seconds": 1}
        self.manifest(path, checks)
        code, output = self.run_verify()
        self.assertEqual(code, 2)
        self.assertIn("BLOCKED", output)

    def test_validate_whole_plan_before_running_commands(self):
        path = self.init()
        checks = dict.fromkeys(factory.GATES)
        checks["lint"] = {"argv": [sys.executable, "-c", "from pathlib import Path; Path('unexpected').touch()"]}
        checks["build"] = {"argv": "invalid string instead of array"}
        self.manifest(path, checks)
        with self.assertRaises(ValueError):
            self.run_verify()
        self.assertFalse((path / "unexpected").exists())

    @unittest.skipUnless(shutil.which("npm"), "npm not on PATH")
    def test_npm_executable_on_current_platform(self):
        path = self.init()
        checks = dict.fromkeys(factory.GATES)
        checks["build"] = {"argv": [shutil.which("npm"), "--version"]}
        self.manifest(path, checks)
        code, output = self.run_verify("build")
        self.assertEqual(code, 0)
        self.assertIn("PASS build", output)

    def test_reject_escape_and_invalid_commands(self):
        path = self.init()
        for spec in ({"argv": "echo ok"}, {"argv": []},
                     {"argv": ["python"], "cwd": "../.."},
                     {"argv": ["python"], "timeout_seconds": -1},
                     {"not_applicable": ""}):
            with self.assertRaises(ValueError):
                factory.check_command(path, spec)

    def test_na_is_explicit_and_only_runs_selected_check(self):
        path = self.init()
        checks = dict.fromkeys(factory.GATES)
        checks["typecheck"] = {"not_applicable": "No typed source in this fixture"}
        self.manifest(path, checks)
        code, output = self.run_verify("typecheck")
        self.assertEqual(code, 0)
        self.assertIn("N/A typecheck", output)
        self.assertNotIn("PASS", output)
        self.assertNotIn("NOT RUN", output)

    def test_agent_sync_roundtrip_and_detect_drift(self):
        shutil.copytree(factory.ROOT / ".github/agents", self.root / ".github/agents")
        factory.sync_agents(self.root)
        factory.sync_agents(self.root, check=True)
        role = self.root / ".codex/agents/mobile.toml"
        self.assertIn("developer_instructions", factory.tomllib.loads(role.read_text()))
        role.write_text("# stale", encoding="utf-8")
        with self.assertRaises(ValueError):
            factory.sync_agents(self.root, check=True)


if __name__ == "__main__":
    unittest.main()
