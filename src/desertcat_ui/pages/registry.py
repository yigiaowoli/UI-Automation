from __future__ import annotations

from typing import TYPE_CHECKING

from desertcat_ui.models import UiCase
from desertcat_ui.pages.base import BasePageObject, PageDescriptor

if TYPE_CHECKING:
    from playwright.sync_api import Page


DESCRIPTORS: dict[str, PageDescriptor] = {
    "download": PageDescriptor(".download-page", (".download-page .card", ".download-page img")),
    "login": PageDescriptor(
        ".login-page",
        ("#login-email", "#login-code", ".submit-button"),
        "#login-email",
        "ui-automation@example.com",
        additional_fills=(("#login-code", "123456"),),
        check_selector="#login-agreement",
        initially_disabled=".submit-button",
        enabled_after_input=".submit-button",
    ),
    "legal": PageDescriptor(".legal-page", ("h1",), count_selector="section", minimum_count=1),
    "home": PageDescriptor(".home-page", ("h1",), count_selector="a, button", minimum_count=1),
    "feed": PageDescriptor(
        ".feed-container",
        count_selector=".category-button",
        minimum_count=2,
        click_selector=".category-button:nth-child(2)",
        after_click_visible=".category-button.active",
    ),
    "following": PageDescriptor(".follow-page", input_selector=".follow-page input", input_value="自动化"),
    "messages": PageDescriptor(".messages-page", (".chat-frame",)),
    "mine": PageDescriptor(".mine-container", count_selector=".mine-tabs-command button", minimum_count=1),
    "chat": PageDescriptor(".chat-layout", input_selector=".conv-search input", input_value="自动化"),
    "detail": PageDescriptor(
        ".detail-page",
        (".back-btn", ".detail-content, .error-state, .loading-state"),
    ),
    "search": PageDescriptor(
        ".search-page",
        (".s-btn",),
        ".search-bar input",
        "自动化测试",
        click_selector=".s-btn",
        after_click_visible=".results-area, .empty-state",
    ),
    "user_profile": PageDescriptor(".up-page", (".back-btn",)),
    "friends": PageDescriptor(".fl-page", (".add-btn",), count_selector=".fl-tabs .tab-btn", exact_count=2),
    "add_friend": PageDescriptor(
        ".af-page",
        (".af-btn",),
        ".af-input",
        "automation_user",
        click_selector=".af-btn",
        after_click_visible=".af-results, .empty",
    ),
    "tools": PageDescriptor(".tools-page", input_selector=".tools-page input", input_value="OpenAI"),
    "ai_ranking": PageDescriptor(".ranking-page", (".ranking-board",)),
    "ai_guide": PageDescriptor(".guide-page", count_selector=".guide-section", minimum_count=1),
    "ai_chat": PageDescriptor(
        ".chat-wrap",
        input_selector=".chat-wrap textarea",
        input_value="请介绍这个项目",
        initially_disabled=".cf-send",
        enabled_after_input=".cf-send",
    ),
    "echarts": PageDescriptor(".echarts-dashboard", count_selector=".chart-container", exact_count=4),
    "profile": PageDescriptor(
        ".settings-page",
        (".settings-content",),
        count_selector=".settings-nav .nav-item",
        minimum_count=2,
        click_selector=".settings-nav .nav-item:nth-child(2)",
        after_click_visible=".settings-content .section",
    ),
    "feedback": PageDescriptor(".feedback-page", input_selector=".search-input", input_value="自动化"),
    "admin_links": PageDescriptor(
        ".link-mgmt",
        (".page-actions .primary", ".categories-bar"),
        input_selector=".search-input",
        input_value="OpenAI",
        click_selector=".page-actions .primary",
        after_click_visible=".dialog-overlay",
    ),
    "publish": PageDescriptor(
        ".text-studio",
        input_selector=".title-input",
        input_value="企业自动化测试帖子",
        additional_fills=((".body-input", "这是一条由隔离 UI 测试填写但不会提交的内容。"),),
        click_selector=".category-option",
        initially_disabled=".publish-button",
        enabled_after_input=".publish-button",
    ),
    "announcements": PageDescriptor(
        ".admin-announcements",
        (".btn-create",),
        click_selector=".btn-create",
        after_click_visible=".el-dialog",
    ),
    "permissions": PageDescriptor(
        ".admin-permissions", (".sr button",), ".sr input", "automation", click_selector=".sr button"
    ),
    "travel": PageDescriptor(
        ".travel-page",
        (".travel-stats",),
        count_selector="canvas, svg, .map-container, .map-error-box",
        minimum_count=1,
    ),
    "music": PageDescriptor(
        ".music-view",
        input_selector='input[aria-label="搜索歌曲"]',
        input_value="沙漠",
        click_selector=".search-bar button[type=submit]",
        after_click_visible=".track-panel, .state-card",
    ),
}


class PageRegistry:
    def create(self, page: "Page", case: UiCase) -> BasePageObject:
        try:
            descriptor = DESCRIPTORS[case.action_key]
        except KeyError as exc:
            raise LookupError(f"No page object registered for {case.case_id}: {case.action_key}") from exc
        if descriptor.root != case.root_selector and case.action_key != "legal":
            raise AssertionError(
                f"Page object root mismatch for {case.case_id}: catalog={case.root_selector}, object={descriptor.root}"
            )
        return BasePageObject(page, descriptor)
