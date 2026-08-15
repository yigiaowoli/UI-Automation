from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Mapping

from desertcat_ui.models import Viewport


class UiConfigurationError(ValueError):
    pass


@dataclass(frozen=True)
class UiSettings:
    base_url: str = "http://127.0.0.1:5173"
    auth_token: str = ""
    user_info: dict[str, Any] = field(default_factory=lambda: {"id": 1, "username": "UI自动化用户", "permissions": []})
    ids: dict[str, Any] = field(default_factory=lambda: {"id": 1, "userId": 1, "postId": 1})
    route_overrides: dict[str, str] = field(default_factory=dict)
    timeout_ms: int = 30_000
    ignore_https_errors: bool = False
    require_authenticated_flows: bool = True
    required_permissions: tuple[str, ...] = (
        "page:echarts",
        "page:admin-feedback",
        "page:admin-links",
        "page:admin-announcement",
        "page:admin-permissions",
    )
    artifacts_dir: Path = Path("reports")
    viewports: tuple[Viewport, ...] = (
        Viewport("desktop", 1366, 768),
        Viewport("mobile", 390, 844),
    )

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "UiSettings":
        source = os.environ if env is None else env
        return cls(
            base_url=source.get("UI_BASE_URL", cls.base_url).rstrip("/"),
            auth_token=source.get("TEST_AUTH_TOKEN", "").strip(),
            user_info=json.loads(source.get("TEST_USER_INFO_JSON", '{"id":1,"username":"UI自动化用户","permissions":[]}')),
            ids=json.loads(source.get("TEST_IDS_JSON", '{"id":1,"userId":1,"postId":1}')),
            route_overrides=json.loads(source.get("UI_ROUTE_OVERRIDES_JSON", "{}")),
            timeout_ms=int(source.get("UI_TIMEOUT_MS", "30000")),
            ignore_https_errors=source.get("UI_IGNORE_HTTPS_ERRORS", "false").lower() in {"1", "true", "yes", "on"},
            require_authenticated_flows=source.get("UI_REQUIRE_AUTH", "true").lower() in {"1", "true", "yes", "on"},
            required_permissions=tuple(
                permission.strip()
                for permission in source.get(
                    "UI_REQUIRED_PERMISSIONS",
                    "page:echarts,page:admin-feedback,page:admin-links,page:admin-announcement,page:admin-permissions",
                ).split(",")
                if permission.strip()
            ),
            artifacts_dir=Path(source.get("ARTIFACTS_DIR", "reports")),
        )

    def validate_runtime(self) -> None:
        if not self.require_authenticated_flows:
            return
        if not self.auth_token:
            raise UiConfigurationError(
                "TEST_AUTH_TOKEN is required; set UI_REQUIRE_AUTH=false only for an intentional public-only run"
            )
        configured = set(self.user_info.get("permissions") or [])
        missing = set(self.required_permissions) - configured
        if missing:
            raise UiConfigurationError(
                "TEST_USER_INFO_JSON is missing required UI permissions: " + ", ".join(sorted(missing))
            )

    def diagnostic(self) -> str:
        values = asdict(self)
        values["auth_token"] = "***" if self.auth_token else "<unset>"
        return json.dumps(values, ensure_ascii=False, default=str, sort_keys=True)
