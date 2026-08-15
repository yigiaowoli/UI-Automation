import pytest

from cases import UI_CASES
from tests.ui._contract import VIEWPORTS, case_params, verify_ui_case


CASES = [case for case in UI_CASES if 13 <= int(case.case_id[-3:]) <= 15]


@pytest.mark.ui
@pytest.mark.social
@pytest.mark.parametrize("viewport", VIEWPORTS)
@pytest.mark.parametrize("case", case_params(CASES))
def test_social_page_contract(ui_executor, page, case, viewport):
    verify_ui_case(ui_executor, page, case, viewport)
