import pytest

from cases import UI_CASES
from tests.ui._contract import VIEWPORTS, case_params, verify_ui_case


COMMUNITY_IDS = {*(f"DC-UI-{i:03d}" for i in range(7, 11)), "DC-UI-024"}
CASES = [case for case in UI_CASES if case.case_id in COMMUNITY_IDS]


@pytest.mark.ui
@pytest.mark.community
@pytest.mark.parametrize("viewport", VIEWPORTS)
@pytest.mark.parametrize("case", case_params(CASES))
def test_community_page_contract(ui_executor, page, case, viewport):
    verify_ui_case(ui_executor, page, case, viewport)
