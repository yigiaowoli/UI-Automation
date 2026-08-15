from __future__ import annotations

import pytest

from desertcat_ui.execution.executor import MissingUiPrerequisite
from desertcat_ui.models import UiCase, Viewport


VIEWPORTS = (
    pytest.param(Viewport("desktop", 1366, 768), id="desktop-1366x768"),
    pytest.param(Viewport("mobile", 390, 844), id="mobile-390x844"),
)


def case_params(cases: list[UiCase]) -> list[pytest.ParameterSet]:
    return [
        pytest.param(case, id=case.case_id, marks=pytest.mark.p0 if case.priority == "高" else pytest.mark.p1)
        for case in cases
    ]


def verify_ui_case(ui_executor, page, case: UiCase, viewport: Viewport) -> None:
    try:
        result = ui_executor.execute(page, case, viewport)
    except MissingUiPrerequisite as exc:
        pytest.skip(str(exc))
    if result.route is None:
        pytest.xfail("Vue component has no product route; source contract verified, browser flow intentionally not claimed")
    assert result.case_id == case.case_id
    assert result.viewport == viewport.name
