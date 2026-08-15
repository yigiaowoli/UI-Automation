from __future__ import annotations

import re
from typing import Any

from desertcat_ui.models import UiCase


class MissingRouteParameter(ValueError):
    pass


PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}|:([A-Za-z][A-Za-z0-9_]*)")


class RouteResolver:
    def __init__(self, base_url: str, ids: dict[str, Any], overrides: dict[str, str]) -> None:
        self._base_url = base_url.rstrip("/")
        self._ids = ids
        self._overrides = overrides

    def url_for(self, case: UiCase) -> str | None:
        route = self._overrides.get(case.case_id, case.route)
        if route is None:
            return None
        missing: list[str] = []

        def replace(match: re.Match[str]) -> str:
            key = match.group(1) or match.group(2)
            if key not in self._ids:
                missing.append(key)
                return match.group(0)
            return str(self._ids[key])

        route = PLACEHOLDER_RE.sub(replace, route)
        if missing:
            names = ", ".join(sorted(set(missing)))
            raise MissingRouteParameter(f"{case.case_id} is missing route parameter(s): {names}")
        route = route if route.startswith("/") else f"/{route}"
        return f"{self._base_url}/#{route}"
