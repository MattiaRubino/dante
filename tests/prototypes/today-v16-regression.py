"""Smoke/regression test for the standalone LifeOS Today v16 prototype.

Usage:
    python tests/prototypes/today-v16-regression.py /path/to/lifeos-home-oggi-v16.html

Requires Playwright and a Chromium executable.
"""
from __future__ import annotations

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def main() -> int:
    prototype = Path(sys.argv[1] if len(sys.argv) > 1 else "prototypes/today/lifeos-home-oggi-v16.html")
    html = prototype.read_text(encoding="utf-8")
    errors: list[str] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 1000})
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.set_content(html, wait_until="domcontentloaded")
        page.wait_for_timeout(300)

        assert page.locator(".ev-block").count() >= 12
        assert not errors

        title = page.locator('.ev-block[data-ev-block="1"] .js-open-modal')
        title.click()
        assert page.locator("#modal-backdrop.is-open").count() == 1
        page.locator("#modal-close").click()

        body = page.locator('.ev-block[data-ev-block="1"] .ev-block__time')
        body.click()
        assert page.locator('.ev-block[data-ev-block="1"].is-context-selected').count() == 1
        body.click()
        assert page.locator('.ev-block[data-ev-block="1"].is-context-selected').count() == 0

        box = body.bounding_box()
        assert box is not None
        page.mouse.move(box["x"] + 5, box["y"] + 4)
        page.mouse.down()
        page.mouse.move(box["x"] + 30, box["y"] + 90, steps=10)
        assert page.locator(".ev-drag-overlay").count() == 1
        page.mouse.up()
        page.wait_for_timeout(250)
        assert page.locator("#modal-backdrop.is-open").count() == 0
        assert page.locator("#move-toast.is-visible").count() == 1
        assert not errors
        browser.close()

    print("Today v16 regression smoke test: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
