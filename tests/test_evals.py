from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_eval(name: str):
    path = ROOT / "evals" / name
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EvalTraceTests(unittest.TestCase):
    def test_device_check_ignores_heredoc_payload(self) -> None:
        for name in ("codex_bootstrap_e2e.py", "claude_bootstrap_e2e.py"):
            module = load_eval(name)
            command = """python3 - <<'PY'\ntext = 'android-emu claim phone'\ntext2 = 'adb devices'\nPY\necho done"""
            scrubbed = module.strip_heredoc_bodies(command)
            self.assertNotRegex(scrubbed, module.DEVICE_COMMAND, name)

    def test_device_check_still_detects_real_invocations(self) -> None:
        examples = (
            "adb devices",
            "ANDROID_SERIAL=emulator-5554 adb shell getprop",
            "android-emu claim pixel",
            "echo ready && emulator @Pixel",
        )
        for name in ("codex_bootstrap_e2e.py", "claude_bootstrap_e2e.py"):
            module = load_eval(name)
            for command in examples:
                with self.subTest(eval=name, command=command):
                    self.assertRegex(module.strip_heredoc_bodies(command), module.DEVICE_COMMAND)


if __name__ == "__main__":
    unittest.main(verbosity=2)
