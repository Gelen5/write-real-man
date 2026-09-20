import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "trends" / "sources"))
import opencli_adapter


class OpenCliAdapterTests(unittest.TestCase):
    @patch("opencli_adapter.shutil.which", return_value="opencli.exe")
    @patch("opencli_adapter.subprocess.run")
    def test_json_error_payload_is_reported_as_source_failure(self, run, _which):
        run.return_value = SimpleNamespace(returncode=0, stdout='{"ok": false, "error": "login needed"}', stderr="")
        with self.assertRaisesRegex(RuntimeError, "login needed"):
            opencli_adapter.run_json("weibo", ["search", "AI"])


if __name__ == "__main__":
    unittest.main()
