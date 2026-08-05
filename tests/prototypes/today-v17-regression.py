"""Regression tests for the standalone LifeOS Today v17 prototype.

Usage:
    python today-v17-regression.py /path/to/LifeOS_Home_Oggi_v17_canvas.html
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def parse_minute(text: str) -> int:
    match = re.match(r"(\d{2}):(\d{2})", text)
    assert match, text
    return int(match.group(1)) * 60 + int(match.group(2))


def launch_browser(playwright):
    system_chromium = shutil.which("chromium") or shutil.which("google-chrome")
    kwargs = {"headless": True}
    if system_chromium:
        kwargs.update(executable_path=system_chromium, args=["--no-sandbox"])
    return playwright.chromium.launch(**kwargs)


def load_page(browser, html: str):
    page = browser.new_page(viewport={"width": 1575, "height": 945})
    errors: list[str] = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    page.set_content(html, wait_until="load")
    page.wait_for_timeout(250)
    return page, errors


def rectangles_intersect(a: dict, b: dict) -> bool:
    return (
        min(a["right"], b["right"]) - max(a["left"], b["left"]) > 1
        and min(a["bottom"], b["bottom"]) - max(a["top"], b["top"]) > 1
    )


def main() -> int:
    prototype = Path(sys.argv[1] if len(sys.argv) > 1 else "LifeOS_Home_Oggi_v17_canvas.html")
    html = prototype.read_text(encoding="utf-8")

    with sync_playwright() as playwright:
        browser = launch_browser(playwright)

        page, errors = load_page(browser, html)
        assert page.title().endswith("v17")
        assert page.locator(".ev-block").count() >= 12
        assert not errors

        rects = page.evaluate(
            """() => [...document.querySelector('.day-section[data-date="2026-08-04"]').querySelectorAll('.ev-block')]
            .map(el => ({id: el.dataset.evBlock, rect: el.getBoundingClientRect().toJSON()}))"""
        )
        collisions = []
        for index, item in enumerate(rects):
            for other in rects[index + 1 :]:
                if rectangles_intersect(item["rect"], other["rect"]):
                    collisions.append((item["id"], other["id"]))
        assert not collisions, collisions

        initial_height = page.eval_on_selector(
            '.day-section[data-date="2026-08-04"] .tl-canvas',
            "el => parseFloat(getComputedStyle(el).height)",
        )
        assert initial_height > 1300

        page.locator('.js-filter-chip[data-cat="focus"]').click()
        page.wait_for_timeout(150)
        filtered_height = page.eval_on_selector(
            '.day-section[data-date="2026-08-04"] .tl-canvas',
            "el => parseFloat(getComputedStyle(el).height)",
        )
        assert abs(initial_height - filtered_height) < 0.5
        page.locator("#tl-toggle").click()
        page.wait_for_timeout(450)
        progress = page.eval_on_selector(
            "#content-grid",
            'el => getComputedStyle(el).getPropertyValue("--expand-progress").trim()',
        )
        assert progress == "1.000"
        filtered_widths = page.evaluate(
            """() => [...document.querySelectorAll('.day-section[data-date="2026-08-04"] .ev-block')]
            .map(el => parseFloat(getComputedStyle(el).width))"""
        )
        assert filtered_widths and max(filtered_widths) < 260
        page.close()

        page, errors = load_page(browser, html)
        body = page.locator('.ev-block[data-ev-block="2"] .ev-block__drag-zone')
        box = body.bounding_box()
        assert box
        x, y = box["x"] + max(3, box["width"] / 2), box["y"] + max(2, box["height"] / 2)
        page.mouse.move(x, y)
        page.mouse.down()
        page.mouse.move(x, y + 23, steps=8)
        page.mouse.up()
        page.wait_for_timeout(300)
        standard_time = page.locator('.ev-block[data-ev-block="2"] .ev-block__time').inner_text()
        assert parse_minute(standard_time) % 5 == 0, standard_time
        assert not errors
        page.close()

        page, errors = load_page(browser, html)
        for _ in range(5):
            page.locator('.js-zoom[data-dir="in"]').click()
            page.wait_for_timeout(60)
        assert page.locator("#tl-zoom-value").inner_text() == "190%"
        target = page.locator('.ev-block[data-ev-block="2"]')
        target.scroll_into_view_if_needed()
        page.wait_for_timeout(100)
        body = page.locator('.ev-block[data-ev-block="2"] .ev-block__drag-zone')
        box = body.bounding_box()
        assert box
        x, y = box["x"] + max(3, box["width"] / 2), box["y"] + max(2, box["height"] / 2)
        page.mouse.move(x, y)
        page.mouse.down()
        page.mouse.move(x, y + 30, steps=10)
        page.mouse.up()
        page.wait_for_timeout(300)
        precise_time = page.locator('.ev-block[data-ev-block="2"] .ev-block__time').inner_text()
        assert parse_minute(precise_time) % 5 != 0, precise_time
        assert not errors
        page.close()

        browser.close()

    print("Today v17 regression suite: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
