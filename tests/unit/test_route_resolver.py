from __future__ import annotations

import unittest

from desertcat_ui.execution.route_resolver import MissingRouteParameter, RouteResolver
from desertcat_ui.models import UiCase


class RouteResolverTest(unittest.TestCase):
    def test_resolves_hash_route_and_identifier(self) -> None:
        resolver = RouteResolver("http://frontend.test", {"userId": 88}, {})
        case = UiCase("DC-UI-X", "用户", "用户主页", "高", "/user/:userId", "User.vue", False, None, ".page", "user")
        self.assertEqual(resolver.url_for(case), "http://frontend.test/#/user/88")

    def test_reports_missing_identifier(self) -> None:
        resolver = RouteResolver("http://frontend.test", {}, {})
        case = UiCase("DC-UI-X", "用户", "用户主页", "高", "/user/:userId", "User.vue", False, None, ".page", "user")
        with self.assertRaisesRegex(MissingRouteParameter, "DC-UI-X.*userId"):
            resolver.url_for(case)


if __name__ == "__main__":
    unittest.main()
