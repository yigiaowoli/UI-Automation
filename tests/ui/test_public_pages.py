import pytest

from cases import UI_CASES
from tests.ui._contract import VIEWPORTS, case_params, verify_ui_case


PUBLIC_IDS = {*(f"DC-UI-{i:03d}" for i in range(1, 7)), "DC-UI-011", "DC-UI-012", *(f"DC-UI-{i:03d}" for i in range(16, 20)), *(f"DC-UI-{i:03d}" for i in range(27, 31))}
CASES = [case for case in UI_CASES if case.case_id in PUBLIC_IDS]


@pytest.mark.ui
@pytest.mark.public
@pytest.mark.parametrize("viewport", VIEWPORTS)
@pytest.mark.parametrize("case", case_params(CASES))
def test_public_page_contract(ui_executor, page, case, viewport):
    verify_ui_case(ui_executor, page, case, viewport)
