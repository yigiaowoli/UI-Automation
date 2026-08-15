from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from desertcat_ui.config.settings import UiConfigurationError, UiSettings


class UiSettingsTest(unittest.TestCase):
    def test_defaults_to_two_supported_viewports(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            settings = UiSettings.from_env()
        self.assertEqual([viewport.name for viewport in settings.viewports], ["desktop", "mobile"])

    def test_diagnostic_never_contains_token(self) -> None:
        with patch.dict(os.environ, {"TEST_AUTH_TOKEN": "browser-secret"}, clear=True):
            self.assertNotIn("browser-secret", UiSettings.from_env().diagnostic())

    def test_authenticated_suite_cannot_start_without_token(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(UiConfigurationError, "TEST_AUTH_TOKEN"):
                UiSettings.from_env().validate_runtime()


if __name__ == "__main__":
    unittest.main()
