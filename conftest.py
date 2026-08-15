from __future__ import annotations

import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from desertcat_ui.config import UiSettings
from desertcat_ui.execution import UiCaseExecutor


load_dotenv(ROOT / ".env")


@pytest.fixture(scope="session")
def ui_settings() -> UiSettings:
    settings = UiSettings.from_env()
    settings.validate_runtime()
    return settings


@pytest.fixture(scope="session")
def ui_executor(ui_settings: UiSettings) -> UiCaseExecutor:
    return UiCaseExecutor(ui_settings, (ROOT / "../felisbieti-web").resolve(), ROOT)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, ui_settings: UiSettings):
    return {
        **browser_context_args,
        "ignore_https_errors": ui_settings.ignore_https_errors,
        "record_video_dir": str(ROOT / ui_settings.artifacts_dir / "videos"),
    }
