from __future__ import annotations

from pathlib import Path

from desertcat_ui.models import UiCase


CONTRACTS: dict[str, tuple[str, ...]] = {
    "register_component": (
        'v-model="username"', 'v-model="email"', 'v-model="code"', 'v-model="password"',
        'v-model="confirmPwd"', "handleRegister", "sendCode",
    ),
    "forgot_component": (
        'v-model="email"', 'v-model="code"', 'v-model="newPassword"', 'v-model="confirmPwd"',
        "handleReset", "sendCode",
    ),
}


class ComponentContract:
    def __init__(self, frontend_root: Path) -> None:
        self._frontend_root = frontend_root

    def verify(self, case: UiCase) -> None:
        component = self._frontend_root / "src" / "views" / case.component
        if not component.exists():
            raise AssertionError(f"Component file does not exist: {component}")
        source = component.read_text(encoding="utf-8")
        required = (case.root_selector.removeprefix("."), "<input", "<button", *CONTRACTS.get(case.action_key, ()))
        missing = [token for token in required if token not in source]
        if missing:
            raise AssertionError(f"{case.case_id} component contract is missing: {', '.join(missing)}")
