# tests/test_deploy.py
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import deploy


class TestDeploy(unittest.TestCase):
    def run_deploy(self, root, *extra):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = deploy.main(
                ["--deploy-root", root, "--build-id", "test", "--commit", "abc123", *extra]
            )
        return code, buffer.getvalue()

    def test_deploy_copies_runs_and_verifies(self):
        with tempfile.TemporaryDirectory() as root:
            code, output = self.run_deploy(root)
            current = Path(root) / "current"
            self.assertEqual(code, 0)
            self.assertIn("Verification      : PASSED", output)
            self.assertTrue((current / "app.py").is_file())
            self.assertIn("commit: abc123", (current / "VERSION.txt").read_text(encoding="utf-8"))
            self.assertTrue((Path(root) / "releases" / "build-test" / "app.py").is_file())

    def test_redeploy_replaces_previous_release(self):
        with tempfile.TemporaryDirectory() as root:
            self.assertEqual(self.run_deploy(root)[0], 0)
            code, _ = self.run_deploy(root)
            self.assertEqual(code, 0)
            history = (Path(root) / "deployments.log").read_text(encoding="utf-8")
            self.assertEqual(history.count("Verification      : PASSED"), 2)

    def test_wrong_expected_output_fails(self):
        with tempfile.TemporaryDirectory() as root:
            report = Path(root) / "out" / "verification.txt"
            code, output = self.run_deploy(
                root, "--expected", "Something else", "--report", str(report)
            )
            self.assertEqual(code, 1)
            self.assertIn("Verification      : FAILED", output)
            self.assertTrue(report.is_file())


if __name__ == "__main__":
    unittest.main()
