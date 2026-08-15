import pytest

from cases import UI_CASES
from tests.ui._contract import VIEWPORTS, case_params, verify_ui_case


ADMIN_IDS = {*(f"DC-UI-{i:03d}" for i in range(20, 24)), "DC-UI-025", "DC-UI-026"}
CASES = [case for case in UI_CASES if case.case_id in ADMIN_IDS]


@pytest.mark.ui
@pytest.mark.admin
@pytest.mark.parametrize("viewport", VIEWPORTS)
@pytest.mark.parametrize("case", case_params(CASES))
def test_account_admin_page_contract(ui_executor, page, case, viewport):
    verify_ui_case(ui_executor, page, case, viewport)
