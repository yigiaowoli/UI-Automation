from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.sync_api import Page


@dataclass(frozen=True)
class PageDescriptor:
    root: str
    visible: tuple[str, ...] = ()
    input_selector: str | None = None
    input_value: str = "企业自动化测试"
    additional_fills: tuple[tuple[str, str], ...] = ()
    check_selector: str | None = None
    click_selector: str | None = None
    after_click_visible: str | None = None
    count_selector: str | None = None
    minimum_count: int = 0
    exact_count: int | None = None
    initially_disabled: str | None = None
    enabled_after_input: str | None = None


class BasePageObject:
    """Reusable page-object implementation for stable selector contracts."""

    def __init__(self, page: "Page", descriptor: PageDescriptor) -> None:
        self.page = page
        self.descriptor = descriptor

    def assert_loaded(self) -> None:
        from playwright.sync_api import expect

        expect(self.page.locator(self.descriptor.root)).to_be_visible()
        for selector in self.descriptor.visible:
            expect(self.page.locator(selector).first).to_be_visible()

    def exercise_primary_flow(self) -> None:
        from playwright.sync_api import expect

        descriptor = self.descriptor
        if descriptor.initially_disabled:
            expect(self.page.locator(descriptor.initially_disabled).first).to_be_disabled()
        if descriptor.input_selector:
            field = self.page.locator(descriptor.input_selector).first
            expect(field).to_be_visible()
            field.fill(descriptor.input_value)
        for selector, value in descriptor.additional_fills:
            field = self.page.locator(selector).first
            expect(field).to_be_visible()
            field.fill(value)
        if descriptor.check_selector:
            checkbox = self.page.locator(descriptor.check_selector).first
            expect(checkbox).to_be_visible()
            checkbox.check()
        if descriptor.click_selector:
            target = self.page.locator(descriptor.click_selector).first
            expect(target).to_be_enabled()
            target.click()
        if descriptor.enabled_after_input:
            expect(self.page.locator(descriptor.enabled_after_input).first).to_be_enabled()
        if descriptor.after_click_visible:
            expect(self.page.locator(descriptor.after_click_visible).first).to_be_visible()
        if descriptor.count_selector:
            count = self.page.locator(descriptor.count_selector).count()
            if descriptor.exact_count is not None:
                assert count == descriptor.exact_count, (
                    f"Expected {descriptor.exact_count} nodes for {descriptor.count_selector}, got {count}"
                )
            else:
                assert count >= descriptor.minimum_count, (
                    f"Expected at least {descriptor.minimum_count} nodes for {descriptor.count_selector}, got {count}"
                )
