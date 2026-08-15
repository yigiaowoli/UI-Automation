from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UiCase:
    case_id: str
    page_name: str
    title: str
    priority: str
    route: str | None
    component: str
    requires_auth: bool
    permission: str | None
    root_selector: str
    action_key: str


@dataclass(frozen=True)
class Viewport:
    name: str
    width: int
    height: int
