from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from desertcat_ui.execution.component_contract import ComponentContract
from desertcat_ui.models import UiCase


class ComponentContractTest(unittest.TestCase):
    def test_reports_missing_registration_binding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            component = root / "src" / "views" / "Register.vue"
            component.parent.mkdir(parents=True)
            component.write_text('<div class="reg-page"><input><button></button></div>', encoding="utf-8")
            case = UiCase(
                "DC-UI-029", "注册", "注册", "高", None, "Register.vue", False, None,
                ".reg-page", "register_component",
            )
            with self.assertRaisesRegex(AssertionError, 'v-model="username"'):
                ComponentContract(root).verify(case)


if __name__ == "__main__":
    unittest.main()
