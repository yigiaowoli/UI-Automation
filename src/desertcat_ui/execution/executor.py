from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from desertcat_ui.config.settings import UiSettings
from desertcat_ui.execution.component_contract import ComponentContract
from desertcat_ui.execution.route_resolver import RouteResolver
from desertcat_ui.models import UiCase, Viewport
from desertcat_ui.pages.registry import PageRegistry

if TYPE_CHECKING:
    from playwright.sync_api import Page


@dataclass(frozen=True)
class UiExecutionResult:
    case_id: str
    viewport: str
    route: str | None


class MissingUiPrerequisite(RuntimeError):
    pass


class UiCaseExecutor:
    """Deep UI module: login state, guards, page object, diagnostics and recovery checks."""

    def __init__(self, settings: UiSettings, frontend_root: Path, project_root: Path) -> None:
        self._settings = settings
        self._resolver = RouteResolver(settings.base_url, settings.ids, settings.route_overrides)
        self._components = ComponentContract(frontend_root)
        self._registry = PageRegistry()
        self._project_root = project_root

    def execute(self, page: "Page", case: UiCase, viewport: Viewport) -> UiExecutionResult:
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

        url = self._resolver.url_for(case)
        if url is None:
            self._components.verify(case)
            return UiExecutionResult(case.case_id, viewport.name, None)

        self._install_identity(page)
        page.set_viewport_size({"width": viewport.width, "height": viewport.height})
        console_errors: list[str] = []
        page_errors: list[str] = []
        failed_api: list[str] = []
        page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
        page.on("pageerror", lambda error: page_errors.append(str(error)))
        page.on(
            "response",
            lambda response: failed_api.append(f"{response.status} {response.url}")
            if "/api/" in response.url and response.status >= 500
            else None,
        )
        artifact = self._project_root / self._settings.artifacts_dir / "failures" / (
            f"{case.case_id}-{viewport.name}.png"
        )
        artifact.parent.mkdir(parents=True, exist_ok=True)
        try:
            response = page.goto(url, wait_until="domcontentloaded", timeout=self._settings.timeout_ms)
            try:
                page.wait_for_load_state("networkidle", timeout=8_000)
            except PlaywrightTimeoutError:
                pass
            if response is not None and response.status >= 500:
                raise AssertionError(f"Document returned HTTP {response.status}")
            if case.requires_auth and not self._settings.auth_token:
                raise MissingUiPrerequisite(f"{case.case_id} requires TEST_AUTH_TOKEN for its positive flow")
            permissions = set(self._settings.user_info.get("permissions") or [])
            if case.permission and case.permission not in permissions:
                raise MissingUiPrerequisite(
                    f"{case.case_id} requires permission {case.permission!r} for its positive flow"
                )

            page_object = self._registry.create(page, case)
            page_object.assert_loaded()
            page_object.exercise_primary_flow()
            self._assert_layout(page)
            page.reload(wait_until="domcontentloaded", timeout=self._settings.timeout_ms)
            page_object.assert_loaded()
            assert not page_errors, "Unhandled page errors: " + " | ".join(page_errors)
            assert not console_errors, "Console errors: " + " | ".join(console_errors)
            assert not failed_api, "Server-side API failures: " + " | ".join(failed_api)
            return UiExecutionResult(case.case_id, viewport.name, page.url)
        except Exception:
            page.screenshot(path=artifact, full_page=True)
            raise

    def verify_unauthenticated_guard(self, page: "Page", case: UiCase, viewport: Viewport) -> None:
        from playwright.sync_api import expect

        url = self._resolver.url_for(case)
        if not url or not case.requires_auth:
            raise ValueError(f"{case.case_id} is not an authenticated route")
        page.set_viewport_size({"width": viewport.width, "height": viewport.height})
        page.goto(url, wait_until="domcontentloaded", timeout=self._settings.timeout_ms)
        expect(page).to_have_url(re.compile(r"#/login\?redirect="))

    def verify_permission_guard(self, page: "Page", case: UiCase, viewport: Viewport) -> None:
        from playwright.sync_api import expect

        if not self._settings.auth_token:
            raise MissingUiPrerequisite("TEST_AUTH_TOKEN is required to verify permission denial")
        if not case.permission:
            raise ValueError(f"{case.case_id} has no page permission")
        restricted_user = {**self._settings.user_info, "permissions": []}
        payload = json.dumps(
            {"token": self._settings.auth_token, "userInfo": restricted_user},
            ensure_ascii=False,
        )
        page.add_init_script(
            f"""(() => {{ const payload = {payload}; localStorage.setItem('token', payload.token);
            localStorage.setItem('userInfo', JSON.stringify(payload.userInfo)); }})();"""
        )
        page.set_viewport_size({"width": viewport.width, "height": viewport.height})
        url = self._resolver.url_for(case)
        if not url:
            raise ValueError(f"{case.case_id} has no routable permission page")
        page.goto(url, wait_until="domcontentloaded", timeout=self._settings.timeout_ms)
        expect(page).to_have_url(re.compile(r"#/home$"))

    def _install_identity(self, page: "Page") -> None:
        if not self._settings.auth_token:
            return
        payload = json.dumps(
            {"token": self._settings.auth_token, "userInfo": self._settings.user_info},
            ensure_ascii=False,
        )
        page.add_init_script(
            f"""(() => {{ const payload = {payload}; localStorage.setItem('token', payload.token);
            localStorage.setItem('userInfo', JSON.stringify(payload.userInfo)); }})();"""
        )

    @staticmethod
    def _assert_layout(page: "Page") -> None:
        metrics = page.evaluate(
            """() => ({ width: document.documentElement.clientWidth,
            scroll: document.documentElement.scrollWidth,
            height: document.body.getBoundingClientRect().height })"""
        )
        assert metrics["scroll"] <= metrics["width"] + 2, (
            f"Horizontal overflow: {metrics['scroll']}px > {metrics['width']}px"
        )
        assert metrics["height"] > 0, "Document body has zero height"
