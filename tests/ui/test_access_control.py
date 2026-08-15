from __future__ import annotations

import pytest

from cases import UI_CASES
from desertcat_ui.execution.executor import MissingUiPrerequisite
from desertcat_ui.models import Viewport


DESKTOP = Viewport("desktop", 1366, 768)
AUTH_CASES = [pytest.param(case, id=case.case_id) for case in UI_CASES if case.requires_auth]
PERMISSION_CASES = [pytest.param(case, id=case.case_id) for case in UI_CASES if case.permission]


@pytest.mark.ui
@pytest.mark.access_control
@pytest.mark.parametrize("case", AUTH_CASES)
def test_unauthenticated_user_is_redirected(browser, ui_executor, case):
    context = browser.new_context()
    page = context.new_page()
    try:
        ui_executor.verify_unauthenticated_guard(page, case, DESKTOP)
    finally:
        context.close()


@pytest.mark.ui
@pytest.mark.access_control
@pytest.mark.parametrize("case", PERMISSION_CASES)
def test_user_without_page_permission_is_rejected(browser, ui_executor, case):
    context = browser.new_context()
    page = context.new_page()
    try:
        try:
            ui_executor.verify_permission_guard(page, case, DESKTOP)
        except MissingUiPrerequisite as exc:
            pytest.skip(str(exc))
    finally:
        context.close()
